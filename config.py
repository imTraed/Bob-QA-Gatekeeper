"""
Configuration settings for Bob-QA Gatekeeper application
"""
import os

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database settings
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE_DIR = os.path.join(BASE_DIR, 'database')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{os.path.join(DATABASE_DIR, "audit.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Application settings
    APP_NAME = 'Bob-QA Gatekeeper'
    APP_VERSION = '1.0.0'
    
    # EU AI Act compliance settings
    RISK_THRESHOLD_HIGH = 0.7
    RISK_THRESHOLD_MEDIUM = 0.4
    RISK_THRESHOLD_LOW = 0.0
    
    # Pagination
    ITEMS_PER_PAGE = 20
    
    @staticmethod
    def init_app(app):
        """Initialize application with configuration"""
        # Create database directory if it doesn't exist
        os.makedirs(Config.DATABASE_DIR, exist_ok=True)


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# Made with Bob
