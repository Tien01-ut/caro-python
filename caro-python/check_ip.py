"""
Script tiện ích để kiểm tra IP của máy tính
"""

import socket
import platform

def get_local_ip():
    """Lấy địa chỉ IP của máy"""
    try:
        # Tạo socket để lấy IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "Không lấy được IP"

def main():
    print("=" * 60)
    print("🌐 THÔNG TIN KẾT NỐI MẠNG")
    print("=" * 60)
    print()
    
    # Thông tin máy
    print(f"Tên máy tính: {platform.node()}")
    print(f"Hệ điều hành: {platform.system()} {platform.release()}")
    print()
    
    # Địa chỉ IP
    ip = get_local_ip()
    print(f"📍 Địa chỉ IP của máy: {ip}")
    print()
    
    print("=" * 60)
    print("📝 HƯỚNG DẪN:")
    print("=" * 60)
    print()
    print("🖥️  Nếu máy này chạy SERVER:")
    print(f"    → Giữ nguyên, không cần làm gì")
    print()
    print("💻 Nếu máy này chạy CLIENT (kết nối đến máy khác):")
    print(f"    1. Mở file: network_config.py")
    print(f"    2. Tìm dòng: SERVER_IP = \"127.0.0.1\"")
    print(f"    3. Thay bằng: SERVER_IP = \"[IP của máy chạy server]\"")
    print(f"    4. Lưu file và chạy client")
    print()
    print("⚠️  Lưu ý:")
    print("    - 2 máy phải cùng mạng WiFi/LAN")
    print("    - Tắt Firewall hoặc cho phép port 7777")
    print()
    print("=" * 60)

if __name__ == "__main__":
    main()
    input("\nNhấn Enter để thoát...")
