# =============================================================================
# GLOBAL-FIRST COMPLIANCE HEADER
# =============================================================================
# File: backend/app/db/session.py
# Role: Database session management - Supabase + SQLAlchemy
# Updated: 2026-02-13 (Phase 1A: SYNC SQLAlchemy added)
# Author: End.STP Team
#
# Architecture:
# - Supabase PostgREST (existing, unchanged)
# - SQLAlchemy SYNC (new, parallel)
# - Future: Phase 5 async migration if needed
# =============================================================================

"""
Database Session Manager
- Supabase Client (Service Role for Backend)
- SQLAlchemy (Direct DB access - SYNC)
"""

import logging
import os
from typing import Generator

import jwt
from supabase import Client, create_client

# =============================================================================
# SQLAlchemy Imports (Phase 1A)
# =============================================================================
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

logger = logging.getLogger(__name__)

# =============================================================================
# SUPABASE CLIENT (EXISTING - UNCHANGED)
# =============================================================================


def get_supabase() -> Client:
    """
    Supabase client döndür (ANON KEY - Frontend-like access)
    Auth endpoint'leri için kullanılır
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")

    if not url or not key:
        raise RuntimeError("❌ Supabase URL/ANON_KEY not loaded!")

    return create_client(url, key)


def get_supabase_admin() -> Client:
    """
    Supabase ADMIN client döndür (SERVICE ROLE KEY)
    Backend queries için - RLS bypass, tam erişim

    FAIL-FAST: Env vars yüklenmemişse crash eder
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not url:
        raise RuntimeError("Sunucu yapılandırma hatası: Supabase URL bulunamadı.")

    if not key:
        raise RuntimeError("Sunucu yapılandırma hatası: Admin anahtarı bulunamadı.")

    # Verify JWT contains service_role
    try:
        payload = jwt.decode(key, options={"verify_signature": False})

        if payload.get("role") != "service_role":
            raise RuntimeError(
                f"❌ Invalid JWT role: {payload.get('role')} "
                f"(expected: service_role)"
            )
    except Exception as e:
        raise RuntimeError(f"❌ JWT verification failed: {e}")

    # Create Supabase admin client
    client = create_client(url, key)

    logger.info("✅ Supabase admin client initialized (service_role JWT)")

    return client


def get_supabase_for_user(access_token: str) -> Client:
    """
    User-specific Supabase client (RLS enforced)
    Uses user's JWT token - only accesses data user is authorized for
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")

    if not url or not key:
        raise RuntimeError("❌ Supabase URL/ANON_KEY not loaded!")

    # Create client with anon key
    client = create_client(url, key)

    # Set JWT token for postgrest queries (RLS enforced)
    # This adds Authorization header to all database requests
    client.postgrest.auth(access_token)

    return client


# =============================================================================
# SQLALCHEMY SETUP (PHASE 1A - NEW)
# =============================================================================

# Database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Engine (connection pool)
engine = None
SessionLocal = None

if DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Health check before use
        pool_size=5,  # Connection pool size
        max_overflow=10,  # Max extra connections
        echo=False,  # SQL logging (set True for debug)
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("✅ SQLAlchemy engine initialized (SYNC)")
    print("🔧 DEBUG: SQLAlchemy engine initialized (SYNC)")
else:
    logger.warning("⚠️ DATABASE_URL not found - SQLAlchemy disabled")
    print("🔧 DEBUG: DATABASE_URL not found")

def get_db() -> Generator[Session, None, None]:
    """
    SQLAlchemy session dependency (SYNC)
    Usage: db: Session = Depends(get_db)

    Phase 1A: Direct sync session
    Phase 5: Will migrate to async if needed

    Threadpool isolation:
    For async endpoints using sync DB calls, FastAPI automatically
    runs Depends() in threadpool. For explicit isolation, use:
        from fastapi.concurrency import run_in_threadpool
        result = await run_in_threadpool(sync_function, db)
    """
    if not SessionLocal:
        raise RuntimeError("❌ Database not configured (DATABASE_URL missing)")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()