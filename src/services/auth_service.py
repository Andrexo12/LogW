import jwt
import os
from datetime import datetime, timedelta
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

# Configuramos el algoritmo de encriptación para las contraseñas
# Usamos bcrypt porque es el estándar de la industria
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

class AuthService:
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Transforma la contraseña plana en un hash seguro para MariaDB."""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Compara la contraseña que entra con el hash guardado en HeidiSQL."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None):
        """Crea el JWT con los Claims (payload)."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
