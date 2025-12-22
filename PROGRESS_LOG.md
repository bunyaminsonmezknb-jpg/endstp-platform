# Progress Log

## 2024-12-23 - Exam Weight System + Subject Accordion

### Database Changes (Supabase SQL Editor)
- ✅ `subject_exam_weights` table created
- ✅ TYT exam weights: 9 subjects, 120 questions
- ✅ AYT_SAY exam weights: 4 subjects, 80 questions
- ✅ AYT_EA exam type + weights: 4 subjects, 80 questions
- ✅ AYT_SOZ exam type + weights: 7 subjects, 80 questions
- ✅ Exam types: AYT_EA, AYT_SOZ added
- ✅ Subjects added: TDE, TAR1, TAR2, COG1, COG2, FEL_GRUP, DIN

### Known Issues
- ⚠️ Fizik subject has 3 duplicates (physics_basics: 72 topics, physics: 55 topics, FIZ: 0 topics)
- ⚠️ TYT shows 127 questions (should be 120) due to Fizik duplicate
- ⚠️ Need to merge Fizik subjects

### Next Session (2024-12-24)
1. Merge 3 Fizik subjects into FIZ
2. Fix TYT total to 120 questions
3. Add exam weight to priority score calculation
4. Frontend: topics_tested/topics_total format
5. Frontend: Ustalık detailed tooltip
