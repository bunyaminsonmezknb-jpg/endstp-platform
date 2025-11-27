"""
Database Session Manager
Supabase Client (Service Role for Backend)
"""

from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

# Supabase URLs
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")


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
    """
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


def get_db():
    """Database session (şimdilik placeholder)"""
    # İleride PostgreSQL direct için kullanılacak
    pass
