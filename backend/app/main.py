"""
End.STP Backend API
FastAPI ana uygulama - 4 Motor Sistemi
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.api.v1.student_analysis import router as student_router
import time
from contextlib import asynccontextmanager

# ============================================
# 1. APP TANIMI
# ============================================

app = FastAPI(
    title="End.STP API",
    description="Akıllı Öğrenme Analiz Sistemi - 4 Motors",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# ============================================
# 2. CORS MIDDLEWARE
# ============================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# 3. MONITORING MIDDLEWARE
# ============================================

async def report_slow_endpoint(path: str, response_time_ms: int):
    """Report slow response time to feature flags"""
    try:
        flag_key = None
        if "/student/tasks/today" in path:
            flag_key = "daily_tasks"
        elif "/student/todays-tasks" in path:
            flag_key = "at_risk_display"
        elif "/test-entry" in path:
            flag_key = "test_entry"
        
        if flag_key:
            from app.db.session import get_supabase_admin
            supabase = get_supabase_admin()
            
            supabase.table("feature_flags").update({
                "avg_response_time_ms": response_time_ms,
                "last_success_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")
            }).eq("flag_key", flag_key).execute()
            
            print(f"⚠️ SLOW: {flag_key} took {response_time_ms}ms")
    except Exception as e:
        print(f"Monitoring error: {e}")

async def report_endpoint_error(path: str, error: str, response_time_ms: int):
    """Report error to feature flags"""
    try:
        flag_key = None
        if "/student/tasks/today" in path:
            flag_key = "daily_tasks"
        elif "/student/todays-tasks" in path:
            flag_key = "at_risk_display"
        elif "/test-entry" in path:
            flag_key = "test_entry"
        
        if flag_key:
            from app.db.session import get_supabase_admin
            supabase = get_supabase_admin()
            
            result = supabase.table("feature_flags").select("error_count, health_score").eq("flag_key", flag_key).execute()
            if result.data:
                current = result.data[0]
                new_error_count = current["error_count"] + 1
                new_health = max(0, current["health_score"] - 10)
                
                supabase.table("feature_flags").update({
                    "error_count": new_error_count,
                    "health_score": new_health,
                    "last_error_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "last_error_message": str(error)[:500],
                    "avg_response_time_ms": response_time_ms
                }).eq("flag_key", flag_key).execute()
                
                print(f"🚨 ERROR: {flag_key} - {error}")
    except Exception as e:
        print(f"Error reporting failed: {e}")

@app.middleware("http")
async def monitor_response_time(request, call_next):
    start_time = time.time()
    
    try:
        response = await call_next(request)
        process_time = int((time.time() - start_time) * 1000)  # ms
        response.headers["X-Process-Time"] = str(process_time)
        
        # Report slow endpoints (background task)
        if process_time > 1000:
            await report_slow_endpoint(request.url.path, process_time)
        
        return response
        
    except Exception as e:
        process_time = int((time.time() - start_time) * 1000)
        await report_endpoint_error(request.url.path, str(e), process_time)
        raise

# ============================================
# 4. ROUTERS (Sıralama önemli!)
# ============================================

# Eski sistem routers
app.include_router(api_router, prefix="/api/v1")
app.include_router(student_router)

# Progress router (YENİ - try-catch ile güvenli)
# Progress router (MODULAR)
try:
    from app.api.v1.endpoints.progress import router as progress_router
    app.include_router(
        progress_router, 
        prefix="/api/v1",  # ← BU DOĞRU
        tags=["progress"]
    )
    
    print("✅ Progress router loaded successfully")
except ImportError as e:
    print(f"⚠️  Progress router not found: {e}")
except Exception as e:
    print(f"❌ Error loading progress router: {e}")

# ============================================
# 5. ROOT ENDPOINTS
# ============================================

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
# ============================================
# 6. MOTOR ROUTER (YENİ!)
# ============================================

try:
    from app.api.v1.endpoints import motors, motor_health, motor_test
    
    # Motor Health Endpoints
    app.include_router(
        motor_health.router,
        prefix="/api/v1/motors",
        tags=["motor-health"]
    )
    
    # Motor Test Endpoints (Logging Test)
    app.include_router(
        motor_test.router,
        prefix="/api/v1/motors",
        tags=["motors-test"]
    )
    
    # Main Motors Endpoints
    app.include_router(
        motors.router,
        prefix="/api/v1/motors",
        tags=["motors"]
    )
    print("✅ Motors router loaded successfully")
except ImportError as e:
    print(f"⚠️  Motors router not found: {e}")
except Exception as e:
    print(f"❌ Error loading motors router: {e}")
