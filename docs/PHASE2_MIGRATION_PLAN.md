======================================================================
PHASE 2 I18N MIGRATION REPORT
Generated: 2025-12-24 22:11:26 UTC
======================================================================

📊 SUMMARY
----------------------------------------------------------------------
Total items found: 6
  - DATE_FORMATTING: 3
  - GENERAL: 3

📋 MIGRATION ITEMS
----------------------------------------------------------------------

1. [GENERAL] backend/app/api/v1/endpoints/progress/calculators.py:17
   # TODO: PHASE-2-I18N - Replace with database-driven translations


2. [DATE_FORMATTING] backend/app/api/v1/endpoints/progress/calculators.py:29
   # TODO: PHASE-2-I18N - Rename to format_date_localized and add language parameter


3. [GENERAL] backend/app/api/v1/endpoints/progress/calculators.py:93
   # TODO: PHASE-2-I18N - These strings should come from translations


4. [GENERAL] backend/app/api/v1/endpoints/progress/calculators.py:124
   # TODO: PHASE-2-I18N - Phase names and disclaimers should be localized


5. [DATE_FORMATTING] backend/app/api/v1/endpoints/progress/calculators.py:250
   # TODO: PHASE-2-I18N - Replace with: labels = [await format_date_localized(p, language, "short") for p in period_starts]


6. [DATE_FORMATTING] backend/app/api/v1/endpoints/progress/calculators.py:254
   # TODO: PHASE-2-I18N - Replace with: labels = [await format_date_localized(p, language, "long") for p in period_starts]


======================================================================
🚀 MIGRATION STEPS (Phase 2)
======================================================================

BACKEND:
  1. Create database migration (languages + translations tables)
  2. Implement get_translation() function
  3. Replace TURKISH_MONTHS with database lookups
  4. Add language parameter to all affected functions
  5. Update API endpoints with Accept-Language header

FRONTEND:
  6. Install next-intl
  7. Create locales/ directory structure
  8. Implement LanguageProvider context
  9. Create LanguageSwitcher component
  10. Replace all hardcoded text with t() calls

TESTING:
  11. Test all date displays in tr/en
  12. Test language switching
  13. Test API responses with different Accept-Language
  14. Performance test (database lookups)
