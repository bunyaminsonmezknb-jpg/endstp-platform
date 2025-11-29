"""
End.STP Backend API
FastAPI ana uygulama - 4 Motor Sistemi
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.api.v1.student_analysis import router as student_router

app = FastAPI(
    title="End.STP API",
    description="Akıllı Öğrenme Analiz Sistemi - 4 Motors",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers (eski sistem + yeni motorlar)
app.include_router(api_router, prefix="/api/v1")  # Eski endpoints
app.include_router(student_router)  # Yeni 4 motor (zaten prefix içinde)

@app.get("/")
async def root():
    return {
        "message": "End.STP API - 4 Motors",
        "version": "1.0.0",
        "docs": "/api/docs",
        "motors": ["BS-Model", "Difficulty", "Time", "Priority"]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "motors": 4}
