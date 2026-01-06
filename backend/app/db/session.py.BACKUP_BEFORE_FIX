"""
Database Session Manager
Supabase Client (Service Role for Backend)
"""

import logging

from supabase import create_client, Client
import os

logger = logging.getLogger(__name__)


# Supabase URLs
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")


def get_supabase() -> Client:
    """
    Supabase client döndür (ANON KEY - Frontend-like access)
    Auth endpoint'leri için kullanılır
    """
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


def get_supabase_admin() -> Client:
    """
    Supabase ADMIN client döndür (SERVICE ROLE KEY)
    Backend queries için - RLS bypass, tam erişim
    
    FAIL-FAST: Env vars yüklenmemişse crash eder
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not url or not key:
        raise RuntimeError("❌ Supabase env vars not loaded! Check .env file.")
    
    # Verify JWT contains service_role
    import jwt
    payload = jwt.decode(key, options={"verify_signature": False})
    
    if payload.get('role') != 'service_role':
        raise RuntimeError(
            f"❌ Invalid JWT role: {payload.get('role')} "
            f"(expected: service_role)"
        )
    
    # Create Supabase admin client
    client = create_client(url, key)
    
    logger.info("✅ Supabase admin client initialized (service_role JWT)")
    
    return client


def get_db():
    """Database session (şimdilik placeholder)"""
    # İleride PostgreSQL direct için kullanılacak
    pass


def get_supabase_for_user(access_token: str) -> Client:
    """
    User-specific Supabase client (RLS enforced)
    Uses user's JWT token - only accesses data user is authorized for
    """
    # Create client with anon key
    client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    
    # Set JWT token for postgrest queries (RLS enforced)
    # This adds Authorization header to all database requests
    client.postgrest.auth(access_token)
    
    return client
