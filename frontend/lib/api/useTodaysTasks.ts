'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import { TodaysTasksData, TodaysTasksResponse } from '../types/todaysTasks';

// API base URL (from environment variable)
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface UseTodaysTasksReturn {
  data: TodaysTasksData | null;
  isLoading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

/**
 * Custom hook to fetch today's tasks data from backend
 * 
 * Endpoint: GET /api/v1/student/todays-tasks
 * 
 * Features:
 * - Automatic retry on failure (3 attempts)
 * - Loading state
 * - Error handling
 * - Manual refetch capability
 */
export const useTodaysTasks = (): UseTodaysTasksReturn => {
  const [data, setData] = useState<TodaysTasksData | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTodaysTasks = async (retryCount = 0): Promise<void> => {
    try {
      setIsLoading(true);
      setError(null);

      // Make API request
      const response = await axios.get<TodaysTasksResponse>(
        `${API_BASE_URL}/api/v1/student/todays-tasks`,
        {
          headers: {
            'Content-Type': 'application/json',
            // TODO: Add JWT token from auth context
            // 'Authorization': `Bearer ${token}`
          },
          timeout: 10000, // 10 seconds
        }
      );

      if (response.data.success && response.data.data) {
        setData(response.data.data);
        setError(null);
      } else {
        throw new Error(response.data.error || 'Failed to fetch data');
      }
    } catch (err: any) {
      console.error('Error fetching todays tasks:', err);

      // Retry logic (max 3 attempts)
      if (retryCount < 2) {
        console.log(`Retrying... (${retryCount + 1}/2)`);
        await new Promise((resolve) => setTimeout(resolve, 1000)); // Wait 1s
        return fetchTodaysTasks(retryCount + 1);
      }

      // Set error after retries exhausted
      const errorMessage =
        err.response?.data?.message ||
        err.message ||
        'Veri yüklenirken bir hata oluştu';
      setError(errorMessage);
      setData(null);
    } finally {
      setIsLoading(false);
    }
  };

  // Fetch on mount
  useEffect(() => {
    fetchTodaysTasks();
  }, []);

  return {
    data,
    isLoading,
    error,
    refetch: () => fetchTodaysTasks(0),
  };
};

// Mock data for development/testing
export const getMockTodaysTasksData = (): TodaysTasksData => ({
  streak: {
    current_streak: 5,
    longest_streak: 12,
    streak_status: 'active',
    last_study_date: '2025-12-04',
    next_milestone: 7,
  },
  time_stats: {
    total_time_today_minutes: 0,
    target_time_minutes: 96,
    remaining_time_minutes: 96,
    progress_percentage: 0,
    total_time_week_minutes: 380,
  },
  tasks: [
    {
      id: 1,
      motor_type: 'priority',
      title: 'Fonksiyonlar',
      subject: 'Matematik',
      priority_score: 87,
      description: 'Öncelik skoru yüksek (87/100)',
      estimated_questions: 12,
      estimated_time_minutes: 18,
      status: 'pending',
      icon: '📌',
    },
    {
      id: 2,
      motor_type: 'repetition',
      title: 'Çembersel Hareket',
      subject: 'Fizik',
      days_since_last: 14,
      description: 'Son tekrar 14 gün önce',
      estimated_questions: 12,
      estimated_time_minutes: 18,
      status: 'pending',
      icon: '🔁',
    },
  ],
  summary: {
    total_tasks: 2,
    completed_tasks: 0,
    pending_tasks: 2,
    completion_percentage: 0,
  },
  generated_at: new Date().toISOString(),
});