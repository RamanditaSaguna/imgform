# Aplikasi Pendaftaran Mahasiswa Baru - Tech Edition

Aplikasi web untuk pendaftaran mahasiswa baru dengan tampilan modern teknologis. Aplikasi ini menggunakan **Python Flask** sebagai backend dan **MySQL** sebagai database.

## 🚀 Teknologi yang Digunakan

- **Backend:** Python 3 dengan framework Flask
- **Database:** MySQL
- **Frontend:** HTML5, CSS3, JavaScript
- **Font:** Google Fonts (Outfit, Rajdhani)
- **Efek Visual:** CSS Animations, Gradients, Glassmorphism
- **File Upload:** Handling dan penyimpanan foto profil mahasiswa

## 📋 Prasyarat

Sebelum menjalankan aplikasi, pastikan Anda memiliki:

1. **Python 3.7+** terinstall
2. **MySQL Server** (bisa melalui XAMPP, WAMP, atau instalasi langsung)
3. **Pip** (Python package manager)

## 💻 Instalasi dan Setup

### 1. Clone atau Download Repository

```bash
# Jika menggunakan git
git clone [url-repository]
cd formft

# Atau jika download ZIP, ekstrak dan masuk ke folder
```

### 2. Setup Virtual Environment (Recommended)

```bash
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Untuk Windows
venv\Scripts\activate
# Untuk MacOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install semua package yang diperlukan
pip install -r requirements.txt
```

### 4. Setup Database MySQL

#### Opsi A: Menggunakan XAMPP (Recommended untuk pemula)

1. Download dan install [XAMPP](https://www.apachefriends.org/)
2. Jalankan XAMPP Control Panel
3. Start **Apache** dan **MySQL** services
4. Buka browser dan akses: `http://localhost/phpmyadmin`
5. Buat database baru bernama: `db_pendaftaran_maba`
6. Import file SQL:
   - Klik tab "Import"
   - Choose file: `database/setup.sql`
   - Klik "Go"

#### Opsi B: Menggunakan MySQL CLI

```bash
# Login ke MySQL
mysql -u root -p

# Buat database dan import
mysql -u root -p < database/setup.sql
```

### 5. Konfigurasi Database

Edit file `config/database.py` sesuai dengan konfigurasi MySQL Anda:

```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'db_pendaftaran_maba',
    'user': 'root',        # Sesuaikan dengan username MySQL Anda
    'password': '',        # Sesuaikan dengan password MySQL Anda (kosong untuk XAMPP default)
    'port': 3306
}
```

### 6. Test Koneksi Database (Opsional)

Buat file test untuk memastikan koneksi database berhasil:

```python
# test_db.py
from config.database import test_connection

if test_connection():
    print("✅ Database connection successful!")
else:
    print("❌ Database connection failed!")
```

```bash
python test_db.py
```

## 🔧 Menjalankan Aplikasi

1. **Pastikan virtual environment aktif**
2. **Pastikan MySQL server berjalan**
3. **Jalankan aplikasi:**

```bash
python app.py
```

4. **Buka browser dan akses:**
   - **Form Pendaftaran:** http://localhost:5000/
   - **Daftar Siswa:** http://localhost:5000/daftar-siswa

## 📱 Fitur Aplikasi

### ✨ Form Pendaftaran
- Upload foto profil dengan preview
- Validasi form real-time
- Design modern dengan animasi CSS
- Responsive untuk mobile dan desktop

### 👥 Manajemen Data Siswa
- Tampilan grid card modern
- Search/filter siswa
- Hapus data siswa
- Statistik pendaftar (total, gender)

### 🎨 UI/UX Features
- Tema cyberpunk/tech modern
- Animasi background yang menarik
- Glassmorphism design
- Responsive design
- Loading animations

## 📁 Struktur Proyek

```
formft/
│
├── app.py                  # File utama aplikasi Flask
├── requirements.txt        # Dependencies Python
├── README.md              # Dokumentasi
│
├── config/                # Folder konfigurasi
│   └── database.py        # Konfigurasi database MySQL
│
├── templates/             # Folder template HTML
│   ├── index.html         # Form pendaftaran
│   ├── success.html       # Halaman sukses
│   └── daftar_siswa.html  # Daftar siswa terdaftar
│
├── static/                # Folder file statis
│   ├── css/
│   │   └── style.css      # File CSS utama
│   ├── uploads/           # Folder upload foto
│   │   └── default.jpg    # Foto default
│   └── images/            # Folder gambar
│       └── default-avatar.png
│
└── database/              # Folder database
    └── setup.sql          # Script setup database
```

## 🔧 Troubleshooting

### Masalah Database Connection

```bash
# Error: Access denied for user 'root'@'localhost'
# Solusi: Periksa username dan password di config/database.py

# Error: Can't connect to MySQL server
# Solusi: Pastikan MySQL service berjalan (XAMPP/sistem)
```

### Masalah Module Import

```bash
# Error: ModuleNotFoundError: No module named 'flask'
# Solusi: Pastikan virtual environment aktif dan requirements terinstall
pip install -r requirements.txt
```

### Masalah Upload File

```bash
# Error: File upload tidak berfungsi
# Solusi: Pastikan folder static/uploads memiliki permission write
# Windows: Klik kanan folder > Properties > Security
# Linux/Mac: chmod 755 static/uploads
```

## 🚀 Development

### Menambah Fitur Baru

1. **Edit siswa**: Implementasi di route `/edit-siswa/<id>`
2. **Export data**: Tambah fungsi export ke Excel/PDF
3. **Email notification**: Kirim email konfirmasi otomatis
4. **Dashboard admin**: Halaman admin dengan statistics

### Customization

1. **Tema warna**: Edit variabel CSS di `static/css/style.css`
2. **Database fields**: Update tabel di `database/setup.sql` dan form HTML
3. **Validasi**: Tambah validasi JavaScript di template

## 📸 Screenshot

Form pendaftaran dengan design modern cyberpunk theme, animasi background, dan fitur upload foto yang user-friendly.

## 🤝 Contributing

1. Fork repository
2. Buat branch fitur baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

---

**⚡ Built with love and modern technology ⚡**
