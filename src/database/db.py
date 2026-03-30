import mysql.connector
import os
from dotenv import load_dotenv

# Cargamos las variables del archivo .env
load_dotenv()

class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
            if self.connection.is_connected():
                print("✅ Conexión exitosa a MariaDB")
                return self.connection
        except mysql.connector.Error as e:
            print(f"❌ Error al conectar: {e}")
            return None

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔌 Conexión cerrada.")
import mysql.connector
import os
from dotenv import load_dotenv

# Cargamos las variables del archivo .env
load_dotenv()

class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
            if self.connection.is_connected():
                print("✅ Conexión exitosa a MariaDB")
                return self.connection
        except mysql.connector.Error as e:
            print(f"❌ Error al conectar: {e}")
            return None

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔌 Conexión cerrada.")
