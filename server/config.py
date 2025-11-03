"""
Database configuration for Caro Game Server
"""

# MySQL Configuration (XAMPP)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # XAMPP mặc định không có password
    'database': 'caro_game'
}

# Server Configuration
SERVER_HOST = '0.0.0.0'  # Listen on all interfaces
SERVER_PORT = 7777
MAX_CLIENTS = 100
THREAD_POOL_SIZE = 10
