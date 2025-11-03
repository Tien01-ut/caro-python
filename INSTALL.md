# Hướng dẫn cài đặt và chạy Caro Game Python

## Bước 1: Cài đặt Python

Đảm bảo bạn đã cài Python 3.8 hoặc cao hơn:

```bash
python --version
```

## Bước 2: Cài đặt MySQL

1. Tải và cài đặt MySQL Server từ: https://dev.mysql.com/downloads/mysql/
2. Khởi động MySQL service

## Bước 3: Tạo Database

### Cách 1: Sử dụng MySQL Command Line

```bash
mysql -u root -p < setup_database.sql
```

### Cách 2: Sử dụng MySQL Workbench

1. Mở MySQL Workbench
2. Kết nối đến MySQL Server
3. Mở file `setup_database.sql`
4. Chạy script (Execute)

## Bước 4: Cài đặt thư viện Python

```bash
cd caro-python
pip install -r requirements.txt
```

Nếu gặp lỗi, cài từng thư viện:

```bash
pip install mysql-connector-python
```

## Bước 5: Cấu hình kết nối Database

Mở file `server/config.py` và chỉnh sửa:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_MYSQL_PASSWORD',  # Điền mật khẩu MySQL của bạn
    'database': 'caro_game'
}
```

## Bước 6: Chạy Server

Mở terminal/command prompt và chạy:

```bash
cd caro-python/server
python server.py
```

Bạn sẽ thấy:
```
==================================================
Caro Game Server - Python Version
==================================================
Database connection successful
Server started on 0.0.0.0:7777
Server is waiting to accept users...
```

## Bước 7: Chạy Client

Mở terminal/command prompt MỚI (giữ server chạy) và chạy:

```bash
cd caro-python/client
python main.py
```

Giao diện đăng nhập sẽ xuất hiện.

## Bước 8: Chơi game

### Đăng nhập
- Username: `player1`
- Password: `player1`

Hoặc đăng ký tài khoản mới.

### Tạo phòng và chơi
1. Sau khi đăng nhập, nhấn "Tạo phòng"
2. Mở client thứ 2 (chạy lại `python main.py`)
3. Đăng nhập với tài khoản khác
4. Chọn phòng và nhấn "Vào phòng"
5. Bắt đầu chơi!

## Khắc phục sự cố

### Lỗi: "Import mysql.connector could not be resolved"

```bash
pip install mysql-connector-python
```

### Lỗi: "Access denied for user"

Kiểm tra lại username và password MySQL trong `server/config.py`

### Lỗi: "Can't connect to MySQL server"

1. Kiểm tra MySQL service đang chạy
2. Kiểm tra port 3306 không bị chặn

### Lỗi: "Address already in use" (port 7777)

Server đang chạy rồi, hoặc:

```bash
# Windows
netstat -ano | findstr :7777
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:7777 | xargs kill -9
```

## Chế độ phát triển

### Thêm tài khoản test

```sql
INSERT INTO user (username, password, nickname, avatar) 
VALUES ('test', 'test', 'Test Player', 'avatar1');
```

### Reset database

```sql
DROP DATABASE caro_game;
```

Sau đó chạy lại `setup_database.sql`

## Tính năng

✅ Đăng nhập/Đăng ký
✅ Tạo phòng (có/không mật khẩu)
✅ Tham gia phòng
✅ Chơi game Caro 15x15
✅ Chat trong game
✅ Đếm ngược thời gian
✅ Tính điểm thắng/thua
✅ Xếp hạng người chơi
✅ Danh sách phòng real-time

🚧 Đang phát triển:
- Quản lý bạn bè
- Chơi với AI
- Lịch sử đấu
- Replay game

## Liên hệ

Nếu gặp vấn đề, vui lòng tạo issue hoặc liên hệ dev.

Chúc bạn chơi game vui vẻ! 🎮
