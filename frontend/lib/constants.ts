/**
 * Global Constants
 * Magic string'leri önlemek için tek kaynak noktası
 */

// LocalStorage Keys
export const STORAGE_KEYS = {
  ACCESS_TOKEN: 'access_token',
  USER: 'user',
  REFRESH_TOKEN: 'refresh_token',
} as const;

// API Endpoints
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const API_ENDPOINTS = {
  STUDENT_DASHBOARD: (studentId: string) => `/api/v1/student/${studentId}/dashboard`,
  STUDENT_PROFILE: (studentId: string) => `/api/v1/student/${studentId}/profile`,
  TEST_RESULTS: '/api/v1/test-results',
  AUTH_LOGIN: '/api/v1/auth/login',
  AUTH_SIGNUP: '/api/v1/auth/signup',
  SUBJECTS: '/api/v1/subjects',
  TOPICS: (subjectId: string) => `/api/v1/subjects/${subjectId}/topics`,
} as const;

// Topic Status Values (Runtime Validation için)
export const VALID_TOPIC_STATUSES = ['critical', 'warning', 'good', 'excellent', 'frozen'] as const;
export type ValidTopicStatus = typeof VALID_TOPIC_STATUSES[number];

// Default değerler
export const DEFAULTS = {
  DAYS_SINCE_LAST_TEST: 0,
  TOTAL_TESTS: 0,
  LATEST_NET: 0,
  REMEMBERING_RATE: 0,
} as const;
