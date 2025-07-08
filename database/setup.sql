-- Script untuk setup database pendaftaran mahasiswa baru
-- Jalankan script ini di MySQL untuk membuat database dan tabel

-- Membuat database baru
CREATE DATABASE IF NOT EXISTS db_pendaftaran_maba 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Menggunakan database yang baru dibuat
USE db_pendaftaran_maba;

-- Membuat tabel pendaftar
CREATE TABLE IF NOT EXISTS pendaftar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    waktu_daftar DATETIME NOT NULL,
    nama_lengkap VARCHAR(100) NOT NULL,
    tanggal_lahir DATE NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    no_telepon VARCHAR(20) NOT NULL,
    alamat TEXT NOT NULL,
    jenis_kelamin ENUM('L', 'P') NOT NULL,
    jurusan_pilihan VARCHAR(100) NOT NULL,
    asal_sekolah VARCHAR(100) NOT NULL,
    nilai_rata_rata DECIMAL(4,2) NOT NULL,
    motivasi TEXT,
    foto VARCHAR(255) DEFAULT 'default.jpg',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Membuat index untuk performa yang lebih baik
CREATE INDEX idx_email ON pendaftar(email);
CREATE INDEX idx_waktu_daftar ON pendaftar(waktu_daftar);
CREATE INDEX idx_jurusan ON pendaftar(jurusan_pilihan);

-- Insert data contoh (opsional)
INSERT INTO pendaftar (
    waktu_daftar, nama_lengkap, tanggal_lahir, email, no_telepon, 
    alamat, jenis_kelamin, jurusan_pilihan, asal_sekolah, nilai_rata_rata, 
    motivasi, foto
) VALUES 
(
    NOW(), 
    'John Doe', 
    '2005-01-15', 
    'john.doe@email.com', 
    '081234567890',
    'Jl. Contoh No. 123, Jakarta', 
    'L', 
    'Teknik Informatika', 
    'SMA Negeri 1 Jakarta', 
    85.50,
    'Saya ingin menjadi programmer yang handal dan berkontribusi untuk kemajuan teknologi Indonesia.',
    'default.jpg'
),
(
    NOW(), 
    'Jane Smith', 
    '2005-05-20', 
    'jane.smith@email.com', 
    '081234567891',
    'Jl. Example No. 456, Bandung', 
    'P', 
    'Sistem Informasi', 
    'SMA Negeri 2 Bandung', 
    88.75,
    'Saya tertarik dengan analisis data dan ingin mengembangkan sistem informasi yang bermanfaat.',
    'default.jpg'
);

-- Menampilkan struktur tabel
DESCRIBE pendaftar;

-- Menampilkan data yang sudah diinsert
SELECT * FROM pendaftar;
