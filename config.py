import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '9876'
    MYSQL_DB = 'emp'
    MYSQL_CURSORCLASS = 'DictCursor'
