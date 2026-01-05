# 🔍 ROOT CAUSE DEBUG PROTOCOL - Motor v2 Permission Issue

## 📊 CURRENT STATUS
- ✅ Motors working with GRANT workaround
- ❌ Don't know WHY service_role needed explicit GRANT
- ⚠️ Not sustainable for production

---

## 🎯 4-STEP PROTOCOL TO FIND ROOT CAUSE

### STEP 1: DB Current Role Verification (CRITICAL)

**1.1. Create RPC Function in Supabase:**
```sql
CREATE OR REPLACE FUNCTION current_role()
RETURNS text
LANGUAGE sql
AS $$
  SELECT current_role;
$$;

-- Test it
SELECT current_role();
-- Expected: 'service_role'
```

**1.2. Add to ContextService __init__:**
```python
# Temporary diagnostic
res = self.supabase.rpc("current_role").execute()
logger.critical(f"🔥 DB CURRENT ROLE: {res.data}")
```

**1.3. Expected Results:**
- ✅ `service_role` → Client is correct, investigate Supabase project config
- ❌ `authenticated` or `anon` → Client is wrong, find where header override happens

---

### STEP 2: JWT Decode Verification

**Terminal:**
```bash
python << 'PY'
import os, jwt
from dotenv import load_dotenv
load_dotenv()

key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
payload = jwt.decode(key, options={"verify_signature": False})
print(f"Role in JWT: {payload.get('role')}")
PY
```

**Expected:** `Role in JWT: service_role`

---

### STEP 3: Force Clean Client (No Headers)

**Modify get_supabase_admin temporarily:**
```python
def get_supabase_admin() -> Client:
    """DIAGNOSTIC: Force clean service_role client"""
    import os
    from supabase import create_client
    
    return create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_SERVICE_ROLE_KEY"),
        options={
            "global": {
                "headers": {}  # 🔥 NO HEADERS
            }
        }
    )
```

---

### STEP 4: Isolated Test (No Motors, No Context)

**Terminal:**
```python
from app.db.session import get_supabase_admin

sb = get_supabase_admin()
print(sb.table("prerequisites").select("id").limit(1).execute())
```

**Expected:**
- ✅ Data returned → service_role works
- ❌ permission denied → client NOT admin

---

## 🧠 DIAGNOSTIC DECISION TREE
```
Run current_role()
    │
    ├─ "service_role"
    │   ├─ Still permission denied?
    │   │   └─ Supabase project config issue
    │   │       → Check project policies
    │   │       → Contact Supabase support
    │   │
    │   └─ Works now?
    │       └─ Header contamination was the issue
    │           → Add clean headers permanently
    │
    └─ "authenticated" or "anon"
        └─ Client is NOT admin
            ├─ Check: .env key is really service_role (JWT decode)
            ├─ Check: No middleware overriding client
            ├─ Check: No request.state.supabase injection
            └─ Check: Supabase Python client version
```

---

## 📝 FINDINGS LOG

| Test | Result | Conclusion |
|------|--------|------------|
| current_role() | ? | ? |
| JWT decode | ✅ service_role | Key is correct |
| Clean headers | ? | ? |
| Isolated test | ? | ? |

---

## ✅ SUCCESS CRITERIA

**Root cause found when:**
1. We know EXACTLY which role DB sees
2. We know WHY it's not service_role (if it isn't)
3. We have SUSTAINABLE fix (not GRANT workaround)

**Acceptable solutions:**
- ✅ Header cleanup in client options
- ✅ Supabase client version upgrade
- ✅ Project-level policy fix
- ❌ GRANT workaround (temporary only)

---

## 🚀 TOMORROW'S PLAN

**Morning (30 min):**
1. Create current_role() function
2. Add diagnostic logs
3. Run all 4 tests
4. Document findings

**Afternoon (1 hour):**
1. Based on findings, implement proper fix
2. Remove GRANT workaround
3. Re-enable RLS (if needed)
4. Verify all motors still work

**Goal:** Production-ready context service without workarounds

---

**Created:** 2025-01-04 Evening
**Status:** Ready for tomorrow's debug session
