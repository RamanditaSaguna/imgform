from flask import Flask, render_template, request, redirect, url_for, flash
import os
import uuid
import datetime
from werkzeug.utils import secure_filename
from config.database import get_db_connection, close_connection
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'maba_form_secret_key'

# Konfigurasi upload
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Pastikan direktori uploads ada
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB max

# Pastikan file default.jpg ada
DEFAULT_AVATAR_PATH = os.path.join(UPLOAD_FOLDER, 'default.jpg')
if not os.path.exists(DEFAULT_AVATAR_PATH):
    # Coba salin dari static/images jika ada
    DEFAULT_IMAGE = os.path.join('static', 'images', 'default-avatar.png')
    if os.path.exists(DEFAULT_IMAGE):
        import shutil
        try:
            shutil.copy(DEFAULT_IMAGE, DEFAULT_AVATAR_PATH)
        except:
            # Jika gagal, buat file dummy
            with open(DEFAULT_AVATAR_PATH, 'w') as f:
                f.write('Placeholder for default avatar')

# Fungsi untuk mengecek ekstensi file
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Fungsi untuk mengecek dan memperbarui struktur database
def check_and_update_database_structure():
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            
            # Cek apakah kolom 'foto' sudah ada
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'pendaftar' 
                AND COLUMN_NAME = 'foto'
            """)
            
            column_exists = cursor.fetchone()[0] > 0
            
            # Jika kolom belum ada, tambahkan
            if not column_exists:
                cursor.execute("""
                    ALTER TABLE pendaftar 
                    ADD COLUMN foto VARCHAR(255) DEFAULT 'default.jpg'
                """)
                conn.commit()
                print("Kolom 'foto' berhasil ditambahkan ke tabel pendaftar")
                
            close_connection(conn, cursor)
            return True
        return False
    except Error as e:
        print(f"Error saat mengupdate struktur database: {str(e)}")
        return False

# Jalankan pemeriksaan database saat aplikasi dimulai
try:
    check_and_update_database_structure()
except Exception as e:
    print(f"⚠️  Database connection failed: {e}")
    print("📝 App will run in demo mode. Please setup MySQL to enable full functionality.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/demo')
def demo():
    """Demo route to show the interface without database"""
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        try:
            # Mengambil data dari form
            nama = request.form['nama']
            tanggal_lahir = request.form['tanggal_lahir']
            email = request.form['email']
            telepon = request.form['telepon']
            alamat = request.form['alamat']
            jenis_kelamin = request.form['jenis_kelamin']
            jurusan = request.form['jurusan']
            asal_sekolah = request.form['asal_sekolah']
            nilai = request.form['nilai']
            motivasi = request.form.get('motivasi', '')
            
            # Handle foto upload
            foto_filename = 'default.jpg'
            if 'foto' in request.files:
                file = request.files['foto']
                if file and file.filename and allowed_file(file.filename):
                    # Generate unique filename
                    filename = secure_filename(file.filename)
                    unique_filename = f"{str(uuid.uuid4())[:8]}_{filename}"
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                    file.save(file_path)
                    foto_filename = unique_filename
            
            # Validasi sederhana
            if not nama or not email or not telepon:
                flash('Semua bidang yang wajib harus diisi!')
                return redirect(url_for('index'))
            
            # Menyimpan data ke MySQL
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                
                # Cek apakah kolom foto ada
                try:
                    # Siapkan query SQL dengan foto
                    query = """INSERT INTO pendaftar 
                            (waktu_daftar, nama_lengkap, tanggal_lahir, email, no_telepon, alamat, 
                            jenis_kelamin, jurusan_pilihan, asal_sekolah, nilai_rata_rata, motivasi, foto)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    
                    # Data untuk dimasukkan dengan foto
                    data_tuple = (
                        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        nama, tanggal_lahir, email, telepon, alamat,
                        jenis_kelamin, jurusan, asal_sekolah, nilai, motivasi, foto_filename
                    )
                    
                    # Eksekusi query
                    cursor.execute(query, data_tuple)
                    
                except Error as e:
                    if "Unknown column 'foto'" in str(e):
                        # Jika kolom foto tidak ada, gunakan query tanpa kolom foto
                        query = """INSERT INTO pendaftar 
                                (waktu_daftar, nama_lengkap, tanggal_lahir, email, no_telepon, alamat, 
                                jenis_kelamin, jurusan_pilihan, asal_sekolah, nilai_rata_rata, motivasi)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                        
                        # Data tanpa foto
                        data_tuple = (
                            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            nama, tanggal_lahir, email, telepon, alamat,
                            jenis_kelamin, jurusan, asal_sekolah, nilai, motivasi
                        )
                        
                        cursor.execute(query, data_tuple)
                        
                        # Tampilkan pesan untuk administrator
                        print("PERINGATAN: Kolom 'foto' tidak ditemukan. Jalankan script add_foto_column.sql")
                    else:
                        # Jika error lain, raise ulang
                        raise e
                
                conn.commit()
                close_connection(conn, cursor)
                
                # Redirect ke halaman sukses
                return render_template('success.html', nama=nama)
            else:
                # Demo mode - just show success page
                flash('📝 Demo Mode: Form submitted successfully! (Data not saved to database)')
                return render_template('success.html', nama=nama)
        
        except Exception as e:
            flash(f'Terjadi kesalahan: {str(e)}')
            return redirect(url_for('index'))

@app.route('/daftar-siswa')
def daftar_siswa():
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            
            # Cek apakah kolom foto ada
            try:
                # Query dengan kolom foto
                query = """SELECT id, waktu_daftar, nama_lengkap, alamat, jenis_kelamin, 
                        asal_sekolah, foto FROM pendaftar ORDER BY waktu_daftar DESC"""
                cursor.execute(query)
            except Error as e:
                if "Unknown column 'foto'" in str(e):
                    # Query tanpa kolom foto
                    query = """SELECT id, waktu_daftar, nama_lengkap, alamat, jenis_kelamin, 
                            asal_sekolah FROM pendaftar ORDER BY waktu_daftar DESC"""
                    cursor.execute(query)
                    print("PERINGATAN: Kolom 'foto' tidak ditemukan. Jalankan script add_foto_column.sql")
                else:
                    # Jika error lain, raise ulang
                    raise e
            
            # Ambil semua data
            siswa_list = cursor.fetchall()
            
            # Format waktu daftar dan tambahkan default foto jika tidak ada
            for siswa in siswa_list:
                if isinstance(siswa['waktu_daftar'], datetime.datetime):
                    siswa['waktu_daftar'] = siswa['waktu_daftar'].strftime('%d-%m-%Y %H:%M:%S')
                
                # Jika tidak ada kolom foto atau foto kosong, gunakan default
                if 'foto' not in siswa or not siswa['foto']:
                    siswa['foto'] = 'default.jpg'
            
            # Tutup koneksi
            close_connection(conn, cursor)
            
            # Render template dengan data
            current_time = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            return render_template('daftar_siswa.html', siswa_list=siswa_list, current_time=current_time)
        else:
            # Demo mode - show sample data
            return demo_student_list()
    
    except Exception as e:
        # Demo mode - show sample data
        return demo_student_list()

def demo_student_list():
    """Demo student list when database is not available"""
    # Sample data for demo
    demo_students = [
        {
            'id': 1,
            'waktu_daftar': '08-07-2025 10:30:00',
            'nama_lengkap': 'John Doe (Demo)',
            'alamat': 'Jl. Contoh No. 123, Jakarta',
            'jenis_kelamin': 'L',
            'asal_sekolah': 'SMA Negeri 1 Jakarta',
            'foto': 'default.jpg'
        },
        {
            'id': 2,
            'waktu_daftar': '08-07-2025 11:15:00',
            'nama_lengkap': 'Jane Smith (Demo)',
            'alamat': 'Jl. Example No. 456, Bandung',
            'jenis_kelamin': 'P',
            'asal_sekolah': 'SMA Negeri 2 Bandung',
            'foto': 'default.jpg'
        },
        {
            'id': 3,
            'waktu_daftar': '08-07-2025 12:00:00',
            'nama_lengkap': 'Ahmad Rizki (Demo)',
            'alamat': 'Jl. Sample No. 789, Surabaya',
            'jenis_kelamin': 'L',
            'asal_sekolah': 'SMA Negeri 3 Surabaya',
            'foto': 'default.jpg'
        }
    ]
    
    current_time = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    flash('📝 Demo Mode: Database not connected. Sample data shown.', 'info')
    return render_template('daftar_siswa.html', siswa_list=demo_students, current_time=current_time)

@app.route('/hapus-siswa/<int:id>')
def hapus_siswa(id):
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            
            # Ambil nama foto sebelum menghapus data
            query_foto = "SELECT foto FROM pendaftar WHERE id = %s"
            cursor.execute(query_foto, (id,))
            result = cursor.fetchone()
            
            if result and result['foto'] != 'default.jpg':
                foto_path = os.path.join(app.config['UPLOAD_FOLDER'], result['foto'])
                if os.path.exists(foto_path):
                    os.remove(foto_path)
            
            # Hapus data siswa
            query_delete = "DELETE FROM pendaftar WHERE id = %s"
            cursor.execute(query_delete, (id,))
            conn.commit()
            
            # Tutup koneksi
            close_connection(conn, cursor)
            
            flash('Data siswa berhasil dihapus!')
            return redirect(url_for('daftar_siswa'))
        else:
            flash('Tidak dapat terhubung ke database!')
            return redirect(url_for('daftar_siswa'))
    
    except Exception as e:
        flash(f'Terjadi kesalahan: {str(e)}')
        return redirect(url_for('daftar_siswa'))

@app.route('/edit-siswa/<int:id>', methods=['GET', 'POST'])
def edit_siswa(id):
    # Implementasi edit siswa akan ditambahkan sesuai kebutuhan
    flash('Fitur edit siswa belum diimplementasikan')
    return redirect(url_for('daftar_siswa'))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
