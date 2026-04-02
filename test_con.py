import mysql.connector
import os
from dotenv import load_dotenv

# Forzamos la carga del .env
load_dotenv()

def test():
    print("--- Intentando conectar con estos datos ---")
    print(f"Host: {os.getenv('DB_HOST')}")
    print(f"User: {os.getenv('DB_USER')}")
    print(f"DB: {os.getenv('DB_NAME')}")
    
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        if conn.is_connected():
            print("\n✅ ¡CONEXIÓN EXITOSA! El puente está bien construido.")
            conn.close()
    except Exception as e:
        print(f"\n❌ ERROR DE CONEXIÓN: {e}")

if __name__ == "__main__":
    test()