"""
Server thread to handle individual client connections
"""

import socket
import threading
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from same directory
from user_dao import UserDAO
from shared.models import User


class ServerThread(threading.Thread):
    """Handle communication with a single client"""
    
    def __init__(self, client_socket, client_number, server_thread_bus, admin):
        """Initialize server thread for a client"""
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.client_number = client_number
        self.server_thread_bus = server_thread_bus
        self.admin = admin
        self.user = None
        self.room = None
        self.is_closed = False
        self.user_dao = UserDAO()
        
        # Get client IP
        try:
            self.client_ip = client_socket.getpeername()[0]
            if self.client_ip == "127.0.0.1":
                self.client_ip = "127.0.0.1"
        except:
            self.client_ip = "unknown"
        
        print(f"Server thread {client_number} started")
    
    def write(self, message):
        """Send message to client"""
        try:
            if not self.is_closed and self.client_socket:
                self.client_socket.sendall((message + "\n").encode('utf-8'))
        except Exception as e:
            print(f"Error sending to client {self.client_number}: {e}")
            self.close()
    
    def close(self):
        """Close connection"""
        if not self.is_closed:
            self.is_closed = True
            try:
                if self.user:
                    self.user_dao.update_to_offline(self.user.id)
                    self.server_thread_bus.broadcast(
                        self.client_number,
                        f"chat-server,{self.user.nickname} đã offline"
                    )
                    if self.admin:
                        self.admin.add_message(f"[{self.user.id}] {self.user.nickname} đã offline")
                
                if self.room:
                    competitor = self.room.get_competitor(self.client_number)
                    if competitor:
                        competitor.write("competitor-left,")
                    self.room.remove_user(self.client_number)
                
                self.client_socket.close()
                self.server_thread_bus.remove(self)
            except Exception as e:
                print(f"Error closing client {self.client_number}: {e}")
    
    def get_string_from_user(self, user):
        """Convert user object to string for transmission"""
        return user.to_string()
    
    def run(self):
        """Main thread loop to handle client messages"""
        try:
            # Send client ID
            self.write(f"server-send-id,{self.client_number}")
            
            # Receive messages
            buffer = ""
            while not self.is_closed:
                try:
                    data = self.client_socket.recv(4096).decode('utf-8')
                    if not data:
                        break
                    
                    buffer += data
                    while '\n' in buffer:
                        message, buffer = buffer.split('\n', 1)
                        if message:
                            self.process_message(message)
                
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"Error receiving from client {self.client_number}: {e}")
                    break
            
        except Exception as e:
            print(f"Error in client thread {self.client_number}: {e}")
        finally:
            self.close()
    
    def process_message(self, message):
        """Process incoming message from client"""
        parts = message.split(',')
        if not parts:
            return
        
        command = parts[0]
        
        # Client verification/login
        if command == "client-verify":
            username = parts[1] if len(parts) > 1 else ""
            password = parts[2] if len(parts) > 2 else ""
            
            user = self.user_dao.verify_user(username, password)
            if not user:
                self.write(f"wrong-user,{username},{password}")
            elif not user.is_online and not self.user_dao.check_is_banned(user.id):
                self.write(f"login-success,{self.get_string_from_user(user)}")
                self.user = user
                self.user_dao.update_to_online(self.user.id)
                self.server_thread_bus.broadcast(
                    self.client_number,
                    f"chat-server,{user.nickname} đang online"
                )
                if self.admin:
                    self.admin.add_message(f"[{user.id}] {user.nickname} đang online")
            elif self.user_dao.check_is_banned(user.id):
                self.write(f"banned-user,{username},{password}")
            else:
                self.write(f"dupplicate-login,{username},{password}")
        
        # Registration
        elif command == "register":
            username = parts[1] if len(parts) > 1 else ""
            password = parts[2] if len(parts) > 2 else ""
            nickname = parts[3] if len(parts) > 3 else ""
            avatar = parts[4] if len(parts) > 4 else "avatar1"
            
            if self.user_dao.check_duplicated(username):
                self.write("duplicate-username,")
            else:
                self.user_dao.add_user(username, password, nickname, avatar)
                user = self.user_dao.verify_user(username, password)
                if user:
                    self.user = user
                    self.user_dao.update_to_online(self.user.id)
                    self.server_thread_bus.broadcast(
                        self.client_number,
                        f"chat-server,{self.user.nickname} đang online"
                    )
                    self.write(f"login-success,{self.get_string_from_user(self.user)}")
        
        # Logout
        elif command == "offline":
            if self.user:
                self.user_dao.update_to_offline(self.user.id)
                if self.admin:
                    self.admin.add_message(f"[{self.user.id}] {self.user.nickname} đã offline")
                self.server_thread_bus.broadcast(
                    self.client_number,
                    f"chat-server,{self.user.nickname} đã offline"
                )
                self.user = None
        
        # View friend list
        elif command == "view-friend-list":
            if self.user:
                friends = self.user_dao.get_list_friend(self.user.id)
                friend_str = "friend-list"
                for friend in friends:
                    friend_str += f",{friend.id},{friend.nickname},"
                    friend_str += f"{'1' if friend.is_online else '0'},"
                    friend_str += f"{'1' if friend.is_playing else '0'}"
                self.write(friend_str)
        
        # Get rank list
        elif command == "get-rank-charts":
            users = self.user_dao.get_rank_list()
            rank_str = "return-get-rank-charts"
            for user in users:
                rank_str += f",{self.get_string_from_user(user)}"
            self.write(rank_str)
        
        # Check if friend
        elif command == "check-friend":
            if self.user and len(parts) > 1:
                friend_id = int(parts[1])
                is_friend = self.user_dao.check_friend(self.user.id, friend_id)
                self.write(f"check-friend-response,{'1' if is_friend else '0'}")
        
        # Get room list
        elif command == "get-list-room":
            room_list_str = "room-list"
            for room in self.server_thread_bus.rooms:
                if room.user1 and room.user1.user:
                    room_list_str += f",{room.id},{room.get_number_of_users()},"
                    room_list_str += f"{room.user1.user.nickname},"
                    room_list_str += f"{'1' if room.password else '0'}"
            self.write(room_list_str)
        
        # Create room
        elif command == "create-room":
            password = parts[1] if len(parts) > 1 else ""
            from room import Room
            new_room = Room(self.server_thread_bus.get_next_room_id(), self)
            if password:
                new_room.set_password(password)
            self.room = new_room
            self.server_thread_bus.add_room(new_room)
            self.write(f"create-room-success,{new_room.id}")
            # Notify others about new room
            self.server_thread_bus.broadcast_new_room(new_room)
        
        # Join room
        elif command == "join-room":
            if len(parts) > 1:
                room_id = int(parts[1])
                password = parts[2] if len(parts) > 2 else ""
                
                room = self.server_thread_bus.find_room(room_id)
                if not room:
                    self.write("room-not-found,")
                elif room.is_full():
                    self.write("room-fully,")
                elif room.password and room.password != password:
                    self.write("room-wrong-password,")
                else:
                    room.add_user(self)
                    self.room = room
                    # Notify both players
                    self.go_to_partner_room()
                    room.user1.go_to_own_room()
        
        # Leave room
        elif command == "leave-room":
            if self.room:
                competitor = self.room.get_competitor(self.client_number)
                if competitor:
                    competitor.write("competitor-left,")
                self.room.remove_user(self.client_number)
                self.server_thread_bus.remove_room(self.room)
                self.room = None
        
        # Start game
        elif command == "start-game":
            if self.room and self.room.is_full():
                self.room.set_users_to_playing()
                self.room.broadcast("start-game,")
        
        # User move
        elif command == "user-move":
            if self.room and len(parts) > 2:
                x = parts[1]
                y = parts[2]
                competitor = self.room.get_competitor(self.client_number)
                if competitor:
                    competitor.write(f"competitor-move,{x},{y}")
        
        # Win
        elif command == "win":
            if self.room:
                self.room.increase_number_of_game()
                self.room.increase_win(self.client_number)
                self.room.set_users_to_not_playing()
                competitor = self.room.get_competitor(self.client_number)
                if competitor:
                    competitor.write("you-lose,")
        
        # Lose
        elif command == "lose":
            if self.room:
                competitor = self.room.get_competitor(self.client_number)
                if competitor:
                    self.room.increase_number_of_game()
                    self.room.increase_win(competitor.client_number)
                    self.room.set_users_to_not_playing()
                    competitor.write("you-win,")
        
        # Draw request
        elif command == "draw-request":
            if self.room:
                competitor = self.room.get_competitor(self.client_number)
                if competitor:
                    competitor.write("draw-request,")
        
        # Draw accept
        elif command == "draw-accept":
            if self.room:
                self.room.increase_number_of_game()
                self.room.increase_draw()
                self.room.set_users_to_not_playing()
                competitor = self.room.get_competitor(self.client_number)
                if competitor:
                    competitor.write("draw-accept,")
        
        # Chat/send message
        elif command == "send-message":
            if self.room and len(parts) > 1:
                msg = ','.join(parts[1:])
                competitor = self.room.get_competitor(self.client_number)
                if competitor:
                    competitor.write(f"receive-message,{msg}")
    
    def go_to_own_room(self):
        """Notify user about going to their room"""
        if self.room and self.room.user2:
            competitor = self.room.user2
            self.write(
                f"go-to-room,{self.room.id},{competitor.client_ip},1,"
                f"{self.get_string_from_user(competitor.user)}"
            )
    
    def go_to_partner_room(self):
        """Notify user about joining partner's room"""
        if self.room and self.room.user1:
            host = self.room.user1
            self.write(
                f"go-to-room,{self.room.id},{host.client_ip},0,"
                f"{self.get_string_from_user(host.user)}"
            )
