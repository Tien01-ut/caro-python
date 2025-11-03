"""
Script tự động tạo database cho Caro Game
"""

import mysql.connector
from mysql.connector import Error

def create_database():
    """Tạo database và tables tự động"""
    try:
        # Kết nối MySQL (không cần database)
        print("Đang kết nối MySQL...")
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''  # XAMPP mặc định không có password
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            print("✅ Kết nối MySQL thành công!")
            
            # Tạo database
            print("\n1. Đang tạo database 'caro_game'...")
            cursor.execute("CREATE DATABASE IF NOT EXISTS caro_game")
            print("✅ Database 'caro_game' đã tạo!")
            
            # Chọn database
            cursor.execute("USE caro_game")
            
            # Tạo bảng user
            print("\n2. Đang tạo bảng 'user'...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS `user`(
                    ID int AUTO_INCREMENT PRIMARY KEY,
                    username varchar(255) UNIQUE NOT NULL,
                    password varchar(255) NOT NULL,
                    nickname varchar(255) NOT NULL,
                    avatar varchar(255) DEFAULT 'avatar1',
                    numberOfGame int DEFAULT 0,
                    numberOfWin int DEFAULT 0,
                    numberOfDraw int DEFAULT 0,
                    IsOnline int DEFAULT 0,
                    IsPlaying int DEFAULT 0
                )
            """)
            print("✅ Bảng 'user' đã tạo!")
            
            # Tạo bảng friend
            print("\n3. Đang tạo bảng 'friend'...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS friend(
                    ID_User1 int NOT NULL,
                    ID_User2 int NOT NULL,
                    FOREIGN KEY (ID_User1) REFERENCES `user`(ID),
                    FOREIGN KEY (ID_User2) REFERENCES `user`(ID),
                    CONSTRAINT PK_friend PRIMARY KEY (ID_User1, ID_User2)
                )
            """)
            print("✅ Bảng 'friend' đã tạo!")
            
            # Tạo bảng banned_user
            print("\n4. Đang tạo bảng 'banned_user'...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS banned_user(
                    ID_User int PRIMARY KEY NOT NULL,
                    FOREIGN KEY (ID_User) REFERENCES `user`(ID)
                )
            """)
            print("✅ Bảng 'banned_user' đã tạo!")
            
            # Thêm dữ liệu mẫu
            print("\n5. Đang thêm dữ liệu mẫu...")
            try:
                cursor.execute("""
                    INSERT INTO `user` (username, password, nickname, avatar, numberOfGame, numberOfWin, numberOfDraw) 
                    VALUES 
                        ('player1', 'player1', 'Nguoi choi 1', 'avatar1', 10, 7, 2),
                        ('player2', 'player2', 'Nguoi choi 2', 'avatar2', 8, 5, 1),
                        ('admin', 'admin', 'Admin', 'avatar3', 20, 15, 3)
                """)
                connection.commit()
                print("✅ Dữ liệu mẫu đã thêm!")
            except Error as e:
                if "Duplicate entry" in str(e):
                    print("⚠️ Dữ liệu mẫu đã tồn tại, bỏ qua...")
                else:
                    raise e
            
            # Kiểm tra
            print("\n6. Kiểm tra dữ liệu...")
            cursor.execute("SELECT COUNT(*) FROM `user`")
            count = cursor.fetchone()[0]
            print(f"✅ Có {count} user trong database!")
            
            cursor.execute("SELECT username, nickname FROM `user`")
            users = cursor.fetchall()
            print("\nDanh sách users:")
            for user in users:
                print(f"  - {user[0]} ({user[1]})")
            
            cursor.close()
            connection.close()
            
            print("\n" + "="*50)
            print("🎉 HOÀN THÀNH! Database đã sẵn sàng!")
            print("="*50)
            print("\n📝 Bạn có thể đăng nhập với:")
            print("   Username: player1")
            print("   Password: player1")
            print("\nHoặc đăng ký tài khoản mới!")
            
    except Error as e:
        print(f"\n❌ LỖI: {e}")
        print("\n💡 Kiểm tra:")
        print("   1. XAMPP đã bật MySQL chưa?")
        print("   2. MySQL đang chạy trên port 3306?")

if __name__ == "__main__":
    print("="*50)
    print("CARO GAME - TỰ ĐỘNG TẠO DATABASE")
    print("="*50)
    create_database()
