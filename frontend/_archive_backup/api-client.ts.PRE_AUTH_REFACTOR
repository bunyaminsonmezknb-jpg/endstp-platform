/**
 * API Client for End.STP Backend
 * Handles all HTTP requests to FastAPI backend
 * 
 * UPDATED: 4 Motor Analysis endpoint eklendi
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface ApiResponse<T> {
  data: T | null;
  error: string | null;
  status: number;
}

/**
 * Generic fetch wrapper with error handling
 */
async function fetchApi<T>(
  endpoint: string,
  options?: RequestInit
): Promise<ApiResponse<T>> {
  try {
    // Get token from localStorage (only in browser)
    const token = typeof window !== 'undefined'
      ? localStorage.getItem('access_token')
      : null;

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...options?.headers,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      return {
        data: null,
        error: errorData.detail || `HTTP ${response.status}: ${response.statusText}`,
        status: response.status,
      };
    }

    const data = await response.json();
    return {
      data,
      error: null,
      status: response.status,
    };
  } catch (error) {
    console.error('API Error:', error);
    return {
      data: null,
      error: error instanceof Error ? error.message : 'Network error',
      status: 0,
    };
  }
}

// ============================================
// ESKİ ENDPOINT'LER (DEĞİŞMEDİ - DOKUNMAYIN)
// ============================================

/**
 * Get student dashboard data (ESKİ SİSTEM)
 */
export async function getStudentDashboard(studentId: number) {
  return fetchApi(`/api/v1/student/${studentId}/dashboard`);
}

/**
 * Get recovery plan (partner links) for a topic
 */
export async function getRecoveryPlan(studentId: number, topicId: number) {
  return fetchApi(`/api/v1/student/${studentId}/topic/${topicId}/recovery-plan`);
}

/**
 * Update topic status after study completion
 */
export async function updateTopicStatus(
  studentId: number,
  topicId: number,
  newRememberingRate: number,
  studyCompleted: boolean
) {
  return fetchApi(`/api/v1/student/${studentId}/topic/update`, {
    method: 'POST',
    body: JSON.stringify({
      topic_id: topicId,
      new_remembering_rate: newRememberingRate,
      study_completed: studyCompleted,
    }),
  });
}

/**
 * Health check
 */
export async function healthCheck() {
  return fetchApi('/health');
}

// ============================================
// YENİ: 4 MOTOR ANALİZ ENDPOINT'İ
// ============================================

/**
 * Topic Test Input for 4 Motor Analysis
 */
export interface TopicTestInput {
  topic_id: number;
  topic_name: string;
  correct: number;
  incorrect: number;
  blank: number;
  total_questions: number;
  
  // BS-Model için (opsiyonel)
  current_ease_factor?: number;
  current_interval?: number;
  actual_gap_days?: number;
  repetitions?: number;
  
  // Time Analyzer için (opsiyonel)
  duration_minutes?: number;
  
  // Priority için (opsiyonel)
  topic_weight?: number;
  course_importance?: number;
  difficulty_baseline?: number;
}

/**
 * 4 Motor Analysis Response - Tek Konu
 */
export interface TopicAnalysisOutput {
  topic_id: number;
  topic_name: string;
  next_review_date: string;
  next_ease_factor: number;
  next_interval: number;
  status: string;
  difficulty_level: number;
  difficulty_percentage: number;
  pace_ratio: number;
  time_modifier: number;
  speed_note: string;
  priority_score: number;
  priority_level: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  suggestion: string;
}

/**
 * 4 Motor Analysis Response - Tam
 */
export interface MotorAnalysisResponse {
  student_id: string;
  analyzed_at: string;
  topics: TopicAnalysisOutput[];
  summary: {
    total_topics: number;
    critical_topics: number;
    high_priority_topics: number;
    next_review_today: number;
  };
}

/**
 * YENİ: 4 Motor ile Öğrenci Analizi
 * 
 * @example
 * const result = await getMotorAnalysis([
 *   {
 *     topic_id: 1,
 *     topic_name: "Türev",
 *     correct: 5,
 *     incorrect: 3,
 *     blank: 2,
 *     total_questions: 10,
 *     duration_minutes: 15
 *   }
 * ]);
 */
export async function getMotorAnalysis(topics: TopicTestInput[]): Promise<ApiResponse<MotorAnalysisResponse>> {
  // Get student ID from localStorage
  const userStr = typeof window !== 'undefined' ? localStorage.getItem('user') : null;
  const studentId = userStr ? JSON.parse(userStr).id : 'unknown';
  
  return fetchApi('/api/v1/student/analyze', {
    method: 'POST',
    body: JSON.stringify({
      student_id: studentId,
      topics: topics
    })
  });
}

/**
 * YENİ: Motor Health Check
 */
export async function getMotorHealth() {
  return fetchApi('/api/v1/student/health');
}
