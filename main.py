# File: main.py

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.application.exceptions.html_exceptions import HTMLError
from app.interface.http.api.v1.router import api_router
from app.interface.http.api.v1.errors.error import custom_html_error_handler

# Import AppState yang baru kita bikin
from app.core.state import AppState


# --- 0. Lifespan buat inisialisasi AppState ---
@asynccontextmanager
async def lifespan(server: FastAPI):
    # Pas server nyala, bikin instance AppState dan tempel di server.state
    server.state.ext = AppState()

    yield  # Server jalan

    # Kalau butuh teardown pas server mati (misal nutup koneksi DB global), taruh di sini
    # await app.state.ext.db_provider.close() 


app = FastAPI(
    title="Jubelio Report Server",
    description="High-performance reporting engine powered by Python & Rust Core",
    version="1.0.0",
    lifespan=lifespan  # <--- Jangan lupa daftarin lifespan-nya cuy
)

app.add_exception_handler(HTMLError, custom_html_error_handler)

# --- 1. CORS Configuration ---
origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://*.jubelio.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

# --- 3. Entry Point ---
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )