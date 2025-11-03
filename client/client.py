"""
Main Client for Caro Game
"""

import sys
import os
import tkinter as tk

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from socket_handle import SocketHandle
from views.login_view import LoginView
from views.register_view import RegisterView
from views.home_view import HomeView
from views.game_view import GameView
from views.game_ai_view import GameAIView


class Client:
    """Main client application"""
    
    def __init__(self):
        self.user = None
        self.socket_handle = SocketHandle(self)
        self.current_view = None
        self.game_view = None
        self.root = None  # Store root window
        
        # Connect to server
        if not self.socket_handle.connect():
            print("Failed to connect to server!")
            sys.exit(1)
    
    # View management
    def open_login_view(self):
        """Open login view"""
        if self.current_view:
            try:
                self.current_view.close()
            except:
                pass
        
        self.current_view = LoginView(self)
        # Start processing socket messages in main thread
        self.socket_handle.process_queue()
        self.current_view.show()
    
    def open_register_view(self):
        """Open register view"""
        if self.current_view:
            try:
                self.current_view.close()
            except:
                pass
        
        self.current_view = RegisterView(self)
        self.current_view.show()
    
    def open_home_view(self):
        """Open home view"""
        print(f"Opening home view for user: {self.user.nickname if self.user else 'None'}")
        
        # Close old window properly
        if self.current_view and hasattr(self.current_view, 'window'):
            try:
                self.current_view.window.destroy()
            except:
                pass
        
        if self.user:
            # Create new home view
            self.current_view = HomeView(self, self.user)
            print("Home view created")
            # Don't call show() - it will start a new mainloop
            # Just make sure window is visible
            self.current_view.window.deiconify()
            self.current_view.window.lift()
            self.current_view.window.focus_force()
    
    def open_game_view(self, room_id, competitor, is_host, competitor_ip):
        """Open game view"""
        print(f"Opening game view for room {room_id}")
        
        # Close old window properly
        if self.current_view and hasattr(self.current_view, 'window'):
            try:
                self.current_view.window.destroy()
            except:
                pass
        
        # Create game view
        self.game_view = GameView(self, room_id, competitor, is_host, competitor_ip)
        self.current_view = self.game_view
        
        # Make sure window is visible
        self.game_view.window.deiconify()
        self.game_view.window.lift()
        self.game_view.window.focus_force()
    
    def open_ai_game_view(self, difficulty="medium"):
        """Open AI game view"""
        print(f"Opening AI game view with difficulty: {difficulty}")
        
        # Close old window properly
        if self.current_view and hasattr(self.current_view, 'window'):
            try:
                self.current_view.window.destroy()
            except:
                pass
        
        # Create AI game view
        self.game_view = GameAIView(self, difficulty)
        self.current_view = self.game_view
        
        # Make sure window is visible
        self.game_view.window.deiconify()
        self.game_view.window.lift()
        self.game_view.window.focus_force()
    
    # Callbacks from socket handler
    def on_login_success(self, user):
        """Handle successful login"""
        self.user = user
        print(f"Login successful: {user.nickname}")
        # Schedule opening home view after current event loop
        if self.current_view and hasattr(self.current_view, 'window'):
            self.current_view.window.after(100, self.open_home_view)
        else:
            self.open_home_view()
    
    def on_login_error(self, message):
        """Handle login error"""
        if self.current_view and hasattr(self.current_view, 'show_error'):
            self.current_view.show_error(message)
    
    def on_register_error(self, message):
        """Handle registration error"""
        if self.current_view and hasattr(self.current_view, 'show_error'):
            self.current_view.show_error(message)
    
    def on_chat_message(self, message):
        """Handle chat message from server"""
        if self.current_view and hasattr(self.current_view, 'add_chat_message'):
            self.current_view.add_chat_message(message)
    
    def on_room_list(self, rooms):
        """Handle room list from server"""
        if self.current_view and hasattr(self.current_view, 'update_room_list'):
            self.current_view.update_room_list(rooms)
    
    def on_new_room(self, room):
        """Handle new room notification"""
        # Refresh room list
        if self.current_view and hasattr(self.current_view, 'refresh_rooms'):
            self.current_view.refresh_rooms()
    
    def on_create_room_success(self, room_id):
        """Handle room creation success"""
        print(f"Room {room_id} created successfully")
        # Stay in home view and wait for opponent
    
    def on_go_to_room(self, room_id, competitor, is_host, competitor_ip):
        """Handle going to room"""
        print(f"Going to room {room_id}")
        self.open_game_view(room_id, competitor, is_host, competitor_ip)
    
    def on_room_error(self, message):
        """Handle room error"""
        import tkinter.messagebox as messagebox
        messagebox.showerror("Lỗi phòng", message)
    
    def on_friend_list(self, friends):
        """Handle friend list"""
        print(f"Friends: {[f.nickname for f in friends]}")
    
    def on_rank_list(self, users):
        """Handle rank list"""
        print("Top ranked players:")
        for i, user in enumerate(users[:10], 1):
            print(f"{i}. {user.nickname} - Wins: {user.num_wins}")
    
    def on_check_friend(self, is_friend):
        """Handle check friend response"""
        pass
    
    def on_start_game(self):
        """Handle game start"""
        if self.game_view:
            print("Game started!")
    
    def on_competitor_move(self, x, y):
        """Handle competitor move"""
        if self.game_view:
            self.game_view.on_competitor_move(x, y)
    
    def on_game_result(self, result):
        """Handle game result"""
        if self.game_view:
            if result == "win":
                self.game_view.on_win()
            elif result == "lose":
                self.game_view.on_lose()
    
    def on_draw_request(self):
        """Handle draw request from competitor"""
        if self.game_view:
            import tkinter.messagebox as messagebox
            if messagebox.askyesno("Yêu cầu hòa", "Đối thủ muốn hòa. Bạn có đồng ý?"):
                self.socket_handle.write("draw-accept,")
                self.game_view.on_draw()
            else:
                self.socket_handle.write("draw-decline,")
    
    def on_draw_accept(self):
        """Handle draw accepted"""
        if self.game_view:
            self.game_view.on_draw()
    
    def on_competitor_left(self):
        """Handle competitor leaving"""
        import tkinter.messagebox as messagebox
        messagebox.showinfo("Thông báo", "Đối thủ đã rời phòng")
        if self.game_view:
            self.game_view.close()
        self.open_home_view()
    
    def on_receive_message(self, message):
        """Handle receiving chat message in game"""
        if self.game_view:
            self.game_view.on_receive_message(message)
    
    def quit(self):
        """Quit application"""
        self.socket_handle.close()
        sys.exit(0)


def main():
    """Main entry point"""
    print("="*50)
    print("Caro Game Client - Python Version")
    print("="*50)
    
    try:
        client = Client()
        client.open_login_view()
    except KeyboardInterrupt:
        print("\nClient interrupted by user")
    except Exception as e:
        print(f"Client error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
