import customtkinter as ctk
from tkinter import filedialog, messagebox
import os

from crypto_utils import encrypt_file, decrypt_file
from drive_utils import upload_to_drive

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class EncryptorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CyberEncryptor")
        self.geometry("600x300")
        self.resizable(False, False)

        self.selected_file = ""

        self.title_label = ctk.CTkLabel(self, text="🔐 CyberEncryptor", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=20)

        self.file_entry = ctk.CTkEntry(self, width=400, placeholder_text="Файл не вибрано")
        self.file_entry.pack(pady=10)

        self.browse_button = ctk.CTkButton(self, text="🔍 Вибрати файл", command=self.browse_file)
        self.browse_button.pack(pady=5)

        self.encrypt_button = ctk.CTkButton(self, text="🔒 Зашифрувати", command=self.encrypt)
        self.encrypt_button.pack(pady=10)

        self.upload_button = ctk.CTkButton(self, text="завантажити в google drive", command=self.upload)
        self.upload_button.pack(pady=5)

        self.decrypt_button = ctk.CTkButton(self, text="🔓 Розшифрувати", command=self.decrypt)
        self.decrypt_button.pack(pady=5)

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.selected_file = file_path
            self.file_entry.delete(0, ctk.END)
            self.file_entry.insert(0, file_path)

    def encrypt(self):
        if not self.selected_file:
            messagebox.showwarning("Увага", "Будь ласка, виберіть файл для шифрування.")
            return
        try:
            encrypted_path = encrypt_file(self.selected_file)
            messagebox.showinfo("Успіх", f"Файл зашифровано:\n{encrypted_path}")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося зашифрувати файл:\n{str(e)}")

    def decrypt(self):
        if not self.selected_file:
            messagebox.showwarning("Увага", "Будь ласка, виберіть файл для розшифрування.")
            return
        if not self.selected_file.endswith(".enc"):
            messagebox.showwarning("Увага", "Це не зашифрований файл (.enc).")
            return
        try:
            decrypted_path = decrypt_file(self.selected_file)
            messagebox.showinfo("Успіх", f"Файл розшифровано:\n{decrypted_path}")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося розшифрувати файл:\n{str(e)}")

    def upload(self):
        if not self.selected_file:
            messagebox.showwarning("Увага", "Будь ласка, виберіть файл для завантаження.")
            return
        try:
            file_id = upload_to_drive(self.selected_file)
            if file_id:
                messagebox.showinfo("Успіх", f"✅ Файл завантажено в Google Drive!\nID: {file_id}")
            else:
                messagebox.showwarning("Завантажено частково", "Файл завантажено, але ID не повернено.")
        except Exception as e:
            messagebox.showerror("Помилка", f"❌ Не вдалося завантажити файл:\n{str(e)}")