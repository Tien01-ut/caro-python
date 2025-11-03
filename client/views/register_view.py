"""
Register view for Caro Game Client
"""

import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared.constants import AVATARS


class RegisterView:
    """Registration window"""
    
    def __init__(self, client):
        self.client = client
        self.window = tk.Tk()
        self.window.title("Đăng ký - Caro Game")
        self.window.geometry("450x550")
        self.window.resizable(False, False)
        
        # Center window
        self.center_window()
        
        # Title
        title = tk.Label(self.window, text="ĐĂNG KÝ TÀI KHOẢN", font=("Arial", 18, "bold"))
        title.pack(pady=15)
        
        # Username
        tk.Label(self.window, text="Tên đăng nhập:", font=("Arial", 11)).pack(pady=3)
        self.username_entry = tk.Entry(self.window, font=("Arial", 11), width=25)
        self.username_entry.pack(pady=3)
        
        # Password
        tk.Label(self.window, text="Mật khẩu:", font=("Arial", 11)).pack(pady=3)
        self.password_entry = tk.Entry(self.window, font=("Arial", 11), width=25, show="*")
        self.password_entry.pack(pady=3)
        
        # Confirm password
        tk.Label(self.window, text="Xác nhận mật khẩu:", font=("Arial", 11)).pack(pady=3)
        self.confirm_password_entry = tk.Entry(self.window, font=("Arial", 11), width=25, show="*")
        self.confirm_password_entry.pack(pady=3)
        
        # Nickname
        tk.Label(self.window, text="Biệt danh:", font=("Arial", 11)).pack(pady=3)
        self.nickname_entry = tk.Entry(self.window, font=("Arial", 11), width=25)
        self.nickname_entry.pack(pady=3)
        
        # Avatar selection
        tk.Label(self.window, text="Chọn avatar:", font=("Arial", 11)).pack(pady=3)
        self.avatar_var = tk.StringVar(value=AVATARS[0])
        avatar_combo = ttk.Combobox(self.window, textvariable=self.avatar_var,
                                    values=AVATARS, state="readonly", width=23)
        avatar_combo.pack(pady=3)
        
        # Buttons frame
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=15)
        
        # Register button
        register_btn = tk.Button(button_frame, text="Đăng ký", font=("Arial", 11),
                                bg="#4CAF50", fg="white", width=12,
                                command=self.register)
        register_btn.pack(side=tk.LEFT, padx=5)
        
        # Back button
        back_btn = tk.Button(button_frame, text="Quay lại", font=("Arial", 11),
                           bg="#f44336", fg="white", width=12,
                           command=self.go_back)
        back_btn.pack(side=tk.LEFT, padx=5)
        
        # Bind enter key
        self.window.bind('<Return>', lambda e: self.register())
        
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
    
    def register(self):
        """Handle register button"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm = self.confirm_password_entry.get().strip()
        nickname = self.nickname_entry.get().strip()
        avatar = self.avatar_var.get()
        
        # Validation
        if not username or not password or not nickname:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin")
            return
        
        if len(username) < 4:
            messagebox.showwarning("Cảnh báo", "Tên đăng nhập phải có ít nhất 4 ký tự")
            return
        
        if len(password) < 4:
            messagebox.showwarning("Cảnh báo", "Mật khẩu phải có ít nhất 4 ký tự")
            return
        
        if password != confirm:
            messagebox.showwarning("Cảnh báo", "Mật khẩu xác nhận không khớp")
            return
        
        # Send register request to server
        self.client.socket_handle.write(f"register,{username},{password},{nickname},{avatar}")
    
    def go_back(self):
        """Go back to login"""
        self.window.destroy()
        self.client.open_login_view()
    
    def show_error(self, message):
        """Show error message"""
        messagebox.showerror("Lỗi", message)
    
    def show(self):
        """Show window"""
        self.window.mainloop()
    
    def close(self):
        """Close window"""
        self.window.destroy()
