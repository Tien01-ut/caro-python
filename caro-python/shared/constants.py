"""
Shared constants for Caro Game
"""

import sys
import os

# Try to import from network_config.py
try:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from network_config import SERVER_IP, SERVER_PORT
    SERVER_HOST = SERVER_IP
except ImportError:
    # Fallback to default
    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = 7777

# Game Settings
BOARD_SIZE = 15  # 15x15 board
WIN_CONDITION = 5  # 5 in a row to win

# Game Timer
GAME_TIMEOUT = 60  # 60 seconds per turn

# Protocol Messages
class Messages:
    # Client -> Server
    CLIENT_VERIFY = "client-verify"
    REGISTER = "register"
    OFFLINE = "offline"
    VIEW_FRIEND_LIST = "view-friend-list"
    GET_LIST_ROOM = "get-list-room"
    CREATE_ROOM = "create-room"
    JOIN_ROOM = "join-room"
    LEAVE_ROOM = "leave-room"
    START_GAME = "start-game"
    USER_MOVE = "user-move"
    CHAT = "chat"
    INVITE_FRIEND = "invite-friend"
    ACCEPT_FRIEND = "accept-friend"
    GET_RANK = "get-rank-charts"
    CHECK_FRIEND = "check-friend"
    DRAW_REQUEST = "draw-request"
    DRAW_ACCEPT = "draw-accept"
    DRAW_DECLINE = "draw-decline"
    ASK_FOR_REVENGE = "ask-for-revenge"
    ACCEPT_REVENGE = "accept-revenge"
    NOT_ACCEPT_REVENGE = "not-accept-revenge"
    WIN = "win"
    LOSE = "lose"
    SEND_MESSAGE = "send-message"
    
    # Server -> Client
    SERVER_SEND_ID = "server-send-id"
    LOGIN_SUCCESS = "login-success"
    WRONG_USER = "wrong-user"
    DUPLICATE_LOGIN = "dupplicate-login"
    BANNED_USER = "banned-user"
    DUPLICATE_USERNAME = "duplicate-username"
    CHAT_SERVER = "chat-server"
    ROOM_FULLY = "room-fully"
    ROOM_NOT_FOUND = "room-not-found"
    ROOM_WRONG_PASSWORD = "room-wrong-password"
    GO_TO_ROOM = "go-to-room"
    NEW_ROOM = "new-room"
    ROOM_LIST = "room-list"
    FRIEND_LIST = "friend-list"
    RETURN_GET_RANK = "return-get-rank-charts"
    CHECK_FRIEND_RESPONSE = "check-friend-response"
    START_GAME_SIGNAL = "start-game"
    COMPETITOR_MOVE = "competitor-move"
    DRAW_REQUEST_MSG = "draw-request"
    DRAW_ACCEPT_MSG = "draw-accept"
    ASK_REVENGE = "ask-for-revenge"
    COMPETITOR_LEFT = "competitor-left"
    YOU_WIN = "you-win"
    YOU_LOSE = "you-lose"
    RECEIVE_MESSAGE = "receive-message"

# UI Colors
COLORS = {
    'WHITE': '#FFFFFF',
    'BLACK': '#000000',
    'LIGHT_GRAY': '#F0F0F0',
    'DARK_GRAY': '#808080',
    'BLUE': '#0066CC',
    'GREEN': '#00CC66',
    'RED': '#CC0000',
    'YELLOW': '#FFCC00'
}

# Avatar options
AVATARS = ["avatar1", "avatar2", "avatar3", "avatar4", "avatar5", "avatar6"]
