-- Script untuk menambahkan kolom foto ke tabel pendaftar yang sudah ada
-- Jalankan script ini jika tabel pendaftar sudah ada tetapi belum memiliki kolom foto

USE db_pendaftaran_maba;

-- Cek apakah kolom foto sudah ada
SELECT COUNT(*) as column_exists
FROM information_schema.COLUMNS 
WHERE TABLE_SCHEMA = 'db_pendaftaran_maba' 
AND TABLE_NAME = 'pendaftar' 
AND COLUMN_NAME = 'foto';

-- Jika kolom belum ada (hasil query di atas = 0), jalankan perintah berikut:
ALTER TABLE pendaftar 
ADD COLUMN foto VARCHAR(255) DEFAULT 'default.jpg' 
AFTER motivasi;

-- Update existing records to have default photo
UPDATE pendaftar 
SET foto = 'default.jpg' 
WHERE foto IS NULL OR foto = '';

-- Verifikasi struktur tabel
DESCRIBE pendaftar;

-- Tampilkan semua data untuk memastikan kolom foto sudah ada
SELECT id, nama_lengkap, email, foto FROM pendaftar LIMIT 5;
