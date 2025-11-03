"""
Shared data models for Caro Game
"""

class User:
    """User model"""
    
    def __init__(self, user_id=None, username="", password="", nickname="", 
                 avatar="", num_games=0, num_wins=0, num_draws=0, 
                 is_online=False, is_playing=False, rank=0):
        self.id = user_id
        self.username = username
        self.password = password
        self.nickname = nickname
        self.avatar = avatar
        self.num_games = num_games
        self.num_wins = num_wins
        self.num_draws = num_draws
        self.is_online = is_online
        self.is_playing = is_playing
        self.rank = rank
    
    def to_string(self):
        """Convert user to comma-separated string for network transmission"""
        return f"{self.id},{self.username},{self.password},{self.nickname}," \
               f"{self.avatar},{self.num_games},{self.num_wins},{self.num_draws},{self.rank}"
    
    @staticmethod
    def from_string(data_str):
        """Create User from comma-separated string"""
        parts = data_str.split(',')
        if len(parts) >= 9:
            return User(
                user_id=int(parts[0]),
                username=parts[1],
                password=parts[2],
                nickname=parts[3],
                avatar=parts[4],
                num_games=int(parts[5]),
                num_wins=int(parts[6]),
                num_draws=int(parts[7]),
                rank=int(parts[8])
            )
        return None
    
    def __str__(self):
        return f"User({self.id}, {self.username}, {self.nickname})"


class Point:
    """Point model for game board"""
    
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False
    
    def __str__(self):
        return f"Point({self.x}, {self.y})"
