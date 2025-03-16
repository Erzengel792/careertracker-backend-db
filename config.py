import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# โหลดค่าจาก .env (สำหรับ development)
load_dotenv()

class Config:
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_secret_key')

    # ดึงค่าจาก environment variables ที่ตั้งไว้ใน App Settings ของ Azure
    AZURE_SQL_DATABASE = os.getenv('AZURE_SQL_DATABASE', 'your_database')
    AZURE_SQL_PASSWORD = os.getenv('AZURE_SQL_PASSWORD', 'your_password')
    AZURE_SQL_PORT = os.getenv('AZURE_SQL_PORT', '1433')
    AZURE_SQL_SERVER = os.getenv('AZURE_SQL_SERVER', 'your_server.database.windows.net')
    AZURE_SQL_USER = os.getenv('AZURE_SQL_USER', 'your_username')
    AZURE_STORAGE_CONNECTION_STRING= os.getenv('AZURE_STORAGE_CONNECTION_STRING', 'your_connection_string')

    # Encode password หากมีอักขระพิเศษ
    encoded_password = quote_plus(AZURE_SQL_PASSWORD)

    # ตั้งค่าการเชื่อมต่อกับ Azure SQL โดยใช้ connection string ของ ODBC
    SQLALCHEMY_DATABASE_URI = (
        f"mssql+pyodbc://{AZURE_SQL_USER}:{encoded_password}@{AZURE_SQL_SERVER}:{AZURE_SQL_PORT}/{AZURE_SQL_DATABASE}"
        f"?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no&Connection+Timeout=30"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


