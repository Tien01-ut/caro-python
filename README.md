# Caro Game - Python Version

Game Caro (Tic-Tac-Toe) multiplayer với kiến trúc client-server, hỗ trợ chơi trực tuyến và chơi với AI.

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

### 🌐 Multiplayer
- ✅ Chơi trên cùng 1 máy (nhiều client)
- ✅ Chơi trên 2 máy khác nhau (LAN/WiFi)
- ✅ Cấu hình IP dễ dàng qua file config
- ✅ Auto-reconnect và xử lý lỗi mạng

## 🛠️ Công nghệ sử dụng

- **Language:** Python 3.8+
- **GUI:** Tkinter (built-in)
- **Database:** MySQL 8.0+ (XAMPP recommended)
- **Networking:** Socket programming
- **Threading:** Multi-threaded server, Queue-based client
- **AI Algorithm:** Minimax with Alpha-Beta Pruning
- **Libraries:** mysql-connector-python

## 📋 Yêu cầu

- Python 3.8 trở lên
- MySQL 8.0+ (XAMPP hoặc MySQL standalone)
- Các thư viện Python (xem `requirements.txt`)

## Cài đặt

### 1. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### 1.5. Kiểm tra IP máy tính (nếu chơi trên 2 máy)

```bash
python check_ip.py
```

### 2. Cấu hình Database

Chạy script SQL để tạo database:

```sql
CREATE DATABASE caro_game;
USE caro_game;

CREATE TABLE `user`(
    ID int AUTO_INCREMENT PRIMARY KEY,
    `username` varchar(255) UNIQUE,
    `password` varchar(255),
    nickname varchar(255),
    avatar varchar(255),
    numberOfGame int DEFAULT 0,
    numberOfWin int DEFAULT 0,
    numberOfDraw int DEFAULT 0,
    IsOnline int DEFAULT 0,
    IsPlaying int DEFAULT 0
);

CREATE TABLE friend(
    ID_User1 int NOT NULL,
    ID_User2 int NOT NULL,
    FOREIGN KEY (ID_User1) REFERENCES `user`(ID),
    FOREIGN KEY (ID_User2) REFERENCES `user`(ID),
    CONSTRAINT PK_friend PRIMARY KEY (ID_User1,ID_User2)
);

CREATE TABLE banned_user(
    ID_User int PRIMARY KEY NOT NULL,
    FOREIGN KEY (ID_User) REFERENCES `user`(ID)
);
```

### 3. Cấu hình kết nối

Chỉnh sửa file `server/config.py`:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'caro_game'
}
```

## Chạy chương trình

### Khởi động Server

```bash
python server/server.py
```

Server sẽ lắng nghe trên port 7777

### Khởi động Client

```bash
python client/main.py
```

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
├── setup_database_mysql.sql       # SQL script cho MySQL
├── requirements.txt               # Python dependencies
│
├── README.md                      # Tài liệu chính
├── QUICKSTART.md                  # Hướng dẫn nhanh 5 phút
├── INSTALL.md                     # Hướng dẫn cài đặt chi tiết
└── MULTIPLAYER_GUIDE.md           # Hướng dẫn chơi trên 2 máy
```

## Hướng dẫn sử dụng

### Chơi trên cùng 1 máy
1. **Đăng ký tài khoản**: Tạo tài khoản mới với username, password, nickname
2. **Đăng nhập**: Đăng nhập với tài khoản đã tạo
3. **Chơi với AI**: Nhấn "Chơi với AI" để chơi đơn
4. **Chơi multiplayer**: Tạo phòng hoặc vào phòng có sẵn

### Chơi trên 2 máy khác nhau

**Máy 1 (Server):**
1. Chạy `python check_ip.py` để xem IP (ví dụ: 192.168.1.100)
2. Chạy server: `python server/server.py`
3. Chạy client: `python client/main.py` (có thể chơi luôn trên máy này)

**Máy 2 (Client):**
1. Mở file `network_config.py`
2. Sửa dòng: `SERVER_IP = "192.168.1.100"` (thay bằng IP máy Server)
3. Lưu file
4. Chạy client: `python client/main.py`

**Lưu ý:**
- 2 máy phải cùng mạng WiFi/LAN
- Tắt Firewall hoặc cho phép port 7777

### Luật chơi
- Bàn cờ 15x15 ô
- Người đầu tiên có 5 ô liên tiếp (ngang/dọc/chéo) thắng
- Mỗi lượt có 60 giây
- Player 1 (X) đánh trước, Player 2 (O) đánh sau

---

## 📚 Tài liệu thêm

- [QUICKSTART.md](QUICKSTART.md) - Hướng dẫn nhanh 5 phút
- [INSTALL.md](INSTALL.md) - Hướng dẫn cài đặt chi tiết từng bước
- [MULTIPLAYER_GUIDE.md](MULTIPLAYER_GUIDE.md) - Hướng dẫn chi tiết chơi trên 2 máy

## 🎯 Các lệnh hữu ích

```bash
# Kiểm tra IP máy tính
python check_ip.py

# Tạo database tự động
python create_database.py

# Chạy server
python server/server.py

# Chạy client
python client/main.py
```

## 🐛 Troubleshooting

### Lỗi kết nối database
- Đảm bảo MySQL/XAMPP đã chạy
- Kiểm tra `server/config.py` có đúng thông tin không
- Chạy `python create_database.py` để tạo database

### Lỗi kết nối server
- Kiểm tra server có đang chạy không
- Kiểm tra IP trong `network_config.py`
- Kiểm tra Firewall có chặn port 7777 không

### AI chạy chậm
- Độ khó "Khó" sẽ mất vài giây để tính toán
- Chọn độ khó "Trung bình" để cân bằng

## 🎯 Điểm nổi bật

Dự án được phát triển với các tính năng nổi bật:
- 🤖 AI thông minh sử dụng thuật toán Minimax với Alpha-Beta Pruning
- 🌐 Hỗ trợ multiplayer qua mạng LAN/WiFi
- 🎨 Giao diện người dùng trực quan, dễ sử dụng
- ⚡ Xử lý đa luồng hiệu quả, hỗ trợ nhiều người chơi đồng thời
- 🛠️ Các tiện ích hỗ trợ setup và cấu hình dễ dàng

## 📄 License

MIT License
