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

        self.title_label = ctk.CTkLabel(self, text="CyberEncryptor", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=20)

        self.file_entry = ctk.CTkEntry(self, width=400, placeholder_text="Nie wybrano pliku")
        self.file_entry.pack(pady=10)

        self.browse_button = ctk.CTkButton(self, text="Wybierz plik", command=self.browse_file)
        self.browse_button.pack(pady=5)

        self.encrypt_button = ctk.CTkButton(self, text="Szyfruj", command=self.encrypt)
        self.encrypt_button.pack(pady=10)

        self.upload_button = ctk.CTkButton(self, text="Prześlij na Google Drive", command=self.upload)
        self.upload_button.pack(pady=5)

        self.decrypt_button = ctk.CTkButton(self, text="Odszyfruj", command=self.decrypt)
        self.decrypt_button.pack(pady=5)

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.selected_file = file_path
            self.file_entry.delete(0, ctk.END)
            self.file_entry.insert(0, file_path)

    def encrypt(self):
        if not self.selected_file:
            messagebox.showwarning("Uwaga", "Proszę wybrać plik do zaszyfrowania.")
            return
        try:
            encrypted_path = encrypt_file(self.selected_file)
            messagebox.showinfo("Sukces", f"Plik zaszyfrowany:\n{encrypted_path}")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się zaszyfrować pliku:\n{str(e)}")

    def decrypt(self):
        if not self.selected_file:
            messagebox.showwarning("Uwaga", "Proszę wybrać plik do odszyfrowania.")
            return
        if not self.selected_file.endswith(".enc"):
            messagebox.showwarning("Uwaga", "To nie jest zaszyfrowany plik (.enc).")
            return
        try:
            decrypted_path = decrypt_file(self.selected_file)
            messagebox.showinfo("Sukces", f"Plik odszyfrowany:\n{decrypted_path}")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się odszyfrować pliku:\n{str(e)}")

    def upload(self):
        if not self.selected_file:
            messagebox.showwarning("Uwaga", "Proszę wybrać plik do przesłania.")
            return
        try:
            file_id = upload_to_drive(self.selected_file)
            if file_id:
                messagebox.showinfo("Sukces", f"Plik został przesłany na Google Drive.\nID: {file_id}")
            else:
                messagebox.showwarning("Uwaga", "Plik został przesłany, ale nie otrzymano identyfikatora.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się przesłać pliku:\n{str(e)}")
