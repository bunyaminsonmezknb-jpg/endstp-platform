# 🗺️ END.STP ROADMAP & TECHNICAL DECISIONS

## 🎯 CURRENT STATUS (December 2024)

**Phase:** MVP Development
**Infrastructure Decision:** Single Supabase Project (dev + prod combined)
**Reason:** Solo developer, no real users yet, MVP validation phase

---

## 🚨 PRODUCTION DATABASE SEPARATION - TRIGGER CONDITIONS

**Decision Date:** 2024-12-18
**Current:** Using single Supabase project for both dev and prod
**Future:** Will migrate to separate production DB when ANY of these triggers occur:

### **TRIGGERS TO CREATE SEPARATE PRODUCTION DB:**

1. 💰 **First Payment Received**
   - Any paying customer
   - Subscription started
   - Financial commitment exists

2. 👥 **10-20 Active Students**
   - Real users (not test accounts)
   - Daily active usage
   - Data becomes critical

3. ⏱️ **Daily Query Volume > 50K Rows**
   - Performance bottleneck
   - Scaling needed
   - Database optimization required

4. 🤖 **AI Automation v2 Launch**
   - Advanced features
   - Production stability critical
   - Rollback safety needed

5. 👨‍💼 **Team Expansion**
   - Second developer joins
   - Multiple environments needed
   - Dev/staging/prod separation

### **WHEN TRIGGERED, ACTION PLAN:**
```bash
# 1. Create new Supabase project
- Name: end-stp-production
- Region: Europe (Frankfurt/London)
- Separate connection strings

# 2. Migration strategy
- Export data from current project
- Run migrations on new prod DB
- Test thoroughly
- Switch connection strings

# 3. Environment separation
- .env.development → current project
- .env.production → new project
- Deploy configs updated
```

---

## 📋 CURRENT MVP GUIDELINES

### **1. Environment Separation (Logical)**
```python
# backend/.env
APP_ENV=development  # or production

# Mark data with environment
{
  "student_id": "...",
  "environment": "dev",  # or "prod"
  "is_test_data": false
}
```

### **2. Migration Discipline**

✅ **Always use:**
- `CREATE TABLE IF NOT EXISTS`
- `ALTER TABLE ... ADD COLUMN IF NOT EXISTS`
- `ON CONFLICT DO NOTHING`

❌ **Avoid:**
- `DROP TABLE` without `IF EXISTS`
- Destructive changes without backup
- Non-idempotent migrations

### **3. Production Mindset**

- ✅ RLS policies: Correct from day 1
- ✅ Auth system: Production-grade now
- ✅ Feature flags: Toggle freely
- ✅ Demo data: Safe to delete/recreate

### **4. Feature Control System**

Our feature flag system already handles:
- Health monitoring
- Auto-disable on critical errors
- Environment-aware toggles
- Zero downtime feature management

---

## 🎯 NEXT MILESTONES

### **MVP (Current)**
- [x] Feature flag system ✅
- [x] Student dashboard ✅
- [x] Test entry ✅
- [ ] Backend deployment
- [ ] Frontend deployment (Vercel)
- [ ] First real user test

### **v1.1 (Post-MVP)**
- [ ] Goal tracking UI
- [ ] Task reasoning tooltips
- [ ] Error timeline visualization
- [ ] Direct Claude API integration

### **v2 (Scaling Phase)**
- [ ] Separate production database ⚠️ TRIGGERED BY CONDITIONS ABOVE
- [ ] Coach/institution dashboards
- [ ] API commercialization
- [ ] Mobile app
- [ ] Global expansion (non-TR markets)

---

## 🔒 TECHNICAL DEBT TRACKING

### **Intentional Shortcuts (with exit plan):**

1. **Single Supabase Project**
   - Current: dev + prod combined
   - Exit: When triggers above occur
   - Effort: 1-2 days migration

2. **No separate staging environment**
   - Current: dev → prod directly
   - Exit: When team > 1 person
   - Effort: 4 hours setup

3. **Manual deployment**
   - Current: Local → production manual
   - Exit: When daily deployments needed
   - Effort: CI/CD pipeline (1 day)

---

## 📝 DECISION LOG

| Date | Decision | Reason | Review Date |
|------|----------|--------|-------------|
| 2024-12-18 | Single Supabase project | Solo dev, MVP phase | First payment or 20 users |
| 2024-12-18 | Feature flag system | Production control, AI diagnostics | - |
| 2024-12-18 | No Supabase CLI | Permission issues, SQL Editor simpler | - |

---

**Last Updated:** 2024-12-18
**Next Review:** When first trigger condition occurs

