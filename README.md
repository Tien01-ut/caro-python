# Caro Game - Python Version

Game Caro (Tic-Tac-Toe) multiplayer với kiến trúc client-server, được chuyển đổi từ Java sang Python.

## Tính năng

### Server
- Xử lý đa luồng với nhiều client đồng thời
- Quản lý phòng chơi
- Hệ thống đăng nhập/đăng ký
- Quản lý bạn bè
- Bảng xếp hạng
- Lưu trữ dữ liệu với MySQL

### Client
- Giao diện đồ họa với Tkinter
- Đăng nhập/Đăng ký
- Tạo và tham gia phòng
- Chơi game Caro 15x15
- Chat với người chơi khác
- Xem bảng xếp hạng
- Quản lý danh sách bạn bè
- Chơi với AI (chế độ đơn)

## Yêu cầu

- Python 3.8+
- MySQL 8.0+ (XAMPP hoặc standalone)
- Các thư viện Python (xem requirements.txt)

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
├── server/
│   ├── server.py           # Server chính
│   ├── server_thread.py    # Xử lý client
│   ├── room.py            # Quản lý phòng chơi
│   ├── user_dao.py        # Truy vấn database
│   ├── config.py          # Cấu hình
│   └── admin_gui.py       # Giao diện quản trị
├── client/
│   ├── main.py            # Entry point
│   ├── client.py          # Client logic
│   ├── socket_handle.py   # Xử lý socket
│   └── views/
│       ├── login_view.py
│       ├── register_view.py
│       ├── home_view.py
│       ├── game_view.py
│       └── ...
├── shared/
│   ├── models.py          # Data models
│   └── constants.py       # Hằng số chung
├── assets/                # Hình ảnh, icon
└── requirements.txt       # Dependencies

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

## Tác giả

Chuyển đổi từ Java sang Python
Original Java version: https://github.com/Duc-ju/caro-game-client

## License

MIT License
