// 🎯 Today's Tasks Data Types
// Backend endpoint: GET /api/v1/student/todays-tasks

export interface TopicAtRisk {
  topic_id: string;
  topic_name: string;
  subject: string;
  retention_rate: number; // 0-100
  days_until_forgotten: number; // Calculated from forgetting curve
  last_studied: string; // ISO date
  difficulty_score: number; // 0-100
  priority_score: number; // 0-100
}

export interface PriorityTopic {
  topic_id: string;
  topic_name: string;
  subject: string;
  priority_score: number; // 0-100
  priority_reason: 'difficulty' | 'retention' | 'prerequisite' | 'never_studied';
  difficulty_score: number; // 0-100
  retention_rate: number; // 0-100
  estimated_study_time: number; // minutes
}

export interface StudyStreak {
  current_streak: number; // days
  longest_streak: number; // days
  streak_status: 'active' | 'at_risk' | 'broken';
  last_study_date: string; // ISO date
  next_milestone: number; // days (e.g., 7, 14, 30)
}

export interface TimeStats {
  total_study_time_today: number; // minutes
  total_study_time_week: number; // minutes
  avg_daily_time: number; // minutes
  target_daily_time: number; // minutes (e.g., 120)
  time_efficiency: number; // 0-100 percentage
}

export interface TodaysTasksData {
  // Card 1: Unutulmaya Yakın Konular
  at_risk_topics: TopicAtRisk[];
  total_at_risk: number;

  // Card 2: Bugün Çalışılacak Konular
  priority_topics: PriorityTopic[];
  total_priority: number;

  // Card 3: Zaman Durumu
  streak: StudyStreak;
  time_stats: TimeStats;

  // Metadata
  generated_at: string; // ISO timestamp
  student_id: string;
}

// API Response wrapper
export interface TodaysTasksResponse {
  success: boolean;
  data: TodaysTasksData;
  message?: string;
  error?: string;
}