"""
Room management for game sessions
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from user_dao import UserDAO


class Room:
    """Manages a game room with two players"""
    
    def __init__(self, room_id, user1_thread):
        """Initialize room with first player"""
        self.id = room_id
        self.user1 = user1_thread
        self.user2 = None
        self.password = ""
        self.user_dao = UserDAO()
        print(f"Room created successfully, ID: {self.id}")
    
    def set_password(self, password):
        """Set room password"""
        self.password = password
    
    def get_password(self):
        """Get room password"""
        return self.password
    
    def is_full(self):
        """Check if room has 2 players"""
        return self.user2 is not None
    
    def get_number_of_users(self):
        """Get current number of players"""
        return 2 if self.user2 else 1
    
    def add_user(self, user2_thread):
        """Add second player to room"""
        self.user2 = user2_thread
    
    def remove_user(self, client_number):
        """Remove a player from room"""
        if self.user1 and self.user1.client_number == client_number:
            self.user1 = None
        elif self.user2 and self.user2.client_number == client_number:
            self.user2 = None
    
    def broadcast(self, message):
        """Send message to both players in room"""
        try:
            if self.user1:
                self.user1.write(message)
            if self.user2:
                self.user2.write(message)
        except Exception as e:
            print(f"Error broadcasting in room {self.id}: {e}")
    
    def get_competitor(self, client_number):
        """Get the opponent of a given client"""
        if self.user1 and self.user1.client_number == client_number:
            return self.user2
        return self.user1
    
    def get_competitor_id(self, client_number):
        """Get opponent's user ID"""
        competitor = self.get_competitor(client_number)
        if competitor and competitor.user:
            return competitor.user.id
        return None
    
    def set_users_to_playing(self):
        """Update both users to playing status"""
        if self.user1 and self.user1.user:
            self.user_dao.update_to_playing(self.user1.user.id)
        if self.user2 and self.user2.user:
            self.user_dao.update_to_playing(self.user2.user.id)
    
    def set_users_to_not_playing(self):
        """Update both users to not playing status"""
        if self.user1 and self.user1.user:
            self.user_dao.update_to_not_playing(self.user1.user.id)
        if self.user2 and self.user2.user:
            self.user_dao.update_to_not_playing(self.user2.user.id)
    
    def increase_number_of_game(self):
        """Increment game count for both players"""
        if self.user1 and self.user1.user:
            self.user_dao.add_game(self.user1.user.id)
        if self.user2 and self.user2.user:
            self.user_dao.add_game(self.user2.user.id)
    
    def increase_win(self, client_number):
        """Increment win count for winner"""
        if self.user1 and self.user1.client_number == client_number:
            self.user_dao.add_win(self.user1.user.id)
        elif self.user2 and self.user2.client_number == client_number:
            self.user_dao.add_win(self.user2.user.id)
    
    def increase_draw(self):
        """Increment draw count for both players"""
        if self.user1 and self.user1.user:
            self.user_dao.add_draw(self.user1.user.id)
        if self.user2 and self.user2.user:
            self.user_dao.add_draw(self.user2.user.id)
    
    def __str__(self):
        """String representation of room"""
        return f"Room {self.id}: {self.get_number_of_users()}/2 players"
