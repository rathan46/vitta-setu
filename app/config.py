import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-dev-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'vitta_setu.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session config
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # App specific
    CALLBACK_MAX_RETRIES = int(os.environ.get('CALLBACK_MAX_RETRIES', 5))
    CALLBACK_INITIAL_DELAY = int(os.environ.get('CALLBACK_INITIAL_DELAY', 5))
    SSE_ENABLED = os.environ.get('SSE_ENABLED', 'True') == 'True'
    APP_DOMAIN = os.environ.get('APP_DOMAIN', 'http://localhost:5000')

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False  # Allows HTTP for local dev

class ProductionConfig(Config):
    DEBUG = False
    # Ensure secure cookies in production
    SESSION_COOKIE_SECURE = True

config_by_name = dict(
    development=DevelopmentConfig,
    production=ProductionConfig,
    default=DevelopmentConfig
)
