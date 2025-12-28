# Version Governance Rules

## 🔐 Change Approval Matrix

| Version | Change Type | Approval | Test Coverage | Review Time |
|---------|-------------|----------|---------------|-------------|
| v1 | Bug fix | 2 people | 95%+ | 2 days |
| v1 | Edge case | 2 people | 95%+ | 2 days |
| v1 | Performance | 2 people + benchmark | 95%+ | 3 days |
| v2 | New feature | 1 person | 85%+ | 1 day |
| v2 | ML model | 1 person + data review | 85%+ | 2 days |
| v2 | Breaking change | 2 people | 90%+ | 3 days |

## 📝 Change Request Template
```markdown
## Change Request: [TITLE]

**Version:** v1.0.1 or v2.4.0
**Type:** Bug Fix / Feature / Performance / Breaking Change
**Priority:** Critical / High / Medium / Low

### Problem Statement
[What is broken or missing?]

### Proposed Solution
[How will you fix it?]

### Testing Plan
[How will you verify it works?]

### Rollback Plan
[What if it breaks production?]

### Approval
- [ ] Reviewer 1: @username
- [ ] Reviewer 2: @username (v1 only)
- [ ] Test Coverage: XX%
- [ ] Performance Benchmark: [results]
```

## 🚦 Deployment Pipeline

### v1 (Strict)
```
1. Local dev → pytest (95%+)
2. Staging → load test (1000 req/s)
3. Production (10% traffic) → monitor 24h
4. Production (100% traffic)
```

### v2 (Flexible)
```
1. Local dev → pytest (85%+)
2. Staging → A/B test
3. Production (feature flag)
```

---

**Enforcement:** Automated CI/CD checks
**Last Updated:** December 28, 2024
