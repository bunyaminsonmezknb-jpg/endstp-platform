/**
 * API Client for End.STP Backend
 * Handles all HTTP requests to FastAPI backend
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

/**
 * Get student dashboard data
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
