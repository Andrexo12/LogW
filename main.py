from fastapi import FastAPI
from src.routes.auth import router as auth_router

app = FastAPI(title="logW API")

# Incluimos las rutas de autenticación
app.include_router(auth_router)

@app.get("/")
def home():
    return {"status": "logW API is running"}
