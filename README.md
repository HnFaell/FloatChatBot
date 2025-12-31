# FloatChatBot

# AIdea - Floating AI Chatbot

Aplikasi chatbot desktop mengambang (floating) yang menggunakan OpenAI API dengan antarmuka PyQt5. AIdea dirancang untuk memberikan akses cepat ke AI assistant tanpa mengganggu pekerjaan Anda.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-API-orange.svg)

## ✨ Fitur Utama

- **Floating Window**: Jendela chat yang selalu berada di atas aplikasi lain
- **Mode Minimize**: Minimize ke bubble kecil untuk menghemat ruang layar
- **Draggable Interface**: Dapat dipindahkan ke posisi mana saja di layar
- **Real-time Chat**: Komunikasi langsung dengan model GPT OpenAI
- **Customizable**: Pengaturan model, temperature, dan max tokens
- **Translucent Design**: Desain transparan yang modern dan elegan

## 📋 Prasyarat

Sebelum menjalankan aplikasi ini, pastikan Anda telah menginstal:

- Python 3.7 atau lebih tinggi
- pip (Python package manager)
- OpenAI API Key

## 🔧 Instalasi

1. **Clone repository ini**
```bash
git clone https://github.com/username/aidea-chatbot.git
cd aidea-chatbot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

Atau install manual:
```bash
pip install PyQt5 requests
```

3. **Konfigurasi API Key**

Buka file `main.py` dan ganti `OPENAI_API_KEY` dengan API key Anda:
```python
OPENAI_API_KEY = "sk-your-api-key-here"
```

> ⚠️ **Penting**: Jangan commit API key Anda ke repository publik!

## 🚀 Cara Menggunakan

1. **Jalankan aplikasi**
```bash
python main.py
```

2. **Gunakan antarmuka**
   - Ketik pesan Anda di kolom input
   - Tekan Enter atau klik tombol "Kirim"
   - AI akan merespons dalam beberapa detik

3. **Kontrol jendela**
   - **⚙️ (Gear)**: Membuka dialog informasi dan pengaturan
   - **• (Dot)**: Minimize/maximize jendela
   - **✕ (Close)**: Menutup aplikasi
   - **Drag**: Klik dan tahan di area mana pun untuk memindahkan jendela

4. **Mode Minimize**
   - Klik tombol • untuk minimize ke bubble
   - Bubble akan muncul di pojok kanan bawah layar
   - Klik bubble untuk membuka kembali jendela chat

## ⚙️ Konfigurasi

### Model Configuration
Di dalam kode, Anda dapat mengubah pengaturan default:

```python
DEFAULT_MODEL = "gpt-3.5-turbo"  # Model yang digunakan
temperature = 0.7                 # Kreativitas respons (0.0 - 2.0)
maxtokens = 300                   # Panjang maksimal respons
```

### Kustomisasi Tampilan
Stylesheet dapat dimodifikasi di method `apply_stylesheet()` untuk mengubah:
- Warna background
- Transparansi
- Border radius
- Font size dan style

## 📁 Struktur Kode

### Class Utama

**`ConfigDialog`**
- Dialog informasi dan pengaturan aplikasi
- Menampilkan pesan selamat datang dan panduan penggunaan

**`APIWorker`**
- Thread terpisah untuk menangani API call
- Mencegah UI freeze saat menunggu respons
- Mengirim signal untuk response dan error handling

**`FloatingChatbot`**
- Main application window
- Mengelola UI dan interaksi pengguna
- Handle drag, minimize, dan chat functionality

### Komponen UI

1. **Header**: Judul aplikasi dan tombol kontrol
2. **Chat Display**: Area untuk menampilkan percakapan
3. **Input Area**: Field input dan tombol kirim
4. **Bubble**: Mode minimize dalam bentuk bubble

## 🔒 Keamanan

- ⚠️ **Jangan** hardcode API key di production
- Gunakan environment variables atau file config terpisah
- Tambahkan `config.py` atau `.env` ke `.gitignore`

Contoh menggunakan environment variable:
```python
import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```

## 🐛 Troubleshooting

**API Key Error**
- Pastikan API key valid dan aktif
- Cek saldo akun OpenAI Anda

**Connection Timeout**
- Periksa koneksi internet
- API call memiliki timeout 30 detik

**UI Issues**
- Pastikan PyQt5 terinstall dengan benar
- Coba reinstall dependencies

## 📝 Lisensi

Project ini menggunakan lisensi MIT. Lihat file `LICENSE` untuk detail.

## 🤝 Kontribusi

Kontribusi selalu welcome! Silakan:
1. Fork repository ini
2. Buat branch fitur (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📞 Kontak

Jika ada pertanyaan atau saran, silakan buat issue di repository ini.

## ⚠️ Disclaimer

Aplikasi ini menggunakan OpenAI API yang berbayar. Pastikan untuk memantau penggunaan token Anda untuk menghindari biaya tak terduga. Gunakan dengan bijak dan hemat token.

---

**Selamat menggunakan AIdea! Enjoy your AI assistant! 🚀**
