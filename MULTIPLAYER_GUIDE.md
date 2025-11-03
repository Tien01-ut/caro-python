# 🎮 HƯỚNG DẪN CHƠI TRÊN 2 MÁY

## 📋 Chuẩn bị:
- 2 máy tính có Python đã cài đặt
- 2 máy cùng mạng WiFi/LAN
- Code game đã copy sang cả 2 máy

---

## 🖥️ MÁY 1 (Chạy Server + Client)

### Bước 1: Kiểm tra IP
```bash
python check_ip.py
```
→ Ghi nhớ địa chỉ IP (ví dụ: **192.168.1.100**)

### Bước 2: Khởi động Server
```bash
python server/server.py
```
→ Server chạy và chờ kết nối

### Bước 3: Khởi động Client (tùy chọn)
Mở terminal mới:
```bash
python client/main.py
```
→ Đăng nhập và tạo phòng

---

## 💻 MÁY 2 (Chạy Client)

### Bước 1: Cấu hình IP
Mở file **`network_config.py`** và sửa:
```python
SERVER_IP = "192.168.1.100"  # ← Thay bằng IP của Máy 1
```
Lưu file.

### Bước 2: Khởi động Client
```bash
python client/main.py
```
→ Đăng nhập và vào phòng

---

## ⚠️ LƯU Ý QUAN TRỌNG

### 1. Firewall
Nếu không kết nối được:
- **Windows:** Tắt Windows Defender Firewall tạm thời
- Hoặc cho phép port 7777:
  - Control Panel → Windows Defender Firewall
  - Advanced Settings → Inbound Rules → New Rule
  - Port → TCP → 7777 → Allow

### 2. Kiểm tra kết nối
Ping từ Máy 2 đến Máy 1:
```bash
ping 192.168.1.100
```
→ Nếu thành công mới tiếp tục

### 3. Mạng
- ✅ Cùng WiFi: OK
- ✅ Cùng LAN: OK  
- ❌ Khác WiFi: KHÔNG được
- ❌ 4G/5G: KHÔNG được

---

## 🎯 CÁCH CHƠI

### Máy 1 (Player 1):
1. Đăng nhập
2. Nhấn "Tạo phòng"
3. Đặt tên phòng
4. Chờ đối thủ vào

### Máy 2 (Player 2):
1. Đăng nhập (tài khoản khác)
2. Thấy phòng trong danh sách
3. Chọn phòng → Nhấn "Vào phòng"
4. Game bắt đầu!

---

## 🆘 XỬ LÝ LỖI

### Lỗi: "Can't connect to server"
- ✅ Kiểm tra IP trong `network_config.py`
- ✅ Kiểm tra Server đã chạy chưa
- ✅ Kiểm tra Firewall
- ✅ Ping thử IP

### Lỗi: "Connection timeout"
- ✅ 2 máy có cùng mạng không?
- ✅ Server có đang chạy không?

### Lỗi: Database
- ✅ Chỉ máy chạy Server cần MySQL
- ✅ Máy Client KHÔNG cần MySQL

---

## 📞 Liên hệ hỗ trợ
Nếu vẫn gặp vấn đề, check lại:
1. `python check_ip.py` - Xem IP đúng chưa
2. `network_config.py` - Đã sửa IP chưa
3. Firewall - Đã tắt hoặc cho phép port 7777 chưa

Chúc chơi game vui vẻ! 🎉
