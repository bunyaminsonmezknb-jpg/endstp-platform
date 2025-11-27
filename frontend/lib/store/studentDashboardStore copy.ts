import { create } from 'zustand';
import { API_BASE_URL, API_ENDPOINTS, STORAGE_KEYS, DEFAULTS } from '../constants';
import { parseTopicStatus, safeNumber } from '../utils/type-guards';
import type { ValidTopicStatus } from '../constants';

interface ApiTopic {
  id: string;
  name: string;
  subject: string;
  rememberingRate: number;
  status: string;
  statusText: string;
  emoji: string;
  days_since_last_test?: number;
  total_tests?: number;
  latest_net?: number;
  achievementBadge?: {
    text: string;
    icon: string;
  };
}

export interface Topic {
  id: string;
  name: string;
  subject: string;
  rememberingRate: number;
  status: ValidTopicStatus;  // ✅ Type-safe
  statusText: string;
  emoji: string;
  daysSinceLastTest: number;
  totalTests: number;
  latestNet: number;
  achievementBadge?: {
    text: string;
    icon: string;
  };
}

export interface DashboardData {
  studentName: string;
  streak: number;
  dailyGoal: {
    current: number;
    target: number;
  };
  weeklySuccess: number;
  weeklyTarget: number;
  studyTimeToday: number;
  weeklyQuestions: number;
  weeklyIncrease: number;
  topics: Topic[];
  criticalAlert: {
    show: boolean;
    topicName: string;
    daysAgo: number;
    forgetRisk: number;
  } | null;
}

interface ApiResponse {
  student_name: string;
  streak: number;
  daily_goal: {
    current: number;
    target: number;
  };
  weekly_success: number;
  weekly_target: number;
  study_time_today: number;
  weekly_questions: number;
  weekly_increase: number;
  topics: ApiTopic[];
  critical_alert: {
    show: boolean;
    topicName: string;
    daysAgo: number;
    forgetRisk: number;
  } | null;
}

// ✅ RUNTIME VALIDATION + TYPE TRANSFORMATION
function transformApiResponse(apiData: ApiResponse): DashboardData {
  return {
    studentName: apiData.student_name,
    streak: safeNumber(apiData.streak, 0),
    dailyGoal: apiData.daily_goal,
    weeklySuccess: safeNumber(apiData.weekly_success, 0),
    weeklyTarget: safeNumber(apiData.weekly_target, 85),
    studyTimeToday: safeNumber(apiData.study_time_today, 0),
    weeklyQuestions: safeNumber(apiData.weekly_questions, 0),
    weeklyIncrease: safeNumber(apiData.weekly_increase, 0),
    topics: apiData.topics.map((topic): Topic => ({
      id: topic.id,
      name: topic.name,
      subject: topic.subject,
      rememberingRate: safeNumber(topic.rememberingRate, DEFAULTS.REMEMBERING_RATE),
      status: parseTopicStatus(topic.status),  // ✅ VALIDATED
      statusText: topic.statusText,
      emoji: topic.emoji,
      daysSinceLastTest: safeNumber(topic.days_since_last_test, DEFAULTS.DAYS_SINCE_LAST_TEST),
      totalTests: safeNumber(topic.total_tests, DEFAULTS.TOTAL_TESTS),
      latestNet: safeNumber(topic.latest_net, DEFAULTS.LATEST_NET),
      achievementBadge: topic.achievementBadge,
    })),
    criticalAlert: apiData.critical_alert,
  };
}

interface StudentDashboardStore {
  dashboardData: DashboardData | null;
  isLoading: boolean;
  error: string | null;
  fetchDashboardData: (studentId: string) => Promise<void>;
}

export const useStudentDashboard = create<StudentDashboardStore>((set) => ({
  dashboardData: null,
  isLoading: false,
  error: null,

  fetchDashboardData: async (studentId: string) => {
    set({ isLoading: true, error: null });

    try {
      // ✅ CONSTANTS KULLANIMI
      const accessToken = localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN);
      
      if (!accessToken) {
        throw new Error('Oturum bulunamadı');
      }

      // ✅ ENVIRONMENT VARIABLE KULLANIMI
      const url = `${API_BASE_URL}${API_ENDPOINTS.STUDENT_DASHBOARD(studentId)}`;
      
      const response = await fetch(url, {
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`API Hatası: ${response.status}`);
      }

      const apiData: ApiResponse = await response.json();
      
      // ✅ VALIDATED TRANSFORMATION
      const transformedData = transformApiResponse(apiData);

      set({ dashboardData: transformedData, isLoading: false });
    } catch (err: any) {
      console.error('Dashboard fetch error:', err);
      set({ 
        error: err.message || 'Veri yüklenirken hata oluştu', 
        isLoading: false 
      });
    }
  },
}));