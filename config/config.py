"""
Application Configuration
Customize these settings according to your needs
"""

import os

class Config:
    """Base configuration"""
    
    # Application Settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'maba_form_secret_key_change_this_in_production'
    
    # File Upload Settings
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Database Settings (can be overridden by environment variables)
    DB_HOST = os.environ.get('DB_HOST') or 'localhost'
    DB_USER = os.environ.get('DB_USER') or 'root'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or ''
    DB_NAME = os.environ.get('DB_NAME') or 'db_pendaftaran_maba'
    DB_PORT = int(os.environ.get('DB_PORT') or 3306)
    
    # Application Settings
    DEBUG = True  # Set to False in production
    
    # Available Study Programs
    STUDY_PROGRAMS = [
        'Teknik Informatika',
        'Sistem Informasi', 
        'Teknik Komputer',
        'Data Science',
        'Cyber Security',
        'Game Development',
        'UI/UX Design',
        'Digital Marketing'
    ]
    
    # University Information
    UNIVERSITY_NAME = "Tech University"
    UNIVERSITY_TAGLINE = "Future Starts Here"
    CONTACT_EMAIL = "admin@techuniversity.edu"
    
    # Pagination Settings
    STUDENTS_PER_PAGE = 12
    
    # Theme Settings
    PRIMARY_COLOR = "#00ff88"
    SECONDARY_COLOR = "#00ccdd"
    BACKGROUND_COLOR = "#0f0f0f"

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-must-set-secret-key-in-production'

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    DB_NAME = 'test_db_pendaftaran_maba'

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
