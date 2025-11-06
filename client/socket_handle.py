"""
Socket handler for client communication with server
"""

import socket
import threading
import sys
import os
import time
from queue import Queue

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.models import User
from shared.constants import SERVER_HOST, SERVER_PORT


class SocketHandle:
    """Handle socket communication with server"""
    
    def __init__(self, client):
        self.client = client
        self.socket = None
        self.is_connected = False
        self.receive_thread = None
        self.message_queue = Queue()  # Thread-safe queue
        self.process_thread = None  # Message processing thread
        self._stop_processing = False  # Flag to stop processing thread
    
    def connect(self):
        """Connect to server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((SERVER_HOST, SERVER_PORT))
            self.is_connected = True
            print("Connected to server successfully!")
            
            # Start receiving thread
            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.daemon = True
            self.receive_thread.start()
            
            # Start processing thread
            self.start_processing()
            
            return True
        except Exception as e:
            print(f"Error connecting to server: {e}")
            return False
    
    def write(self, message):
        """Send message to server"""
        try:
            if self.socket and self.is_connected:
                self.socket.sendall((message + "\n").encode('utf-8'))
                print(f"[DEBUG] Sent message: {message}")
        except Exception as e:
            print(f"Error sending message: {e}")
            self.is_connected = False
    
    def receive_messages(self):
        """Receive messages from server"""
        buffer = ""
        while self.is_connected:
            try:
                data = self.socket.recv(4096).decode('utf-8')
                if not data:
                    print("[DEBUG] Connection closed by server (no data)")
                    break
                
                buffer += data
                while '\n' in buffer:
                    message, buffer = buffer.split('\n', 1)
                    if message:
                        # Put message in queue instead of processing directly
                        print(f"[DEBUG] Queued message: {message}")
                        self.message_queue.put(message)
            
            except Exception as e:
                print(f"Error receiving message: {e}")
                break
        
        self.is_connected = False
        print("Disconnected from server")
    
    def start_processing(self):
        """Start message processing thread"""
        if self.process_thread is None:
            self._stop_processing = False
            self.process_thread = threading.Thread(target=self._process_queue_thread)
            self.process_thread.daemon = True
            self.process_thread.start()
            print("[DEBUG] Message processing thread started")

    def _process_queue_thread(self):
        """Process messages in a separate thread"""
        print("[DEBUG] Message processing thread running")
        while not self._stop_processing:
            try:
                # Process all pending messages
                while not self.message_queue.empty():
                    try:
                        message = self.message_queue.get_nowait()
                        print(f"[DEBUG] Processing message: {message}")
                        self.process_message(message)
                    except:
                        break
                # Sleep a bit to prevent busy-waiting
                time.sleep(0.1)
            except:
                pass

    def process_message(self, message):
        """Process message from server"""
        try:
            parts = message.split(',')
            if not parts:
                return
            
            command = parts[0]
            print(f"[DEBUG] Processing command: {command}")
        except Exception as e:
            print(f"Error parsing message: {e}")
            return
        
        # Server sends client ID
        if command == "server-send-id":
            client_id = int(parts[1]) if len(parts) > 1 else 0
            print(f"Received client ID: {client_id}")
        
        # Login successful
        elif command == "login-success":
            print("Login successful")
            user = User.from_string(','.join(parts[1:]))
            if user:
                self.client.on_login_success(user)
        
        # Wrong credentials
        elif command == "wrong-user":
            self.client.on_login_error("Tài khoản hoặc mật khẩu không chính xác")
        
        # Duplicate login
        elif command == "dupplicate-login":
            self.client.on_login_error("Tài khoản đã đăng nhập ở nơi khác")
        
        # Banned user
        elif command == "banned-user":
            self.client.on_login_error("Tài khoản đã bị ban")
        
        # Duplicate username in registration
        elif command == "duplicate-username":
            self.client.on_register_error("Tên tài khoản đã được sử dụng")
        
        # Chat message from server
        elif command == "chat-server":
            msg = parts[1] if len(parts) > 1 else ""
            self.client.on_chat_message(msg)
        
        # Room list
        elif command == "room-list":
            print("[DEBUG] Received room list")
            rooms = []
            i = 1
            while i < len(parts):
                if i + 3 < len(parts):
                    room = {
                        'id': int(parts[i]),
                        'players': int(parts[i+1]),
                        'host': parts[i+2],
                        'has_password': parts[i+3] == '1'
                    }
                    rooms.append(room)
                    i += 4
                else:
                    break
            print(f"[DEBUG] Room list: {len(rooms)} rooms")
            self.client.on_room_list(rooms)
        
        # New room created
        elif command == "new-room":
            print("[DEBUG] New room notification received")
            if len(parts) >= 4:
                room = {
                    'id': int(parts[1]),
                    'players': int(parts[2]),
                    'host': parts[3],
                    'has_password': parts[4] == '1' if len(parts) > 4 else False
                }
                print(f"[DEBUG] New room: {room}")
                self.client.on_new_room(room)
        
        # Create room success
        elif command == "create-room-success":
            room_id = int(parts[1]) if len(parts) > 1 else 0
            print(f"[DEBUG] Room {room_id} created successfully")
            self.client.on_create_room_success(room_id)
        
        # Go to room
        elif command == "go-to-room":
            if len(parts) >= 5:
                room_id = int(parts[1])
                competitor_ip = parts[2]
                is_host = parts[3] == '1'
                competitor = User.from_string(','.join(parts[4:]))
                print(f"[DEBUG] Going to room {room_id}, is_host={is_host}")
                self.client.on_go_to_room(room_id, competitor, is_host, competitor_ip)
        
        # Room errors
        elif command == "room-fully":
            self.client.on_room_error("Phòng chơi đã đủ 2 người chơi")
        elif command == "room-not-found":
            self.client.on_room_error("Không tìm thấy phòng")
        elif command == "room-wrong-password":
            self.client.on_room_error("Mật khẩu phòng sai")
        
        # Friend list
        elif command == "friend-list":
            friends = []
            i = 1
            while i < len(parts):
                if i + 3 < len(parts):
                    friend = User(
                        user_id=int(parts[i]),
                        nickname=parts[i+1],
                        is_online=parts[i+2] == '1',
                        is_playing=parts[i+3] == '1'
                    )
                    friends.append(friend)
                    i += 4
                else:
                    break
            self.client.on_friend_list(friends)
        
        # Rank list
        elif command == "return-get-rank-charts":
            users = []
            i = 1
            while i < len(parts):
                if i + 8 < len(parts):
                    user = User(
                        user_id=int(parts[i]),
                        username=parts[i+1],
                        password=parts[i+2],
                        nickname=parts[i+3],
                        avatar=parts[i+4],
                        num_games=int(parts[i+5]),
                        num_wins=int(parts[i+6]),
                        num_draws=int(parts[i+7]),
                        rank=int(parts[i+8])
                    )
                    users.append(user)
                    i += 9
                else:
                    break
            self.client.on_rank_list(users)
        
        # Check friend response
        elif command == "check-friend-response":
            is_friend = parts[1] == '1' if len(parts) > 1 else False
            self.client.on_check_friend(is_friend)
        
        # Game events
        elif command == "start-game":
            print("[DEBUG] Game starting!")
            self.client.on_start_game()
        elif command == "competitor-move":
            if len(parts) >= 3:
                x = int(parts[1])
                y = int(parts[2])
                print(f"[DEBUG] Competitor moved to ({x}, {y})")
                self.client.on_competitor_move(x, y)
        elif command == "you-win":
            self.client.on_game_result("win")
        elif command == "you-lose":
            self.client.on_game_result("lose")
        elif command == "draw-request":
            self.client.on_draw_request()
        elif command == "draw-accept":
            self.client.on_draw_accept()
        elif command == "competitor-left":
            print("[DEBUG] Competitor left the game")
            self.client.on_competitor_left()
        
        # Chat in game
        elif command == "receive-message":
            msg = ','.join(parts[1:]) if len(parts) > 1 else ""
            self.client.on_receive_message(msg)
    
    def close(self):
        """Close connection"""
        self.is_connected = False
        # Stop message processing thread
        self._stop_processing = True
        if self.process_thread:
            try:
                self.process_thread.join(timeout=1.0)
            except:
                pass
            self.process_thread = None
        # Close socket
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        print("Connection closed")
