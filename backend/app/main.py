"""
End.STP Backend API
FastAPI ana uygulama - 4 Motor Sistemi + Admin Panel
"""

# ============================================
# 0) ENV LOAD (ALTIN STANDART - TEK KEZ)
# ============================================

from pathlib import Path
import os
import time

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent  # backend/
ENV_PATH = BASE_DIR / ".env"

loaded = load_dotenv(dotenv_path=ENV_PATH, override=True)
print(f"✅ .env loaded={loaded} path={ENV_PATH}")

# Fail-fast
assert os.getenv("SUPABASE_URL"), "❌ SUPABASE_URL not loaded"
assert os.getenv("SUPABASE_SERVICE_ROLE_KEY"), "❌ SUPABASE_SERVICE_ROLE_KEY not loaded"
assert os.getenv("SUPABASE_JWT_SECRET"), "❌ SUPABASE_JWT_SECRET not loaded"

# ============================================
# 1) NOW SAFE TO IMPORT APP MODULES
# ============================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.api.v1.student_analysis import router as student_router
from app.api.v1.endpoints import motors, motor_health, motor_test, segmentation

# ============================================
# 2) APP TANIMI
# ============================================

app = FastAPI(
    title="End.STP API",
    description="Akıllı Öğrenme Analiz Sistemi - 4 Motors + Admin Panel",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# ============================================
# 3) CORS MIDDLEWARE (FIXED)
# ============================================
# Admin panel fix: Both localhost and 127.0.0.1 origins
# allow_credentials=True required for JWT authentication
# ============================================

CORS_ORIGINS = [
    "http://localhost:3000",      # ✅ Frontend dev (primary)
    "http://127.0.0.1:3000",      # ✅ Alternative localhost
    "http://localhost:3001",      # ✅ Alternative port
    "http://127.0.0.1:3001",      # ✅ Alternative port + IP
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,              # ✅ Specific origins (not "*")
    allow_credentials=True,                  # ✅ Required for JWT auth
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],  # ✅ All methods
    allow_headers=["*"],                     # ✅ All headers (including Authorization)
    expose_headers=["*"],                    # ✅ Expose response headers
    max_age=600,                             # ✅ Preflight cache (10 min)
)

# ============================================
# 4) MONITORING MIDDLEWARE
# ============================================

async def _report_slow_or_error(flag_key: str, payload: dict):
    try:
        from app.db.session import get_supabase_admin
        supabase = get_supabase_admin()
        supabase.table("feature_flags").update(payload).eq("flag_key", flag_key).execute()
    except Exception as e:
        print(f"Monitoring report failed: {e}")

def _flag_from_path(path: str) -> str | None:
    if "/student/tasks/today" in path:
        return "daily_tasks"
    if "/student/todays-tasks" in path:
        return "at_risk_display"
    if "/test-entry" in path:
        return "test_entry"
    return None

@app.middleware("http")
async def monitor_response_time(request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = int((time.time() - start_time) * 1000)
        response.headers["X-Process-Time"] = str(process_time)

        flag_key = _flag_from_path(request.url.path)
        if flag_key and process_time > 1000:
            await _report_slow_or_error(
                flag_key,
                {
                    "avg_response_time_ms": process_time,
                    "last_success_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                },
            )
            print(f"⚠️ SLOW: {flag_key} took {process_time}ms")

        return response

    except Exception as e:
        process_time = int((time.time() - start_time) * 1000)
        flag_key = _flag_from_path(request.url.path)
        if flag_key:
            try:
                from app.db.session import get_supabase_admin
                supabase = get_supabase_admin()
                r = supabase.table("feature_flags").select("error_count, health_score").eq("flag_key", flag_key).execute()
                current = (r.data or [{}])[0]
                new_error_count = int(current.get("error_count", 0)) + 1
                new_health = max(0, int(current.get("health_score", 100)) - 10)

                await _report_slow_or_error(
                    flag_key,
                    {
                        "error_count": new_error_count,
                        "health_score": new_health,
                        "last_error_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "last_error_message": str(e)[:500],
                        "avg_response_time_ms": process_time,
                    },
                )
            except Exception as ee:
                print(f"Error reporting failed: {ee}")

        raise

# ============================================
# 5) ROUTERS
# ============================================

# Main API router (includes admin)
app.include_router(api_router, prefix="/api/v1")
app.include_router(student_router)

# Progress router (MODULAR)
try:
    from app.api.v1.endpoints.progress import router as progress_router
    app.include_router(progress_router, prefix="/api/v1", tags=["progress"])
    print("✅ Progress router loaded successfully")
except ImportError as e:
    print(f"⚠️  Progress router not found: {e}")
except Exception as e:
    print(f"❌ Error loading progress router: {e}")

# Motor Routers
try:
    app.include_router(motor_health.router, prefix="/api/v1/motors", tags=["motor-health"])
    app.include_router(motor_test.router, prefix="/api/v1/motors", tags=["motors-test"])
    app.include_router(motors.router, prefix="/api/v1/motors", tags=["motors"])
    print("✅ Motors router loaded successfully")
except ImportError as e:
    print(f"⚠️  Motors router not found: {e}")
except Exception as e:
    print(f"❌ Error loading motors router: {e}")
    

# Segmentation Router
try:
    app.include_router(segmentation.router, prefix="/api/v1/segmentation", tags=["segmentation"])
    print("✅ Segmentation router loaded successfully")
except ImportError as e:
    print(f"⚠️  Segmentation router not found: {e}")
except Exception as e:
    print(f"❌ Error loading segmentation router: {e}")

# ============================================
# 6) ROOT ENDPOINTS
# ============================================

@app.get("/")
async def root():
    return {
        "message": "End.STP API - 4 Motors + Segmentation + Admin Panel",
        "version": "1.0.0",
        "docs": "/api/docs",
        "motors": ["BS-Model", "Difficulty", "Time", "Priority"],
        "meta_motor": "Segmentation",
        "admin_panel": "enabled"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "motors": 4, "meta_motor": "segmentation", "admin": "enabled"}
