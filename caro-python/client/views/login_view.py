"""
Login view for Caro Game Client
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class LoginView:
    """Login window"""
    
    def __init__(self, client):
        self.client = client
        self.window = tk.Tk()
        self.window.title("Đăng nhập - Caro Game")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        
        # Center window
        self.center_window()
        
        # Title
        title = tk.Label(self.window, text="CARO GAME", font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # Username
        tk.Label(self.window, text="Tên đăng nhập:", font=("Arial", 12)).pack(pady=5)
        self.username_entry = tk.Entry(self.window, font=("Arial", 12), width=25)
        self.username_entry.pack(pady=5)
        
        # Password
        tk.Label(self.window, text="Mật khẩu:", font=("Arial", 12)).pack(pady=5)
        self.password_entry = tk.Entry(self.window, font=("Arial", 12), width=25, show="*")
        self.password_entry.pack(pady=5)
        
        # Buttons frame
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=20)
        
        # Login button
        login_btn = tk.Button(button_frame, text="Đăng nhập", font=("Arial", 12),
                             bg="#4CAF50", fg="white", width=12,
                             command=self.login)
        login_btn.pack(side=tk.LEFT, padx=5)
        
        # Register button
        register_btn = tk.Button(button_frame, text="Đăng ký", font=("Arial", 12),
                                bg="#2196F3", fg="white", width=12,
                                command=self.go_to_register)
        register_btn.pack(side=tk.LEFT, padx=5)
        
        # Bind enter key
        self.window.bind('<Return>', lambda e: self.login())
        
        # Focus on username
        self.username_entry.focus()
    
    def center_window(self):
        """Center window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def login(self):
        """Handle login button"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin")
            return
        
        # Send login request to server
        self.client.socket_handle.write(f"client-verify,{username},{password}")
    
    def go_to_register(self):
        """Go to register view"""
        self.window.destroy()
        self.client.open_register_view()
    
    def show_error(self, message):
        """Show error message"""
        messagebox.showerror("Lỗi", message)
    
    def show(self):
        """Show window"""
        self.window.mainloop()
    
    def close(self):
        """Close window"""
        self.window.destroy()
