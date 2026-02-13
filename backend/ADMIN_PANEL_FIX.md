# Admin Panel Permission Fix - Complete Log

## Phase 1: SELECT GRANT + CORS (Commit: admin-panel-select-grant-fixed)

**Date:** 2026-02-13

### Problem
- Frontend: "Failed to fetch"
- Backend: 500 Internal Server Error
- Error: `permission denied for table user_profiles/admin_feature_flags/dashboard_settings`
- CORS blocked

### Solution

**1. Database (Supabase SQL):**
```sql
-- SELECT permissions
GRANT SELECT ON TABLE public.user_profiles TO service_role;
GRANT SELECT ON TABLE public.admin_feature_flags TO service_role;
GRANT SELECT ON TABLE public.dashboard_settings TO service_role;
```

**2. Backend (main.py):**
```python
# CORS fix
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)
```

**3. Test Results:**
- ✅ GET /admin/feature-flags → 200 OK
- ✅ GET /admin/dashboard/settings → 200 OK
- ✅ Frontend pages load

---

## Phase 2: UPDATE GRANT (Current)

**Date:** 2026-02-13

### Problem
- Toggle feature flags → 500 error
- Save dashboard settings → 500 error
- Error: `permission denied for table admin_feature_flags/dashboard_settings` (UPDATE)

### Solution

**Database (Supabase SQL):**
```sql
-- UPDATE permissions
GRANT UPDATE ON TABLE public.admin_feature_flags TO service_role;
GRANT UPDATE ON TABLE public.dashboard_settings TO service_role;

-- Verify
SELECT grantee, privilege_type
FROM information_schema.table_privileges
WHERE table_name IN ('admin_feature_flags', 'dashboard_settings')
  AND grantee = 'service_role'
ORDER BY table_name, privilege_type;

-- Result:
-- admin_feature_flags | service_role | SELECT
-- admin_feature_flags | service_role | UPDATE
-- dashboard_settings  | service_role | SELECT
-- dashboard_settings  | service_role | UPDATE
```

**Test Results:**
- ✅ PUT /admin/feature-flags/{flag_key} → 200 OK
- ✅ PUT /admin/dashboard/settings → 200 OK
- ✅ Toggle enable/disable works
- ✅ Save settings works

---

## Status: ✅ COMPLETE

**Admin panel fully operational:**
- Feature flags: GET + PUT working
- Dashboard settings: GET + PUT working
- Toggle operations: Working
- CORS: Fixed
- Auth guard: Working

**Next:** L5 SQLAlchemy migration (planned this week)

---

**Branch:** feature/audit-sqlalchemy  
**Tags:** admin-panel-select-grant-fixed  
**Author:** End.STP Team  
**Date:** 2026-02-13

