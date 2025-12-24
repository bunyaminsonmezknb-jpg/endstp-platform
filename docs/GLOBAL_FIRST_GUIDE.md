# 🌍 GLOBAL-FIRST Development Guide

## Overview

End.STP is built with GLOBAL-FIRST principles to support international expansion from day one. This guide ensures all new code is globally compatible.

---

## ✅ GOLDEN RULES

### 1. UTC Datetime Handling

**❌ WRONG:**
```python
from datetime import datetime

now = datetime.now()  # Local timezone!
```

**✅ CORRECT:**
```python
from datetime import datetime, timezone

now = datetime.now(timezone.utc)  # Always UTC!
```

### 2. Language Support

**❌ WRONG:**
```python
return {"message": "Test başarıyla kaydedildi"}
```

**✅ CORRECT (Phase 1 - MVP):**
```python
# TODO: PHASE-2-I18N - Replace with translation lookup
# ALLOWED: Temporary hardcoded for MVP
return {"message": "Test başarıyla kaydedildi"}
```

**✅ CORRECT (Phase 2+):**
```python
message = await get_translation("success.test_saved", language)
return {"message": message}
```

### 3. Database Columns

**❌ WRONG:**
```sql
CREATE TABLE subjects (
  name TEXT  -- Single language!
);
```

**✅ CORRECT:**
```sql
CREATE TABLE subjects (
  name_tr TEXT,
  name_en TEXT
);
```

### 4. Date Formatting

**❌ WRONG:**
```python
label = date.strftime("%d %B")  # OS locale-dependent!
```

**✅ CORRECT (Phase 1):**
```python
# TODO: PHASE-2-I18N
label = format_date_turkish(date, "short")
```

**✅ CORRECT (Phase 2+):**
```python
label = await format_date_localized(date, language, "short")
```

---

## 🔍 PRE-COMMIT CHECKLIST

Before every commit, verify:

- [ ] All `datetime.now()` uses `timezone.utc`
- [ ] No hardcoded Turkish text (or has `TODO: PHASE-2-I18N`)
- [ ] Multi-language columns used (`_tr`, `_en`)
- [ ] API endpoints accept `Accept-Language` header (Phase 2+)
- [ ] Timezone conversion documented

**Automated:** Pre-commit hook will check these automatically!

---

## 📋 MIGRATION TAGS

Use TODO tags for temporary hardcoded solutions:
```python
# TODO: PHASE-2-I18N - Brief description
# MIGRATION-GUIDE:
#   1. Specific step
#   2. Another step
# ALLOWED: Justification for temporary solution
HARDCODED_VALUE = ...
```

**Find all migration items:**
```bash
python scripts/migrate_to_i18n.py
```

---

## 🚀 PHASE TIMELINE

### Phase 1 (MVP - Current)
- Hardcoded Turkish with TODO tags
- UTC-aware datetime everywhere
- Database columns ready (_tr, _en)

### Phase 2 (Post-MVP)
- Database-driven translations
- Language parameter in APIs
- Frontend i18n (next-intl)

### Phase 3 (Global Expansion)
- 5+ language support
- Admin translation management
- RTL support (Arabic)

---

## 📞 SUPPORT

Questions? Check:
- `ENDSTP_MASTER_CONTEXT.md` - Architecture decisions
- `scripts/migrate_to_i18n.py` - Migration planning
- Pre-commit hook - Automated checks

**Remember:** Every line of code should be globally compatible!
