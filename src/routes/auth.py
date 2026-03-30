from fastapi import APIRouter, HTTPException, Depends
from src.models.user import UserCreate, UserLogin
from src.services.auth_service import AuthService
from src.database.db import Database
import mysql.connector

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
def register(user_data: UserCreate):
    db = Database()
    conn = db.connect()
    if not conn:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    
    cursor = conn.cursor()
    try:
        # Encriptamos la contraseña antes de guardar
        hashed_pwd = AuthService.hash_password(user_data.password)
        
        query = "INSERT INTO users (email, password_hash) VALUES (%s, %s)"
        cursor.execute(query, (user_data.email, hashed_pwd))
        conn.commit()
        
        return {"message": "Usuario registrado exitosamente en logW"}
    except mysql.connector.Error as err:
        if err.errno == 1062: # Error de duplicado en MariaDB
            raise HTTPException(status_code=400, detail="El email ya existe")
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        db.close()

@router.post("/login")
def login(credentials: UserLogin):
    db = Database()
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM users WHERE email = %s", (credentials.email,))
    user = cursor.fetchone()
    db.close()

    if not user or not AuthService.verify_password(credentials.password, user['password_hash']):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    # Si todo está bien, generamos el "carnet" (JWT)
    token = AuthService.create_access_token(data={"sub": user['email']})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/forgot-password")
def forgot_password(email: str):
    db = Database()
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)
    
    # 1. Verificar si el usuario existe
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    db.close()

    if not user:
        # Por seguridad, a veces es mejor decir que se envió el correo 
        # aunque el usuario no exista, para evitar "user enumeration".
        return {"message": "Si el email existe, se ha enviado un enlace de recuperación."}

    # 2. Generar un Token de un solo uso (expira en 15 min)
    reset_token = AuthService.create_access_token(
        data={"sub": user['email'], "action": "password_reset"},
        expires_delta=timedelta(minutes=15)
    )

    # 3. Simulación de envío de correo
    # En un proyecto real aquí usarías una librería como 'emails' o 'fastapi-mail'
    reset_link = f"https://logw-app.com/reset-password?token={reset_token}"
    
    return {
        "message": "Enlace generado",
        "debug_link": reset_link  # Esto es para que tú lo pruebes sin configurar email real todavía
    }
