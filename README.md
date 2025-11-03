<div align="center">

# 🎮 Caro Game - Python Edition

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-orange.svg)](https://www.mysql.com/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com)

**Trò chơi Caro multiplayer với AI thông minh, kiến trúc client-server hiện đại**

[Tính năng](#-tính-năng) •
[Demo](#-demo) •
[Cài đặt](#-cài-đặt) •
[Sử dụng](#-sử-dụng) •
[Tài liệu](#-tài-liệu)

</div>

---

## ✨ Tính năng

### 🖥️ Server
- ✅ Xử lý đa luồng với nhiều client đồng thời
- ✅ Quản lý phòng chơi (tạo, vào, rời phòng)
- ✅ Hệ thống đăng nhập/đăng ký với xác thực
- ✅ Quản lý trạng thái người chơi (online, offline, playing)
- ✅ Bảng xếp hạng theo thống kê thắng/thua
- ✅ Lưu trữ dữ liệu với MySQL
- ✅ Protocol messaging system

### 💻 Client
- ✅ Giao diện đồ họa đẹp mắt với Tkinter
- ✅ Đăng nhập/Đăng ký tài khoản
- ✅ Tạo phòng (có/không mật khẩu)
- ✅ Tham gia phòng từ danh sách
- ✅ Chơi game Caro 15x15 (5 in a row to win)
- ✅ Timer 60 giây cho mỗi lượt
- ✅ Hiển thị điểm số và lượt chơi
- ✅ Chat server (hiển thị thông báo)
- ✅ Xem bảng xếp hạng
- ✅ **Chơi với AI thông minh** (3 độ khó: Dễ, Trung bình, Khó)
- ✅ AI sử dụng thuật toán **Minimax với Alpha-Beta Pruning**



---

## 📸 Demo

### Giao diện chính

```
┌─────────────────────────────────────────────────────────────┐
│  🎮 CARO GAME - Chào mừng đến với game Caro online!         │
│                                                              │
│  📋 Đăng nhập           📋 Đăng ký           🏠 Trang chủ    │
│  ┌─────────────────┐   ┌──────────────┐    ┌─────────────┐ │
│  │ Username: ***   │   │ Tạo tài khoản│    │ Danh sách   │ │
│  │ Password: ***   │   │ mới ngay!    │    │ phòng chơi  │ │
│  └─────────────────┘   └──────────────┘    └─────────────┘ │
│                                                              │
│  🎮 Game Board (15x15)   🤖 AI Mode       👥 Multiplayer   │
│  ┌───────────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ X O X O X O X O X │  │ Độ khó: ★★☆  │  │ Room #1      │ │
│  │ O X O X O X O X O │  │ AI thinking..│  │ 2/2 players  │ │
│  │ X O X O X O X O X │  └──────────────┘  └──────────────┘ │
│  └───────────────────┘                                      │
└─────────────────────────────────────────────────────────────┘
```

### Chế độ chơi

| Mode | Description | Status |
|------|-------------|--------|
| 🤖 **Single Player** | Chơi với AI (3 độ khó) | ✅ Hoàn thành |
| 👥 **Local Multiplayer** | Chơi 2 người trên 1 máy | ✅ Hoàn thành |
| 🌐 **Online Multiplayer** | Chơi qua mạng LAN/WiFi | ✅ Hoàn thành |
| 🏆 **Tournament** | Chế độ giải đấu | 🚧 Đang phát triển |

---

## 🛠️ Tech Stack

<table>
<tr>
<td>

**Backend**
- 🐍 Python 3.8+
- 🗄️ MySQL 8.0+
- 🔌 Socket Programming
- 🧵 Multi-threading
- 📦 mysql-connector-python

</td>
<td>

**Frontend**
- 🖼️ Tkinter GUI
- 🎨 Custom Components
- 📊 Real-time Updates
- ⚡ Queue-based Events

</td>
<td>

**AI & Algorithms**
- 🤖 Minimax Algorithm
- ✂️ Alpha-Beta Pruning
- 🎯 Heuristic Evaluation
- ⚡ Move Optimization

</td>
</tr>
</table>

### Kiến trúc hệ thống

```
┌─────────────────────────────────────────────────────────┐
│                   CARO GAME SYSTEM                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐         ┌──────────────┐             │
│  │   CLIENT 1   │◄───────►│              │             │
│  └──────────────┘         │              │             │
│                           │    SERVER    │◄────► MySQL │
│  ┌──────────────┐         │              │             │
│  │   CLIENT 2   │◄───────►│  Port 7777   │             │
│  └──────────────┘         └──────────────┘             │
│                                                          │
│  [Tkinter GUI] ◄──► [Socket] ◄──► [Thread Pool]        │
│        ▲                               ▲                │
│        │                               │                │
│    [AI Engine]                    [Room Manager]        │
│   (Minimax)                      [User Manager]         │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 Yêu cầu hệ thống

### Phần cứng
- **RAM:** 512 MB (tối thiểu), 2 GB (khuyên dùng)
- **Ổ cứng:** 50 MB khả dụng
- **CPU:** Dual-core 1.0 GHz trở lên
- **Mạng:** LAN/WiFi (cho multiplayer online)

### Phần mềm
- **OS:** Windows 10/11, Linux, macOS
- **Python:** 3.8 hoặc cao hơn
- **MySQL:** 8.0+ (XAMPP khuyên dùng cho Windows)
- **Dependencies:** Xem `requirements.txt`

---

## 🚀 Cài đặt

### Bước 1: Clone repository

```bash
git clone https://github.com/Huyho-12/caro-python.git
cd caro-python
```

### Bước 2: Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### Bước 3: Cài đặt MySQL

**Windows (XAMPP):**
1. Tải XAMPP từ [https://www.apachefriends.org/](https://www.apachefriends.org/)
2. Cài đặt và khởi động MySQL từ XAMPP Control Panel

**Linux:**
```bash
sudo apt-get install mysql-server
sudo systemctl start mysql
```

**macOS:**
```bash
brew install mysql
brew services start mysql
```

### Bước 4: Tạo Database

```bash
python create_database.py
```

Script sẽ tự động:
- ✅ Tạo database `caro_game`
- ✅ Tạo bảng `user` với schema đầy đủ
- ✅ Thêm 5 tài khoản mẫu để test

**Tài khoản mẫu:**
| Username | Password | Role |
|----------|----------|------|
| `player1` | `player1` | Người chơi |
| `player2` | `player2` | Người chơi |
| `admin` | `admin` | Admin |

### Bước 5: Kiểm tra cấu hình (Tùy chọn)

**Chơi trên 1 máy:** Bỏ qua bước này

**Chơi trên 2 máy:**
```bash
python check_ip.py  # Xem IP của máy server
```

Sau đó sửa `network_config.py` trên máy client:
```python
SERVER_IP = "192.168.1.100"  # Thay bằng IP máy server
```

---

## 🎮 Sử dụng

### Khởi động Server

```bash
cd caro-python
python server/server.py
```

**Output:**
```
==================================================
Caro Game Server - Python Version
==================================================
Server Configuration:
- Host: 0.0.0.0
- Port: 7777
- Max Clients: 50
==================================================
[✓] Database connected successfully
[✓] Server started on port 7777
[✓] Waiting for clients...
==================================================

### Khởi động Client

Mở terminal **MỚI** (giữ server chạy):

```bash
python client/main.py
```

**Output:**
```
==================================================
Caro Game Client - Python Version
==================================================
[✓] Connected to server successfully
[✓] Client ID: #12345
==================================================
```

### Hướng dẫn sử dụng nhanh

1. **Đăng nhập:**
   - Username: `player1`
   - Password: `player1`

2. **Chọn chế độ chơi:**
   - 🤖 **Chơi với AI**: Luyện tập với AI thông minh
   - 🎮 **Tạo phòng**: Tạo phòng mới cho multiplayer
   - 📥 **Vào phòng**: Tham gia phòng có sẵn

3. **Chơi game:**
   - Bàn cờ 15x15 ô
   - 5 quân liên tiếp để thắng (ngang/dọc/chéo)
   - Mỗi lượt có 60 giây

**Máy 1 (Server):**
```bash
python check_ip.py       # Xem IP: 192.168.1.100
python server/server.py  # Khởi động server
```

**Máy 2 (Client):**
1. Sửa `network_config.py`:
   ```python
   SERVER_IP = "192.168.1.100"  # IP máy server
   ```
2. Chạy client:
   ```bash
   python client/main.py
   ```

📖 **Chi tiết:** Xem [MULTIPLAYER_GUIDE.md](MULTIPLAYER_GUIDE.md)

---

## Cấu trúc dự án

```
caro-python/
├── server/                        # Server side
│   ├── server.py                  # Server chính, xử lý kết nối
│   ├── server_thread.py           # Xử lý từng client
│   ├── room.py                    # Quản lý phòng chơi
│   ├── user_dao.py                # Truy vấn database
│   └── config.py                  # Cấu hình database & server
│
├── client/                        # Client side
│   ├── main.py                    # Entry point
│   ├── client.py                  # Client logic chính
│   ├── socket_handle.py           # Xử lý kết nối socket
│   ├── ai_player.py               # AI player (Minimax algorithm)
│   └── views/                     # Giao diện người dùng
│       ├── login_view.py          # Màn hình đăng nhập
│       ├── register_view.py       # Màn hình đăng ký
│       ├── home_view.py           # Trang chủ
│       ├── game_view.py           # Màn hình chơi multiplayer
│       └── game_ai_view.py        # Màn hình chơi với AI
│
├── shared/                        # Code dùng chung
│   ├── models.py                  # Data models (User, Point)
│   └── constants.py               # Hằng số & protocol messages
│
├── assets/                        # Tài nguyên (hình ảnh, icon, âm thanh)
│
├── network_config.py              # Cấu hình IP cho multiplayer
├── check_ip.py                    # Script kiểm tra IP
├── create_database.py             # Script tự động tạo database
├── requirements.txt               # Python dependencies
│
├── README.md                      # Tài liệu chính
├── QUICKSTART.md                  # Hướng dẫn nhanh 5 phút
├── INSTALL.md                     # Hướng dẫn cài đặt chi tiết
└── MULTIPLAYER_GUIDE.md           # Hướng dẫn chơi trên 2 máy
```

## 📖 Cấu trúc dự án

```
caro-python/
├── 📁 server/                     # Server-side application
│   ├── server.py                  # Main server với ThreadPoolExecutor
│   ├── server_thread.py           # Client handler (protocol processing)
│   ├── room.py                    # Room management & game logic
│   ├── user_dao.py                # Database operations (DAO pattern)
│   └── config.py                  # Database & server configuration
│
├── 📁 client/                     # Client-side application
│   ├── main.py                    # Application entry point
│   ├── client.py                  # Main client controller
│   ├── socket_handle.py           # Socket communication handler
│   ├── ai_player.py               # AI engine (Minimax + Alpha-Beta)
│   └── 📁 views/                  # GUI components
│       ├── login_view.py          # Login screen
│       ├── register_view.py       # Registration screen
│       ├── home_view.py           # Main lobby
│       ├── game_view.py           # Multiplayer game board
│       └── game_ai_view.py        # AI game board
│
├── 📁 shared/                     # Shared modules
│   ├── models.py                  # Data models (User, Point)
│   └── constants.py               # Protocol constants & messages
│
├── 📁 assets/                     # Resources
│   ├── avatar/                    # User avatars
│   ├── icon/                      # App icons
│   └── sound/                     # Sound effects (future)
│
├── 🛠️ Tools & Config
│   ├── network_config.py          # Network configuration
│   ├── check_ip.py                # IP checker utility
│   ├── create_database.py         # Database setup script
│   └── requirements.txt           # Python dependencies
│
└── 📚 Documentation
    ├── README.md                  # This file
    ├── QUICKSTART.md              # 5-minute quick start
    ├── INSTALL.md                 # Detailed installation
    ├── MULTIPLAYER_GUIDE.md       # LAN/WiFi multiplayer guide
    └── CHANGELOG.md               # Version history
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [QUICKSTART.md](QUICKSTART.md) | 🚀 5-minute quick start guide |
| [INSTALL.md](INSTALL.md) | 📦 Detailed installation instructions |
| [MULTIPLAYER_GUIDE.md](MULTIPLAYER_GUIDE.md) | 🌐 LAN/WiFi multiplayer setup |
| [CHANGELOG.md](CHANGELOG.md) | 📝 Version history & updates |

---

## 🎯 API & Commands

### Quick Commands

```bash
# Development
python check_ip.py              # Check machine IP address
python create_database.py       # Setup database automatically

# Running
python server/server.py         # Start game server
python client/main.py           # Start game client

# Testing
python -m pytest tests/         # Run unit tests (if available)
```

### Server Configuration

File: `server/config.py`
```python
DB_CONFIG = {
    'host': 'localhost',          # MySQL host
    'user': 'root',                # MySQL username  
    'password': '',                # MySQL password (empty for XAMPP)
    'database': 'caro_game'        # Database name
}

SERVER_HOST = '0.0.0.0'           # Listen on all interfaces
SERVER_PORT = 7777                # Server port
MAX_CLIENTS = 50                  # Max concurrent clients
```

### Client Configuration

File: `network_config.py`
```python
SERVER_IP = "127.0.0.1"           # Server IP (localhost)
SERVER_PORT = 7777                # Server port (must match server)
```

---

## 🐛 Troubleshooting

<details>
<summary><strong>❌ Database Connection Failed</strong></summary>

**Problem:** `Can't connect to MySQL server`

**Solutions:**
1. Start MySQL/XAMPP:
   ```bash
   # Windows: Open XAMPP Control Panel → Start MySQL
   # Linux: sudo systemctl start mysql
   ```
2. Verify credentials in `server/config.py`
3. Create database:
   ```bash
   python create_database.py
   ```
4. Check MySQL is running:
   ```bash
   netstat -ano | findstr 3306
   ```

</details>

<details>
<summary><strong>❌ Server Connection Timeout</strong></summary>

**Problem:** Client can't connect to server

**Solutions:**
1. Verify server is running
2. Check `network_config.py` has correct IP
3. Disable Firewall temporarily or allow port 7777
4. Test connection:
   ```bash
   ping 192.168.1.100  # Replace with server IP
   telnet 192.168.1.100 7777
   ```

</details>

<details>
<summary><strong>⚠️ AI Too Slow</strong></summary>

**Problem:** AI takes too long to make a move

**Solutions:**
- Use "Medium" difficulty (recommended)
- "Hard" difficulty may take 3-5 seconds
- Ensure your CPU meets requirements

</details>

<details>
<summary><strong>⚠️ GUI Not Responding</strong></summary>

**Problem:** Window freezes or doesn't update

**Solutions:**
1. Close and restart client
2. Check server logs for errors
3. Verify Python 3.8+ is installed
4. Update Tkinter:
   ```bash
   # Linux
   sudo apt-get install python3-tk
   ```

</details>

---

## 🎯 Highlights & Features

### 🤖 Intelligent AI
- **Algorithm:** Minimax with Alpha-Beta Pruning
- **Difficulty Levels:** Easy (random), Medium (depth 2), Hard (depth 3)
- **Optimization:** Move ordering, heuristic evaluation, smart move selection
- **Performance:** < 2s response time on average hardware

### 🌐 Networking
- **Protocol:** Custom socket-based protocol
- **Architecture:** Multi-threaded server with ThreadPoolExecutor
- **Scalability:** Supports 50+ concurrent clients
- **Features:** Room management, user authentication, real-time updates

### 🎨 User Experience
- **GUI Framework:** Tkinter with custom components
- **Responsive:** Queue-based event handling for smooth UI
- **Intuitive:** Simple navigation, clear game state indicators
- **Customizable:** Easy to extend and modify

---

## � Contributing

We welcome contributions! Here's how you can help:

1. **Report Bugs:** Open an issue with detailed description
2. **Suggest Features:** Share your ideas in issues
3. **Submit Pull Requests:** Fork, create branch, commit, push, PR
4. **Improve Documentation:** Fix typos, add examples
5. **Share:** Star ⭐ the project and share with friends!

### Development Setup

```bash
git clone https://github.com/Huyho-12/caro-python.git
cd caro-python
pip install -r requirements.txt
python create_database.py
```

### Code Style
- Follow PEP 8 guidelines
- Add docstrings to functions
- Comment complex logic
- Test before committing

---

## 📊 Project Status

| Feature | Status | Version |
|---------|--------|---------|
| Core Game Engine | ✅ Complete | 2.0.0 |
| AI Player | ✅ Complete | 2.0.0 |
| Multiplayer (LAN) | ✅ Complete | 2.0.0 |
| User Authentication | ✅ Complete | 2.0.0 |
| Room Management | ✅ Complete | 2.0.0 |
| Friend System | 🚧 In Progress | TBD |
| Tournament Mode | 📋 Planned | TBD |
| Sound Effects | 📋 Planned | TBD |
| Online Multiplayer | 📋 Planned | TBD |

---

## 🙏 Acknowledgments

- **Python Community** - For amazing libraries and support
- **MySQL** - Reliable database system
- **Tkinter** - Simple yet powerful GUI framework
- **Minimax Algorithm** - Foundation of AI intelligence

---

## 📄 License

```
MIT License

Copyright (c) 2025 Caro Game Python

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

<div align="center">

**Made with ❤️ and ☕**

⭐ Star this project if you find it useful!

[⬆ Back to top](#-caro-game---python-edition)

</div>
