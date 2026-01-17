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

export const useTodaysTasks = (): UseTodaysTasksReturn => {
  const [data, setData] = useState<TodaysTasksData | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTodaysTasks = useCallback(
    async (retryCount = 0): Promise<void> => {
      let willRetry = false;

      try {
        setIsLoading(true);
        setError(null);

        // ✅ DOĞRU ENDPOINT
        const raw = await api.get('/student/tasks/today');

        // api client AxiosResponse döndürüyor olabilir → raw.data
        const payload: any = (raw as any)?.data ?? raw;

        if (!payload) {
          throw new Error('Boş API yanıtı');
        }

        /**
         * Backend gerçek response:
         * {
         *   success: true,
         *   tasks,
         *   at_risk_topics,
         *   total_at_risk,
         *   ...
         * }
         */
        if (payload.success !== true) {
          throw new Error('Geçersiz API yanıtı');
        }

        // ✅ ENVELOPE AÇILDI – UI'nin beklediği shape korunuyor
        setData(payload as TodaysTasksData);

      } catch (err: any) {
        console.error('[useTodaysTasks] fetch error:', err);

        // Retry (max 3 deneme: 0,1,2)
        if (retryCount < 2) {
          willRetry = true;
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
        // Retry varsa loading'i kapatıp flicker yaratma
        if (!willRetry) {
          setIsLoading(false);
        }
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
