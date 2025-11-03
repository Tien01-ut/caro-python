-- Create database for Caro Game (MySQL/XAMPP version)
CREATE DATABASE IF NOT EXISTS caro_game;
USE caro_game;

-- User table
CREATE TABLE IF NOT EXISTS `user`(
    ID int AUTO_INCREMENT PRIMARY KEY,
    `username` varchar(255) UNIQUE NOT NULL,
    `password` varchar(255) NOT NULL,
    nickname varchar(255) NOT NULL,
    avatar varchar(255) DEFAULT 'avatar1',
    numberOfGame int DEFAULT 0,
    numberOfWin int DEFAULT 0,
    numberOfDraw int DEFAULT 0,
    IsOnline int DEFAULT 0,
    IsPlaying int DEFAULT 0
);

-- Friend table
CREATE TABLE IF NOT EXISTS friend(
    ID_User1 int NOT NULL,
    ID_User2 int NOT NULL,
    FOREIGN KEY (ID_User1) REFERENCES `user`(ID) ON DELETE CASCADE,
    FOREIGN KEY (ID_User2) REFERENCES `user`(ID) ON DELETE CASCADE,
    CONSTRAINT PK_friend PRIMARY KEY (ID_User1, ID_User2)
);

-- Banned user table
CREATE TABLE IF NOT EXISTS banned_user(
    ID_User int PRIMARY KEY NOT NULL,
    FOREIGN KEY (ID_User) REFERENCES `user`(ID) ON DELETE CASCADE
);

-- Insert some test data
INSERT INTO `user` (username, password, nickname, avatar, numberOfGame, numberOfWin, numberOfDraw) 
VALUES 
    ('player1', 'player1', 'Người chơi 1', 'avatar1', 10, 7, 2),
    ('player2', 'player2', 'Người chơi 2', 'avatar2', 8, 5, 1),
    ('admin', 'admin', 'Admin', 'avatar3', 20, 15, 3)
ON DUPLICATE KEY UPDATE username=username;

-- Add friend relationship
INSERT IGNORE INTO friend (ID_User1, ID_User2) VALUES (1, 2);

SELECT 'Database setup completed successfully!' as Status;
