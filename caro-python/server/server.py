"""
Main Server for Caro Game
Handles client connections and manages game rooms
"""

import socket
import threading
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from same directory
from config import SERVER_HOST, SERVER_PORT, MAX_CLIENTS
from server_thread import ServerThread


class ServerThreadBus:
    """Manages all active server threads and rooms"""
    
    def __init__(self):
        self.threads = []
        self.rooms = []
        self.lock = threading.Lock()
        self.next_room_id = 100
    
    def add(self, server_thread):
        """Add a new server thread"""
        with self.lock:
            self.threads.append(server_thread)
    
    def remove(self, server_thread):
        """Remove a server thread"""
        with self.lock:
            if server_thread in self.threads:
                self.threads.remove(server_thread)
    
    def add_room(self, room):
        """Add a new room"""
        with self.lock:
            self.rooms.append(room)
    
    def remove_room(self, room):
        """Remove a room"""
        with self.lock:
            if room in self.rooms:
                self.rooms.remove(room)
    
    def find_room(self, room_id):
        """Find room by ID"""
        with self.lock:
            for room in self.rooms:
                if room.id == room_id:
                    return room
        return None
    
    def get_next_room_id(self):
        """Get next available room ID"""
        with self.lock:
            room_id = self.next_room_id
            self.next_room_id += 1
            return room_id
    
    def broadcast(self, sender_number, message):
        """Send message to all clients except sender"""
        with self.lock:
            for thread in self.threads:
                if thread.client_number != sender_number:
                    try:
                        thread.write(message)
                    except:
                        pass
    
    def broadcast_new_room(self, room):
        """Notify all clients about a new room"""
        if room.user1 and room.user1.user:
            message = (f"new-room,{room.id},1,{room.user1.user.nickname},"
                      f"{'1' if room.password else '0'}")
            self.broadcast(room.user1.client_number, message)
    
    def get_length(self):
        """Get number of active threads"""
        with self.lock:
            return len(self.threads)


class AdminConsole:
    """Simple admin console for server monitoring"""
    
    def __init__(self):
        self.messages = []
    
    def add_message(self, message):
        """Add message to console"""
        print(f"[ADMIN] {message}")
        self.messages.append(message)
    
    def run(self):
        """Run admin console (currently just prints messages)"""
        pass


class Server:
    """Main server class"""
    
    def __init__(self):
        self.server_socket = None
        self.server_thread_bus = ServerThreadBus()
        self.admin = AdminConsole()
        self.client_number = 0
        self.is_running = False
    
    def start(self):
        """Start the server"""
        try:
            # Create server socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((SERVER_HOST, SERVER_PORT))
            self.server_socket.listen(MAX_CLIENTS)
            
            self.is_running = True
            print(f"Server started on {SERVER_HOST}:{SERVER_PORT}")
            print("Server is waiting to accept users...")
            
            # Start admin console
            self.admin.run()
            
            # Accept client connections
            while self.is_running:
                try:
                    client_socket, address = self.server_socket.accept()
                    print(f"Client connected from: {address[0]}:{address[1]}")
                    
                    # Create and start server thread for client
                    server_thread = ServerThread(
                        client_socket,
                        self.client_number,
                        self.server_thread_bus,
                        self.admin
                    )
                    self.server_thread_bus.add(server_thread)
                    server_thread.start()
                    
                    print(f"Number of active threads: {self.server_thread_bus.get_length()}")
                    self.client_number += 1
                    
                except KeyboardInterrupt:
                    print("\nShutting down server...")
                    break
                except Exception as e:
                    print(f"Error accepting client: {e}")
        
        except Exception as e:
            print(f"Error starting server: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Stop the server"""
        self.is_running = False
        
        # Close all client connections
        for thread in self.server_thread_bus.threads[:]:
            try:
                thread.close()
            except:
                pass
        
        # Close server socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        print("Server stopped")


def main():
    """Main entry point"""
    print("="*50)
    print("Caro Game Server - Python Version")
    print("="*50)
    
    server = Server()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nServer interrupted by user")
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        server.stop()


if __name__ == "__main__":
    main()
