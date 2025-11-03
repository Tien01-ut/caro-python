"""
Game view for playing Caro
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared.constants import BOARD_SIZE, WIN_CONDITION, GAME_TIMEOUT

class GameView:
    """Game playing window"""
    
    def __init__(self, client, room_id, competitor, is_host, competitor_ip):
        self.client = client
        self.room_id = room_id
        self.competitor = competitor
        self.is_host = is_host
        self.competitor_ip = competitor_ip
        self.my_turn = is_host  # Host starts first
        
        # Game state
        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.buttons = []
        self.game_over = False
        self.timer_seconds = GAME_TIMEOUT
        self.my_score = 0
        self.competitor_score = 0
        
        # Create window
        self.window = tk.Tk()
        self.window.title(f"Phòng {room_id} - Caro Game")
        self.window.geometry("900x700")
        self.window.resizable(False, False)
        
        # Center window
        self.center_window()
        
        # Create UI
        self.create_top_info()
        self.create_game_board()
        self.create_bottom_controls()
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Start timer if it's my turn
        if self.my_turn:
            self.start_timer()
    
    def center_window(self):
        """Center window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_top_info(self):
        """Create top info panel"""
        top_frame = tk.Frame(self.window, bg="#f0f0f0")
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Player 1 (me)
        player1_frame = tk.Frame(top_frame, bg="#4CAF50", relief=tk.RAISED, bd=2)
        player1_frame.pack(side=tk.LEFT, padx=5)
        
        tk.Label(player1_frame, text=self.client.user.nickname, font=("Arial", 14, "bold"),
                bg="#4CAF50", fg="white").pack(padx=20, pady=5)
        tk.Label(player1_frame, text=f"Thắng: {self.my_score}", font=("Arial", 10),
                bg="#4CAF50", fg="white").pack(padx=20, pady=2)
        self.my_turn_label = tk.Label(player1_frame, text="⭐ Lượt của bạn" if self.my_turn else "",
                                      font=("Arial", 10, "bold"), bg="#4CAF50", fg="yellow")
        self.my_turn_label.pack(padx=20, pady=2)
        
        # Center info
        center_frame = tk.Frame(top_frame, bg="#f0f0f0")
        center_frame.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        tk.Label(center_frame, text=f"PHÒNG {self.room_id}", font=("Arial", 16, "bold"),
                bg="#f0f0f0").pack()
        
        self.score_label = tk.Label(center_frame, text=f"Tỉ số: {self.my_score} - {self.competitor_score}",
                                    font=("Arial", 14), bg="#f0f0f0")
        self.score_label.pack()
        
        self.timer_label = tk.Label(center_frame, text=f"Thời gian: {self.timer_seconds}s",
                                    font=("Arial", 12), bg="#f0f0f0", fg="red")
        self.timer_label.pack()
        
        # Player 2 (competitor)
        player2_frame = tk.Frame(top_frame, bg="#2196F3", relief=tk.RAISED, bd=2)
        player2_frame.pack(side=tk.RIGHT, padx=5)
        
        tk.Label(player2_frame, text=self.competitor.nickname, font=("Arial", 14, "bold"),
                bg="#2196F3", fg="white").pack(padx=20, pady=5)
        tk.Label(player2_frame, text=f"Thắng: {self.competitor_score}", font=("Arial", 10),
                bg="#2196F3", fg="white").pack(padx=20, pady=2)
        self.competitor_turn_label = tk.Label(player2_frame, text="" if self.my_turn else "⭐ Lượt đối thủ",
                                             font=("Arial", 10, "bold"), bg="#2196F3", fg="yellow")
        self.competitor_turn_label.pack(padx=20, pady=2)
    
    def create_game_board(self):
        """Create game board"""
        board_frame = tk.Frame(self.window, bg="white")
        board_frame.pack(padx=10, pady=10)
        
        # Create buttons for board
        for i in range(BOARD_SIZE):
            row = []
            for j in range(BOARD_SIZE):
                btn = tk.Button(board_frame, text="", width=2, height=1,
                              font=("Arial", 16, "bold"), bg="white",
                              relief=tk.RAISED, bd=2,
                              command=lambda x=i, y=j: self.make_move(x, y))
                btn.grid(row=i, column=j, padx=1, pady=1, sticky="nsew")
                row.append(btn)
            self.buttons.append(row)
        
        # Make grid cells expand uniformly
        for i in range(BOARD_SIZE):
            board_frame.grid_rowconfigure(i, weight=1, uniform="row")
            board_frame.grid_columnconfigure(i, weight=1, uniform="col")
    
    def create_bottom_controls(self):
        """Create bottom control panel"""
        bottom_frame = tk.Frame(self.window)
        bottom_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Buttons
        tk.Button(bottom_frame, text="🤝 Xin hòa", font=("Arial", 11),
                 bg="#FF9800", fg="white", width=12,
                 command=self.request_draw).pack(side=tk.LEFT, padx=5)
        
        tk.Button(bottom_frame, text="🔄 Chơi lại", font=("Arial", 11),
                 bg="#9C27B0", fg="white", width=12,
                 command=self.request_revenge).pack(side=tk.LEFT, padx=5)
        
        tk.Button(bottom_frame, text="🚪 Rời phòng", font=("Arial", 11),
                 bg="#f44336", fg="white", width=12,
                 command=self.leave_room).pack(side=tk.LEFT, padx=5)
        
        # Chat
        chat_frame = tk.Frame(bottom_frame)
        chat_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(20, 0))
        
        self.chat_entry = tk.Entry(chat_frame, font=("Arial", 11))
        self.chat_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.chat_entry.bind('<Return>', lambda e: self.send_chat())
        
        tk.Button(chat_frame, text="Gửi", font=("Arial", 11),
                 command=self.send_chat).pack(side=tk.RIGHT, padx=(5, 0))
    
    def make_move(self, x, y):
        """Handle player move"""
        if self.game_over:
            messagebox.showinfo("Thông báo", "Ván đấu đã kết thúc")
            return
        
        if not self.my_turn:
            messagebox.showwarning("Cảnh báo", "Chưa đến lượt của bạn")
            return
        
        if self.board[x][y] != 0:
            messagebox.showwarning("Cảnh báo", "Ô này đã được đánh")
            return
        
        # Make move
        self.board[x][y] = 1  # 1 for player, 2 for competitor
        self.buttons[x][y].config(text="X", bg="#4CAF50", fg="white", state=tk.DISABLED)
        
        # Send move to server
        self.client.socket_handle.write(f"user-move,{x},{y}")
        
        # Check win
        if self.check_win(x, y, 1):
            self.on_win()
            return
        
        # Check draw (board full)
        if self.is_board_full():
            self.on_draw()
            return
        
        # Switch turn
        self.my_turn = False
        self.update_turn_display()
        self.stop_timer()
    
    def on_competitor_move(self, x, y):
        """Handle competitor move"""
        self.board[x][y] = 2
        self.buttons[x][y].config(text="O", bg="#2196F3", fg="white", state=tk.DISABLED)
        
        # Check if competitor wins
        if self.check_win(x, y, 2):
            self.on_lose()
            return
        
        # Check draw
        if self.is_board_full():
            self.on_draw()
            return
        
        # My turn now
        self.my_turn = True
        self.update_turn_display()
        self.start_timer()
    
    def check_win(self, x, y, player):
        """Check if player wins at position (x, y)"""
        # Check 4 directions: horizontal, vertical, diagonal, anti-diagonal
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dx, dy in directions:
            count = 1
            
            # Check positive direction
            i, j = x + dx, y + dy
            while 0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE and self.board[i][j] == player:
                count += 1
                i += dx
                j += dy
            
            # Check negative direction
            i, j = x - dx, y - dy
            while 0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE and self.board[i][j] == player:
                count += 1
                i -= dx
                j -= dy
            
            if count >= WIN_CONDITION:
                return True
        
        return False
    
    def is_board_full(self):
        """Check if board is full"""
        for row in self.board:
            if 0 in row:
                return False
        return True
    
    def on_win(self):
        """Handle win"""
        self.game_over = True
        self.stop_timer()
        self.my_score += 1
        self.update_score_display()
        self.client.socket_handle.write("win,")
        messagebox.showinfo("Chúc mừng!", "Bạn đã thắng!")
    
    def on_lose(self):
        """Handle lose"""
        self.game_over = True
        self.stop_timer()
        self.competitor_score += 1
        self.update_score_display()
        messagebox.showinfo("Tiếc quá!", "Bạn đã thua")
    
    def on_draw(self):
        """Handle draw"""
        self.game_over = True
        self.stop_timer()
        messagebox.showinfo("Hòa!", "Ván đấu hòa")
    
    def update_turn_display(self):
        """Update turn indicators"""
        if self.my_turn:
            self.my_turn_label.config(text="⭐ Lượt của bạn")
            self.competitor_turn_label.config(text="")
        else:
            self.my_turn_label.config(text="")
            self.competitor_turn_label.config(text="⭐ Lượt đối thủ")
    
    def update_score_display(self):
        """Update score display"""
        self.score_label.config(text=f"Tỉ số: {self.my_score} - {self.competitor_score}")
    
    def start_timer(self):
        """Start countdown timer"""
        self.timer_seconds = GAME_TIMEOUT
        self.update_timer()
    
    def stop_timer(self):
        """Stop timer"""
        pass  # Timer will stop when turn changes
    
    def update_timer(self):
        """Update timer display"""
        if self.my_turn and not self.game_over:
            self.timer_label.config(text=f"Thời gian: {self.timer_seconds}s")
            
            if self.timer_seconds > 0:
                self.timer_seconds -= 1
                self.window.after(1000, self.update_timer)
            else:
                # Timeout - lose
                messagebox.showwarning("Hết giờ!", "Bạn đã hết thời gian")
                self.client.socket_handle.write("lose,")
                self.on_lose()
    
    def request_draw(self):
        """Request draw"""
        if self.game_over:
            messagebox.showinfo("Thông báo", "Ván đấu đã kết thúc")
            return
        
        self.client.socket_handle.write("draw-request,")
        messagebox.showinfo("Thông báo", "Đã gửi yêu cầu hòa đến đối thủ")
    
    def request_revenge(self):
        """Request revenge (play again)"""
        if not self.game_over:
            messagebox.showinfo("Thông báo", "Ván đấu chưa kết thúc")
            return
        
        self.client.socket_handle.write("ask-for-revenge,")
        messagebox.showinfo("Thông báo", "Đã gửi yêu cầu chơi lại đến đối thủ")
    
    def leave_room(self):
        """Leave room"""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn rời phòng?"):
            self.client.socket_handle.write("leave-room,")
            self.window.destroy()
            self.client.open_home_view()
    
    def send_chat(self):
        """Send chat message"""
        message = self.chat_entry.get().strip()
        if message:
            self.client.socket_handle.write(f"send-message,{message}")
            self.chat_entry.delete(0, tk.END)
    
    def on_receive_message(self, message):
        """Display received chat message"""
        messagebox.showinfo("Tin nhắn", f"{self.competitor.nickname}: {message}")
    
    def on_closing(self):
        """Handle window close"""
        self.leave_room()
    
    def show(self):
        """Show window"""
        # Don't call mainloop - it's already running
    
    def close(self):
        """Close window"""
        self.window.destroy()
