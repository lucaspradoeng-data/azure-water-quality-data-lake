from pathlib import Path
import os

import pyodbc
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

server = os.getenv("AZURE_SQL_SERVER")
database = os.getenv("AZURE_SQL_DATABASE")
user = os.getenv("AZURE_SQL_USER")
password = os.getenv("AZURE_SQL_PASSWORD")
driver = os.getenv("ODBC_DRIVER", "ODBC Driver 18 for SQL Server")

connection_string = (
    f"DRIVER={{{driver}}};"
    f"SERVER=tcp:{server},1433;"
    f"DATABASE={database};"
    f"UID={user};"
    f"PWD={password};"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
    "Connection Timeout=60;"
)

print("Testando conexão direta via pyodbc...")

with pyodbc.connect(connection_string) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    resultado = cursor.fetchone()[0]

print(f"Conexão pyodbc validada com sucesso. Resultado: {resultado}")