from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.auth import router as auth_router
import logging
import os

# Configurar logging con formato mejorado
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="logW API",
    description="API for logW application",
    version="1.0.0"
)

# Middleware CORS: restringir orígenes en producción usando variables de entorno
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas de autenticación
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

@app.get("/", tags=["General"])
async def home():
    logger.info("Home endpoint accessed")
    return {"status": "logW API is running", "version": "1.0.0"}

@app.get("/health", tags=["General"])
async def health_check():
    logger.info("Health check performed")
    return {"status": "healthy"}
