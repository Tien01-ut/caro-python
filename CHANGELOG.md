# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2025-11-03

### Added
- 🤖 **AI Player** với thuật toán Minimax và Alpha-Beta Pruning
  - 3 độ khó: Dễ, Trung bình, Khó
  - AI thông minh biết tấn công và phòng thủ
  - Tối ưu tốc độ với giới hạn nước đi và kiểm tra nhanh
- 🌐 **Multiplayer qua mạng LAN/WiFi**
  - File `network_config.py` dễ cấu hình
  - Script `check_ip.py` để kiểm tra IP
  - Hướng dẫn chi tiết trong `MULTIPLAYER_GUIDE.md`
- 📚 **Tài liệu đầy đủ**
  - `README.md` - Tài liệu chính
  - `QUICKSTART.md` - Hướng dẫn nhanh 5 phút
  - `INSTALL.md` - Hướng dẫn cài đặt chi tiết
  - `MULTIPLAYER_GUIDE.md` - Hướng dẫn chơi 2 máy
- 🛠️ **Tiện ích**
  - `create_database.py` - Tự động tạo database
  - `.gitignore` - Quản lý Git tốt hơn

### Changed
- ⚡ Tối ưu hiệu suất AI (giảm thời gian suy nghĩ từ ~60s xuống ~2s)
- 🎨 Cải thiện giao diện game board
  - Kích thước nút cố định, không bị nở ra khi click
  - Font size thống nhất
  - Grid layout đều đặn
- 🔧 Sửa lỗi threading với Tkinter
  - Implement Queue-based message processing
  - Tránh lỗi "main thread is not in main loop"
- 📝 Cập nhật cấu trúc dự án trong README

### Fixed
- ✅ Lỗi import modules trong server
- ✅ Lỗi window management (destroy vs withdraw)
- ✅ Lỗi multiple mainloop calls
- ✅ Lỗi register form bị cắt (tăng size từ 400x450 lên 450x550)
- ✅ Lỗi database connection (hướng dẫn dùng 127.0.0.1 thay vì localhost)

## [1.0.0] - Original

### Added
- Server-client architecture
- Basic multiplayer gameplay
- User authentication
- Room management
- MySQL database integration
- Tkinter GUI

---

## Roadmap

### [Future]
- [ ] Friend system (đang phát triển)
- [ ] Private messaging
- [ ] Tournament mode
- [ ] Game replay/recording
- [ ] Sound effects
- [ ] Custom avatars
- [ ] Mobile version (?)
