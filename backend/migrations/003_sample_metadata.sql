UPDATE feature_flags SET
  component_path = 'frontend/app/student/dashboard/components/TodayStatusCards.tsx',
  backend_endpoint = '/api/v1/student/tasks/today',
  related_files = ARRAY['backend/app/api/v1/endpoints/student/tasks.py', 'frontend/app/student/dashboard/components/TodayStatusCards.tsx'],
  fix_guide = 'Check generate_motor_driven_tasks() in tasks.py line 340. SQL query may timeout with large datasets.',
  error_severity = 'medium',
  user_impact_level = 'high',
  depends_on = ARRAY['test_entry', 'at_risk_display'],
  avg_response_time_ms = 1450,
  p95_response_time_ms = 3200,
  rows_processed = 120000,
  last_error_message = 'TimeoutError: SQL query exceeded 30s timeout',
  last_error_function = 'generate_motor_driven_tasks() - tasks.py:340',
  latency_score = 40,
  error_score = 70,
  data_volume_score = 30
WHERE flag_key = 'daily_tasks';

UPDATE feature_flags SET
  component_path = 'frontend/app/student/dashboard/components/AtRiskCard.tsx',
  backend_endpoint = '/api/v1/student/todays-tasks',
  related_files = ARRAY['backend/app/api/v1/endpoints/student/tasks.py'],
  fix_guide = 'BS-Motor forgetting curve calculation in utils.py.',
  user_impact_level = 'critical',
  avg_response_time_ms = 350,
  latency_score = 95
WHERE flag_key = 'at_risk_display';
