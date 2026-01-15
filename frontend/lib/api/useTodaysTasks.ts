'use client';

import { useState, useEffect, useCallback } from 'react';
import { api } from './client';
import { TodaysTasksData } from '../types/todaysTasks';

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
 * Altın Standartlar:
 * - Auth → api-client interceptor
 * - No localStorage / token usage
 * - Retry mekanizması
 * - Type-safe response
 * - Sadece canlı veri
 */
export const useTodaysTasks = (): UseTodaysTasksReturn => {
  const [data, setData] = useState<TodaysTasksData | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTodaysTasks = useCallback(
    async (retryCount = 0): Promise<void> => {
      try {
        setIsLoading(true);
        setError(null);

        const response = await api.get('/student/todays-tasks');

        /**
         * Beklenen backend response:
         * {
         *   success: true,
         *   data: TodaysTasksData
         * }
         */
        if (!response) {
          throw new Error('Boş API yanıtı');
        }

        setData(response as TodaysTasksData);

      } catch (err: any) {
        console.error('[useTodaysTasks] fetch error:', err);

        // Retry (max 3 deneme)
        if (retryCount < 2) {
          await new Promise((resolve) => setTimeout(resolve, 1000));
          return fetchTodaysTasks(retryCount + 1);
        }

        const message =
          err?.response?.data?.message ||
          err?.message ||
          'Bugünkü görevler yüklenemedi';

        setError(message);
        setData(null);
      } finally {
        setIsLoading(false);
      }
    },
    []
  );

  // İlk yükleme
  useEffect(() => {
    fetchTodaysTasks();
  }, [fetchTodaysTasks]);

  return {
    data,
    isLoading,
    error,
    refetch: () => fetchTodaysTasks(0),
  };
};
