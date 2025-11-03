# Caro Game Python - Quick Start Guide

## 🚀 Khởi động nhanh (5 phút)

### 1. Setup Database (1 phút)
```bash
mysql -u root -p < setup_database.sql
```

### 2. Config (30 giây)
Mở `server/config.py`, sửa:
```python
'password': 'your_mysql_password_here'
```

### 3. Install Dependencies (1 phút)
```bash
pip install mysql-connector-python
```

### 4. Chạy Server (10 giây)
```bash
cd server
python server.py
```

### 5. Chạy Client (10 giây)
Mở terminal mới:
```bash
cd client
python main.py
```

### 6. Chơi! 🎮
- Đăng ký tài khoản mới hoặc:
- Login: `player1` / `player1`

---

## 📁 Cấu trúc Project

```
caro-python/
├── server/              # Server code
│   ├── server.py       # Main server
│   ├── server_thread.py
│   ├── room.py
│   ├── user_dao.py     # Database
│   └── config.py       # ⚙️ Config here!
├── client/             # Client code  
│   ├── main.py        # Run this!
│   ├── client.py
│   ├── socket_handle.py
│   └── views/         # GUI views
├── shared/            # Shared code
│   ├── models.py
│   └── constants.py
└── setup_database.sql # SQL script
```

---

## 🎮 Cách chơi

1. **Player 1**: Tạo phòng
2. **Player 2**: Vào phòng
3. **Chơi**: Đặt X/O trên bảng 15x15
4. **Thắng**: 5 ô liên tiếp (ngang/dọc/chéo)

---

## 🔧 Troubleshooting

**Lỗi MySQL?**
```bash
pip install mysql-connector-python
```

**Port 7777 đang dùng?**
- Đóng server cũ
- Hoặc đổi port trong `config.py`

**Không kết nối được?**
- Check MySQL đang chạy
- Check username/password trong config

---

## 📚 Đọc thêm

- `README.md` - Tổng quan dự án
- `INSTALL.md` - Hướng dẫn chi tiết
- `setup_database.sql` - Database schema

---

**Converted from Java to Python**
Original: github.com/Duc-ju/caro-game-client

Happy Gaming! 🎉
