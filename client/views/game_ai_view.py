"""
Game view for playing against AI
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os
import threading
import time

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared.constants import INITIAL_BOARD_SIZE, WIN_CONDITION
from ai_player import AIPlayer


class GameAIView:
    """Game window for playing against AI"""
    
    def __init__(self, client, difficulty="medium"):
        self.client = client
        self.difficulty = difficulty
        self.board_size = INITIAL_BOARD_SIZE
        self.ai = AIPlayer(difficulty, self.board_size)
        self.my_turn = True  # Player starts first
        
        # Game state
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.buttons = []
        self.game_over = False
        self.my_score = 0
        self.ai_score = 0
        
        # Create window
        self.window = tk.Tk()
        self.window.title(f"Chơi với AI - Độ khó: {self.get_difficulty_name()}")
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
    
    def get_difficulty_name(self):
        """Get difficulty name in Vietnamese"""
        names = {"easy": "Dễ", "medium": "Trung bình", "hard": "Khó"}
        return names.get(self.difficulty, "Trung bình")
    
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
        
        # Player (me)
        player_frame = tk.Frame(top_frame, bg="#4CAF50", relief=tk.RAISED, bd=2)
        player_frame.pack(side=tk.LEFT, padx=5)
        
        tk.Label(player_frame, text=self.client.user.nickname, font=("Arial", 14, "bold"),
                bg="#4CAF50", fg="white").pack(padx=20, pady=5)
        tk.Label(player_frame, text=f"Thắng: {self.my_score}", font=("Arial", 10),
                bg="#4CAF50", fg="white").pack(padx=20, pady=2)
        self.my_turn_label = tk.Label(player_frame, text="⭐ Lượt của bạn",
                                      font=("Arial", 10, "bold"), bg="#4CAF50", fg="yellow")
        self.my_turn_label.pack(padx=20, pady=2)
        
        # Center info
        center_frame = tk.Frame(top_frame, bg="#f0f0f0")
        center_frame.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        tk.Label(center_frame, text=f"CHƠI VỚI AI", font=("Arial", 16, "bold"),
                bg="#f0f0f0").pack()
        
        self.score_label = tk.Label(center_frame, text=f"Tỉ số: {self.my_score} - {self.ai_score}",
                                    font=("Arial", 14), bg="#f0f0f0")
        self.score_label.pack()
        
        tk.Label(center_frame, text=f"Độ khó: {self.get_difficulty_name()}",
                font=("Arial", 12), bg="#f0f0f0", fg="#666").pack()
        
        # AI
        ai_frame = tk.Frame(top_frame, bg="#FF5722", relief=tk.RAISED, bd=2)
        ai_frame.pack(side=tk.RIGHT, padx=5)
        
        tk.Label(ai_frame, text="🤖 AI", font=("Arial", 14, "bold"),
                bg="#FF5722", fg="white").pack(padx=20, pady=5)
        tk.Label(ai_frame, text=f"Thắng: {self.ai_score}", font=("Arial", 10),
                bg="#FF5722", fg="white").pack(padx=20, pady=2)
        self.ai_turn_label = tk.Label(ai_frame, text="",
                                      font=("Arial", 10, "bold"), bg="#FF5722", fg="yellow")
        self.ai_turn_label.pack(padx=20, pady=2)
    
    def create_game_board(self):
        """Create simple game board (no scrollbars)"""
        # Container frame
        container = tk.Frame(self.window, bg="white")
        container.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Create frame for board
        board_frame = tk.Frame(container, bg="white")
        board_frame.pack(expand=True)
        
        # Create board buttons
        for i in range(self.board_size):
            row = []
            for j in range(self.board_size):
                btn = tk.Button(board_frame, text="", width=3, height=1,
                              font=("Arial", 14, "bold"), bg="white",
                              relief=tk.RAISED, bd=1,
                              command=lambda x=i, y=j: self.make_move(x, y))
                btn.grid(row=i, column=j, padx=0, pady=0)
                row.append(btn)
            self.buttons.append(row)
    
    def create_bottom_controls(self):
        """Create bottom control panel"""
        bottom_frame = tk.Frame(self.window)
        bottom_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Buttons
        tk.Button(bottom_frame, text="🔄 Chơi lại", font=("Arial", 11),
                 bg="#4CAF50", fg="white", width=15,
                 command=self.new_game).pack(side=tk.LEFT, padx=5)
        
        tk.Button(bottom_frame, text="⚙️ Đổi độ khó", font=("Arial", 11),
                 bg="#2196F3", fg="white", width=15,
                 command=self.change_difficulty).pack(side=tk.LEFT, padx=5)
        
        tk.Button(bottom_frame, text="🏠 Về trang chủ", font=("Arial", 11),
                 bg="#FF9800", fg="white", width=15,
                 command=self.go_home).pack(side=tk.LEFT, padx=5)
        
        tk.Button(bottom_frame, text="🚪 Thoát", font=("Arial", 11),
                 bg="#f44336", fg="white", width=15,
                 command=self.on_closing).pack(side=tk.RIGHT, padx=5)
    
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
        self.board[x][y] = 1  # 1 for player
        self.buttons[x][y].config(text="X", bg="#4CAF50", fg="white", state=tk.DISABLED)
        
        # Check win
        if self.check_win(x, y, 1):
            self.on_win()
            return
        
        # Check draw
        if self.is_board_full():
            self.on_draw()
            return
        
        # Switch turn to AI
        self.my_turn = False
        self.update_turn_display()
        
        # AI makes move after short delay
        self.window.after(200, self.ai_make_move)
    
    def ai_make_move(self):
        """AI makes a move"""
        if self.game_over:
            return
        
        # Get AI move
        move = self.ai.get_move(self.board)
        
        if move:
            x, y = move
            self.board[x][y] = 2  # 2 for AI
            self.buttons[x][y].config(text="O", bg="#FF5722", fg="white", state=tk.DISABLED)
            
            # Check if AI wins
            if self.check_win(x, y, 2):
                self.on_lose()
                return
            
            # Check draw
            if self.is_board_full():
                self.on_draw()
                return
            
            # Switch turn back to player
            self.my_turn = True
            self.update_turn_display()
    
    def check_win(self, x, y, symbol):
        """Check if the move at (x, y) wins the game"""
        # Check horizontal
        count = 1
        # Left
        j = y - 1
        while j >= 0 and self.board[x][j] == symbol:
            count += 1
            j -= 1
        # Right
        j = y + 1
        while j < self.board_size and self.board[x][j] == symbol:
            count += 1
            j += 1
        if count >= WIN_CONDITION:
            return True
        
        # Check vertical
        count = 1
        # Up
        i = x - 1
        while i >= 0 and self.board[i][y] == symbol:
            count += 1
            i -= 1
        # Down
        i = x + 1
        while i < self.board_size and self.board[i][y] == symbol:
            count += 1
            i += 1
        if count >= WIN_CONDITION:
            return True
        
        # Check diagonal (top-left to bottom-right)
        count = 1
        # Top-left
        i, j = x - 1, y - 1
        while i >= 0 and j >= 0 and self.board[i][j] == symbol:
            count += 1
            i -= 1
            j -= 1
        # Bottom-right
        i, j = x + 1, y + 1
        while i < self.board_size and j < self.board_size and self.board[i][j] == symbol:
            count += 1
            i += 1
            j += 1
        if count >= WIN_CONDITION:
            return True
        
        # Check diagonal (top-right to bottom-left)
        count = 1
        # Top-right
        i, j = x - 1, y + 1
        while i >= 0 and j < self.board_size and self.board[i][j] == symbol:
            count += 1
            i -= 1
            j += 1
        # Bottom-left
        i, j = x + 1, y - 1
        while i < self.board_size and j >= 0 and self.board[i][j] == symbol:
            count += 1
            i += 1
            j -= 1
        if count >= WIN_CONDITION:
            return True
        
        return False
    
    def is_board_full(self):
        """Check if board is full"""
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == 0:
                    return False
        return True
    
    def update_turn_display(self):
        """Update turn indicator"""
        if self.my_turn:
            self.my_turn_label.config(text="⭐ Lượt của bạn")
            self.ai_turn_label.config(text="")
        else:
            self.my_turn_label.config(text="")
            self.ai_turn_label.config(text="⭐ AI đang suy nghĩ...")
    
    def on_win(self):
        """Handle player win"""
        self.game_over = True
        self.my_score += 1
        self.score_label.config(text=f"Tỉ số: {self.my_score} - {self.ai_score}")
        # Hỏi chơi lại ngay
        result = messagebox.askyesno("Chúc mừng!", 
                                     f"🎉 Bạn đã thắng!\n\nTỉ số hiện tại: {self.my_score} - {self.ai_score}\n\nBạn có muốn chơi ván mới không?")
        if result:
            self.new_game()
        else:
            self.go_home()
    
    def on_lose(self):
        """Handle player lose"""
        self.game_over = True
        self.ai_score += 1
        self.score_label.config(text=f"Tỉ số: {self.my_score} - {self.ai_score}")
        # Hỏi chơi lại ngay
        result = messagebox.askyesno("Tiếc quá!", 
                                     f"😢 AI đã thắng!\n\nTỉ số hiện tại: {self.my_score} - {self.ai_score}\n\nBạn có muốn chơi ván mới không?")
        if result:
            self.new_game()
        else:
            self.go_home()
    
    def on_draw(self):
        """Handle draw"""
        self.game_over = True
        # Hỏi chơi lại ngay
        result = messagebox.askyesno("Hòa!", 
                                     f"🤝 Ván đấu hòa!\n\nTỉ số hiện tại: {self.my_score} - {self.ai_score}\n\nBạn có muốn chơi ván mới không?")
        if result:
            self.new_game()
        else:
            self.go_home()
    
    def new_game(self):
        """Start new game"""
        self.game_over = False
        self.my_turn = True
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        
        # Reset buttons
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.buttons[i][j].config(text="", bg="white", state=tk.NORMAL)
        
        self.update_turn_display()
    
    def change_difficulty(self):
        """Change AI difficulty"""
        difficulty_window = tk.Toplevel(self.window)
        difficulty_window.title("Chọn độ khó")
        difficulty_window.geometry("300x200")
        difficulty_window.resizable(False, False)
        
        # Center window
        x = self.window.winfo_x() + (self.window.winfo_width() // 2) - 150
        y = self.window.winfo_y() + (self.window.winfo_height() // 2) - 100
        difficulty_window.geometry(f"300x200+{x}+{y}")
        
        tk.Label(difficulty_window, text="Chọn độ khó:", font=("Arial", 14, "bold")).pack(pady=20)
        
        def select_difficulty(level):
            self.difficulty = level
            self.ai = AIPlayer(level)
            self.window.title(f"Chơi với AI - Độ khó: {self.get_difficulty_name()}")
            difficulty_window.destroy()
            self.new_game()
        
        tk.Button(difficulty_window, text="😊 Dễ", font=("Arial", 12),
                 bg="#4CAF50", fg="white", width=20,
                 command=lambda: select_difficulty("easy")).pack(pady=5)
        
        tk.Button(difficulty_window, text="😐 Trung bình", font=("Arial", 12),
                 bg="#FF9800", fg="white", width=20,
                 command=lambda: select_difficulty("medium")).pack(pady=5)
        
        tk.Button(difficulty_window, text="😤 Khó", font=("Arial", 12),
                 bg="#f44336", fg="white", width=20,
                 command=lambda: select_difficulty("hard")).pack(pady=5)
    
    def go_home(self):
        """Return to home page"""
        self.window.withdraw()
        self.client.open_home_view()
    
    def on_closing(self):
        """Handle window close"""
        if messagebox.askokcancel("Thoát", "Bạn có chắc muốn thoát?"):
            self.window.destroy()
            self.client.open_home_view()
    
    def show(self):
        """Show window"""
        self.window.deiconify()
        self.window.mainloop()
