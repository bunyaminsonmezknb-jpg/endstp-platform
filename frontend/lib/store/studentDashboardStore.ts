import { create } from 'zustand';
import { api } from '@/lib/api/client';

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
  latest_success_rate?: number;
  next_review?: {
    days_remaining: number;
    urgency: string;
  };
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
  status: 'excellent' | 'good' | 'warning' | 'frozen' | 'critical';
  statusText: string;
  emoji: string;
  daysSinceLastTest?: number;
  totalTests?: number;
  latestNet?: number;
  latestSuccessRate?: number;
  nextReview?: {
    daysRemaining: number;
    urgency: string;
  };
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
  criticalAlert?: {
    show: boolean;
    topicName: string;
    daysAgo: number;
    forgetRisk: number;
  };
  projection?: {
    status: string;
    total_topics: number;
    completed_topics: number;
    remaining_topics: number;
    estimated_days: number;
    estimated_date: string;
    velocity: string;
    warning_level: string;
    message: string;
  } | null;
}

interface StudentDashboardStore {
  dashboardData: DashboardData | null;
  isLoading: boolean;
  error: string | null;
  fetchDashboardData: (studentId?: string) => Promise<void>;
  setDashboardData: (data: DashboardData) => void;
  updateTopicStatus: (topicId: string, newRememberingRate: number) => void;
}

export const useStudentDashboard = create<StudentDashboardStore>((set) => ({
  dashboardData: null,
  isLoading: false,
  error: null,

  fetchDashboardData: async (studentId?: string) => {
    set({ isLoading: true, error: null });
    
    try {
      // Yeni endpoint: /student/dashboard (token'dan ID alır)
      const response = await api.get<any>('/student/dashboard');
      
      // Transform API response
      const dashboardData: DashboardData = {
        studentName: response.student_name || 'Öğrenci',
        streak: response.streak || 0,
        dailyGoal: response.daily_goal || { current: 0, target: 5 },
        weeklySuccess: response.weekly_success || 0,
        weeklyTarget: response.weekly_target || 85,
        studyTimeToday: response.study_time_today || 0,
        weeklyQuestions: response.weekly_questions || 0,
        weeklyIncrease: response.weekly_increase || 0,
        topics: (response.topics || []).map((topic: ApiTopic) => ({
          id: topic.id,
          name: topic.name,
          subject: topic.subject,
          rememberingRate: topic.rememberingRate,
          status: topic.status.toLowerCase() as any,
          statusText: topic.statusText,
          emoji: topic.emoji,
          daysSinceLastTest: topic.days_since_last_test,
          totalTests: topic.total_tests,
          latestNet: topic.latest_net,
          latestSuccessRate: topic.latest_success_rate,
          nextReview: topic.next_review
  ? {
      daysRemaining: topic.next_review.days_remaining,
      urgency: topic.next_review.urgency
    }
  : undefined,
          achievementBadge: topic.achievementBadge,
        })),
        criticalAlert: response.critical_alert,
        projection: response.projection,
      };

      set({ dashboardData, isLoading: false });
    } catch (err: any) {
      set({ 
        error: err.message || 'Dashboard yüklenemedi', 
        isLoading: false 
      });
    }
  },

  setDashboardData: (data: DashboardData) => set({ dashboardData: data }),

  updateTopicStatus: (topicId: string, newRememberingRate: number) =>
    set((state) => {
      if (!state.dashboardData) return state;

      const updatedTopics = state.dashboardData.topics.map((topic) =>
        topic.id === topicId
          ? { ...topic, rememberingRate: newRememberingRate }
          : topic
      );

      return {
        dashboardData: {
          ...state.dashboardData,
          topics: updatedTopics,
        },
      };
    }),
}));
