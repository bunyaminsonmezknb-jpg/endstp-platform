INSERT INTO feature_flags (flag_key, description, is_enabled, phase) VALUES
('test_entry', 'Test Entry System', true, 'mvp'),
('at_risk_display', 'At-Risk Topics Card', true, 'mvp'),
('daily_tasks', 'Bugünkü Görevler', true, 'mvp'),
('mini_progress', 'Mini Progress (7 days)', true, 'mvp'),
('topic_detail', 'Konu Detayı', true, 'mvp'),
('motor_driven_tasks', 'Motor task generation', false, 'mvp'),
('difficulty_calculation', 'Difficulty Motor', true, 'mvp'),
('time_analysis', 'Time Analyzer', true, 'mvp'),
('goal_cards', 'Hedef Kartları', false, 'v1.1'),
('task_reasoning', 'Task Tooltips', false, 'v1.1'),
('projection_display', 'Projection UI', false, 'v2')
ON CONFLICT (flag_key) DO NOTHING;
