"""
User Data Access Object for database operations
"""

import mysql.connector
from mysql.connector import Error
import sys
import os

# Add parent directory to path to import shared modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Import from same directory
from config import DB_CONFIG
from shared.models import User


class UserDAO:
    """Handle all database operations for users"""
    
    def __init__(self):
        """Initialize database connection"""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            if self.connection.is_connected():
                print("Database connection successful")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.connection = None
    
    def verify_user(self, username, password):
        """Verify user credentials"""
        try:
            cursor = self.connection.cursor()
            query = """SELECT ID, username, password, nickname, avatar, 
                       numberOfGame, numberOfWin, numberOfDraw, IsOnline, IsPlaying
                       FROM user WHERE username = %s AND password = %s"""
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                rank = self.get_rank(result[0])
                return User(
                    user_id=result[0],
                    username=result[1],
                    password=result[2],
                    nickname=result[3],
                    avatar=result[4],
                    num_games=result[5],
                    num_wins=result[6],
                    num_draws=result[7],
                    is_online=result[8] != 0,
                    is_playing=result[9] != 0,
                    rank=rank
                )
            return None
        except Error as e:
            print(f"Error verifying user: {e}")
            return None
    
    def add_user(self, username, password, nickname, avatar):
        """Add new user to database"""
        try:
            cursor = self.connection.cursor()
            query = """INSERT INTO user(username, password, nickname, avatar)
                       VALUES(%s, %s, %s, %s)"""
            cursor.execute(query, (username, password, nickname, avatar))
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error adding user: {e}")
            return False
    
    def check_duplicated(self, username):
        """Check if username already exists"""
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM user WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            cursor.close()
            return result is not None
        except Error as e:
            print(f"Error checking duplicate: {e}")
            return False
    
    def check_is_banned(self, user_id):
        """Check if user is banned"""
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM banned_user WHERE ID_User = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            cursor.close()
            return result is not None
        except Error as e:
            print(f"Error checking ban status: {e}")
            return False
    
    def update_to_online(self, user_id):
        """Update user status to online"""
        try:
            cursor = self.connection.cursor()
            query = "UPDATE user SET IsOnline = 1 WHERE ID = %s"
            cursor.execute(query, (user_id,))
            self.connection.commit()
            cursor.close()
        except Error as e:
            print(f"Error updating online status: {e}")
    
    def update_to_offline(self, user_id):
        """Update user status to offline"""
        try:
            cursor = self.connection.cursor()
            query = "UPDATE user SET IsOnline = 0, IsPlaying = 0 WHERE ID = %s"
            cursor.execute(query, (user_id,))
            self.connection.commit()
            cursor.close()
        except Error as e:
            print(f"Error updating offline status: {e}")
    
    def update_to_playing(self, user_id):
        """Update user status to playing"""
        try:
            cursor = self.connection.cursor()
            query = "UPDATE user SET IsPlaying = 1 WHERE ID = %s"
            cursor.execute(query, (user_id,))
            self.connection.commit()
            cursor.close()
        except Error as e:
            print(f"Error updating playing status: {e}")
    
    def update_to_not_playing(self, user_id):
        """Update user status to not playing"""
        try:
            cursor = self.connection.cursor()
            query = "UPDATE user SET IsPlaying = 0 WHERE ID = %s"
            cursor.execute(query, (user_id,))
            self.connection.commit()
            cursor.close()
        except Error as e:
            print(f"Error updating not playing status: {e}")
    
    def add_game(self, user_id):
        """Increment number of games played"""
        try:
            cursor = self.connection.cursor()
            query = "UPDATE user SET numberOfGame = numberOfGame + 1 WHERE ID = %s"
            cursor.execute(query, (user_id,))
            self.connection.commit()
            cursor.close()
        except Error as e:
            print(f"Error adding game count: {e}")
    
    def add_win(self, user_id):
        """Increment number of wins"""
        try:
            cursor = self.connection.cursor()
            query = "UPDATE user SET numberOfWin = numberOfWin + 1 WHERE ID = %s"
            cursor.execute(query, (user_id,))
            self.connection.commit()
            cursor.close()
        except Error as e:
            print(f"Error adding win count: {e}")
    
    def add_draw(self, user_id):
        """Increment number of draws"""
        try:
            cursor = self.connection.cursor()
            query = "UPDATE user SET numberOfDraw = numberOfDraw + 1 WHERE ID = %s"
            cursor.execute(query, (user_id,))
            self.connection.commit()
            cursor.close()
        except Error as e:
            print(f"Error adding draw count: {e}")
    
    def get_rank(self, user_id):
        """Get user's rank based on wins"""
        try:
            cursor = self.connection.cursor()
            query = """SELECT COUNT(*) + 1 FROM user 
                       WHERE numberOfWin > (SELECT numberOfWin FROM user WHERE ID = %s)"""
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else 0
        except Error as e:
            print(f"Error getting rank: {e}")
            return 0
    
    def get_rank_list(self):
        """Get top users by rank"""
        try:
            cursor = self.connection.cursor()
            query = """SELECT ID, username, password, nickname, avatar, 
                       numberOfGame, numberOfWin, numberOfDraw, 0 as rank
                       FROM user ORDER BY numberOfWin DESC LIMIT 100"""
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            
            users = []
            for i, row in enumerate(results):
                user = User(
                    user_id=row[0],
                    username=row[1],
                    password=row[2],
                    nickname=row[3],
                    avatar=row[4],
                    num_games=row[5],
                    num_wins=row[6],
                    num_draws=row[7],
                    rank=i + 1
                )
                users.append(user)
            return users
        except Error as e:
            print(f"Error getting rank list: {e}")
            return []
    
    def get_list_friend(self, user_id):
        """Get user's friend list"""
        try:
            cursor = self.connection.cursor()
            query = """SELECT u.ID, u.nickname, u.IsOnline, u.IsPlaying
                       FROM user u
                       INNER JOIN friend f ON (f.ID_User1 = %s AND f.ID_User2 = u.ID)
                       OR (f.ID_User2 = %s AND f.ID_User1 = u.ID)"""
            cursor.execute(query, (user_id, user_id))
            results = cursor.fetchall()
            cursor.close()
            
            friends = []
            for row in results:
                friend = User(
                    user_id=row[0],
                    nickname=row[1],
                    is_online=row[2] != 0,
                    is_playing=row[3] != 0
                )
                friends.append(friend)
            return friends
        except Error as e:
            print(f"Error getting friend list: {e}")
            return []
    
    def check_friend(self, user1_id, user2_id):
        """Check if two users are friends"""
        try:
            cursor = self.connection.cursor()
            query = """SELECT * FROM friend 
                       WHERE (ID_User1 = %s AND ID_User2 = %s)
                       OR (ID_User1 = %s AND ID_User2 = %s)"""
            cursor.execute(query, (user1_id, user2_id, user2_id, user1_id))
            result = cursor.fetchone()
            cursor.close()
            return result is not None
        except Error as e:
            print(f"Error checking friend: {e}")
            return False
    
    def add_friend(self, user1_id, user2_id):
        """Add friend relationship"""
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO friend(ID_User1, ID_User2) VALUES(%s, %s)"
            cursor.execute(query, (user1_id, user2_id))
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error adding friend: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")
