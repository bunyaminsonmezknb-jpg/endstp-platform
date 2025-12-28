# 🏗️ Motor Version Strategy

## 🎯 Philosophy

### v1 = KEMİK SİSTEM (Foundation)
```
STABLE | FAST | RELIABLE | FALLBACK
```

**Characteristics:**
- ⚡ Response time: <50ms guaranteed
- 🛡️ Never crash (defensive programming)
- 🎯 Single responsibility: Core calculation
- 🔒 LTS (Long Term Support)

**Change Policy:**
- ✅ **ALLOWED:**
  - Bug fixes (crash prevention)
  - Input validation (edge cases)
  - Error handling improvements
  - Performance optimization (without breaking)
  - Documentation updates
  - Test coverage improvements

- ❌ **FORBIDDEN:**
  - New feature additions (→ go to v2)
  - Algorithm modifications (stability first)
  - Breaking changes (API compatibility sacred)
  - Performance degradation (speed is king)

**Release Cadence:** Quarterly (bug fixes only)

---

### v2 = İNOVASYON LAB (Evolution)
```
ADVANCED | EVOLVING | EXPERIMENTAL | FEATURES
```

**Characteristics:**
- 🚀 Cutting-edge features
- 🧠 ML/AI integration
- 🔬 Experimental algorithms
- 📈 Continuous improvement

**Change Policy:**
- ✅ **ENCOURAGED:**
  - New feature additions
  - ML model integration
  - Advanced analytics
  - Breaking changes (with major version bump)
  - Performance experiments

- ⚠️ **REQUIREMENTS:**
  - Must maintain v1 API compatibility (wrapper)
  - Timeout handling (fallback to v1)
  - Feature flags (tier-based)
  - Comprehensive testing (v2 fail → v1 win)

**Release Cadence:** Continuous (rolling release)

---

## 🛡️ Fallback Strategy
```
User Request
    ↓
Tier Check (FREE/BASIC/PREMIUM)
    ↓
┌─────────────────────────────┐
│  Try v2 (if tier allows)    │
│  ↓                           │
│  Success? → Return result    │
│  ↓                           │
│  Timeout/Error?              │
│  ↓                           │
│  FALLBACK TO v1 (KEMİK)     │ ← Never fails!
│  ↓                           │
│  Return safe result          │
└─────────────────────────────┘
```

**Why this works:**
- v1 = Minimal features, always succeeds
- v2 = Rich features, might fail/timeout
- User always gets an answer

---

## 📊 Version Matrix

| Tier | Motor | Features | Response Time | Fallback |
|------|-------|----------|---------------|----------|
| FREE | v1 | 4 core | <50ms | N/A |
| BASIC | v2 | 8 enhanced | <150ms | → v1 |
| PREMIUM | v2 | 15 full | <500ms | → v1 |

---

## 🔢 Semantic Versioning

### v1.x.x (LTS)
```
1.0.0 → Initial stable release
1.0.1 → Bug fix (blank_rate validation)
1.0.2 → Edge case (zero tests)
1.1.0 → Minor improvement (0-130 scale)
1.2.0 → Performance optimization
```

### v2.x.x (Rolling)
```
2.0.0 → Initial advanced version
2.1.0 → Add prerequisite + bs_model features
2.2.0 → Add ML prediction
2.3.0 → Add AI insights
3.0.0 → Breaking change (major refactor)
```

---

## 👥 Governance

### v1 Changes (Strict)
1. **Proposal:** Submit change request
2. **Review:** Two-person approval required
3. **Testing:** 95%+ coverage required
4. **Approval:** Security + Performance checks
5. **Deploy:** Staged rollout (staging → prod)

### v2 Changes (Flexible)
1. **Proposal:** Feature specification
2. **Review:** One-person approval
3. **Testing:** 85%+ coverage required
4. **Approval:** Functional checks
5. **Deploy:** Direct to staging, A/B test

---

## 📈 Success Metrics

### v1 KPIs
- ✅ Zero crashes (100% uptime)
- ✅ <50ms response time (99th percentile)
- ✅ Fallback success rate (100%)

### v2 KPIs
- ✅ Feature adoption rate (by tier)
- ✅ Accuracy improvement vs v1
- ✅ Timeout rate (<5%)

---

## 🎓 Example: Adding a Feature

### ❌ WRONG (Adding to v1)
```python
# difficulty_engine.py (v1)
def calculate_difficulty_score(tests):
    # ❌ DON'T DO THIS!
    prerequisite_weakness = analyze_prerequisites()
    # This belongs in v2!
```

### ✅ CORRECT (Adding to v2)
```python
# difficulty_engine_v2.py (v2)
class MasterDifficultyEngine:
    FEATURES = {
        # ... existing
        "prerequisite": {  # NEW!
            "enabled_tiers": ["basic", "premium"],
            "version": "2.4.0"
        }
    }
```

---

**Last Updated:** December 28, 2024  
**Maintainers:** End.STP Core Team
