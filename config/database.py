import mysql.connector
from mysql.connector import Error

# Konfigurasi database MySQL
DB_CONFIG = {
    'host': 'localhost',
    'database': 'db_pendaftaran_maba',
    'user': 'root',
    'password': '',  # Sesuaikan dengan password MySQL Anda
    'port': 3306
}

def get_db_connection():
    """
    Membuat koneksi ke database MySQL
    Returns:
        connection object jika berhasil, None jika gagal
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def close_connection(connection, cursor=None):
    """
    Menutup koneksi database
    Args:
        connection: objek koneksi database
        cursor: objek cursor (opsional)
    """
    try:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
    except Error as e:
        print(f"Error closing connection: {e}")

def test_connection():
    """
    Menguji koneksi ke database
    Returns:
        True jika berhasil terhubung, False jika gagal
    """
    connection = get_db_connection()
    if connection:
        close_connection(connection)
        return True
    return False
