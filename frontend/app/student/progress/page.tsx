'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import { useAuthReady } from '@/lib/hooks/useAuthReady';
import { api } from '@/lib/api/client';

import ProjectionCard from '../dashboard/components/ProjectionCard';
import UniversityGoalCard from '../dashboard/components/UniversityGoalCard';
import ProgressTrendChart from './components/ProgressTrendChart';
import SubjectProgressList from './components/SubjectProgressList'; // ⭐ EKLENDI

type NormalizedError = {
  code?: string;
  message: string;
  silent?: boolean;
  retryable?: boolean;
  raw?: unknown;
};

function normalizeError(err: any): NormalizedError {
  const code = err?.code || err?.error?.code || err?.data?.code;
  const message =
    err?.message ||
    err?.error?.message ||
    err?.data?.message ||
    'Beklenmeyen bir hata oluştu.';
  const silent = Boolean(err?.silent ?? err?.error?.silent);
  const retryable = Boolean(err?.retryable ?? err?.error?.retryable);
  return { code, message, silent, retryable, raw: err };
}

function isSessionNotReady(e: NormalizedError) {
  return e.code === 'SESSION_NOT_READY';
}

function qs(params: Record<string, string | number>) {
  return new URLSearchParams(
    Object.entries(params).map(([k, v]) => [k, String(v)])
  ).toString();
}

export default function ProgressPage() {
  const { ready } = useAuthReady();

  const [trend, setTrend] = useState<any | null>(null);
  const [loadingTrend, setLoadingTrend] = useState(true);
  const [trendError, setTrendError] = useState<NormalizedError | null>(null);

  // ⭐ SUBJECTS STATE
  const [subjects, setSubjects] = useState<any[] | null>(null);
  const [loadingSubjects, setLoadingSubjects] = useState(true);
  const [subjectsError, setSubjectsError] = useState<NormalizedError | null>(null);

  const inFlightRef = useRef(false);
  const requestIdRef = useRef(0);
  const retryRef = useRef(0);
  const timerRef = useRef<any>(null);

  const clearTimer = useCallback(() => {
    if (timerRef.current) {
      clearTimeout(timerRef.current);
      timerRef.current = null;
    }
  }, []);

  useEffect(() => {
    return () => {
      clearTimer();
      requestIdRef.current += 1;
      inFlightRef.current = false;
    };
  }, [clearTimer]);

  const fetchTrend = useCallback(async () => {
    if (!ready) return;
    if (inFlightRef.current) return;
    inFlightRef.current = true;

    clearTimer();
    const myRequestId = ++requestIdRef.current;

    setLoadingTrend(true);
    setTrendError(null);

    let scheduledRetry = false;

    try {
      const weeklyTrends = await api.get<any>(
        `/student/progress/trends?${qs({ period: 'weekly', num_periods: 24 })}`
      );
      const monthlyTrends = await api.get<any>(
        `/student/progress/trends?${qs({ period: 'monthly', num_periods: 12 })}`
      );
      const weeklyPrediction = await api.get<any>(
        `/student/progress/prediction?${qs({ period: 'weekly' })}`
      );
      const monthlyPrediction = await api.get<any>(
        `/student/progress/prediction?${qs({ period: 'monthly' })}`
      );

      if (myRequestId !== requestIdRef.current) return;

      retryRef.current = 0;

      setTrend({
        weeklyData: weeklyTrends?.data ?? weeklyTrends,
        monthlyData: monthlyTrends?.data ?? monthlyTrends,
        weeklyPrediction: weeklyPrediction?.data ?? weeklyPrediction,
        monthlyPrediction: monthlyPrediction?.data ?? monthlyPrediction,
      });
    } catch (err: any) {
      const e = normalizeError(err);
      if (myRequestId !== requestIdRef.current) return;

      if (isSessionNotReady(e)) {
        const next = retryRef.current + 1;
        retryRef.current = next;

        if (next <= 6) {
          const delay = Math.min(2000, 250 * Math.pow(2, next - 1));
          scheduledRetry = true;

          timerRef.current = setTimeout(() => {
            inFlightRef.current = false;
            fetchTrend();
          }, delay);

          return;
        }

        setTrendError({
          code: 'SESSION_NOT_READY',
          message: 'Oturum hazırlanamadı. Lütfen sayfayı yenileyin.',
          silent: true,
          raw: err,
        });
        return;
      }

      setTrendError(e);
    } finally {
      if (!scheduledRetry) {
        if (myRequestId === requestIdRef.current) setLoadingTrend(false);
        inFlightRef.current = false;
      }
    }
  }, [ready, clearTimer]);

  // ⭐ SUBJECTS FETCH
  const fetchSubjects = useCallback(async () => {
    if (!ready) return;

    setLoadingSubjects(true);
    setSubjectsError(null);

    try {
      const response = await api.get<any>('/student/progress/subjects');
      setSubjects(response?.data ?? response);
    } catch (err: any) {
      const e = normalizeError(err);
      setSubjectsError(e);
    } finally {
      setLoadingSubjects(false);
    }
  }, [ready]);

  useEffect(() => {
    if (!ready) return;
    fetchTrend();
    fetchSubjects(); // ⭐ SUBJECTS FETCH
  }, [ready, fetchTrend, fetchSubjects]);

  if (!ready) {
    return (
      <div className="p-6">
        <div className="rounded-2xl border p-6 shadow-sm">
          <div className="text-lg font-semibold">Oturum hazırlanıyor…</div>
          <div className="mt-2 text-sm text-muted-foreground">Lütfen bekleyin.</div>
        </div>
      </div>
    );
  }

  const showTrendError = Boolean(trendError && !loadingTrend);

  return (
    <div className="p-6 space-y-6">
      {/* Top Cards */}
      <div className="grid gap-6 lg:grid-cols-2">
        <ProjectionCard />
        <UniversityGoalCard />
      </div>

      {/* Trend Chart */}
      {showTrendError ? (
        <div className="bg-red-50 border border-red-200 rounded-2xl p-6">
          <div className="font-semibold text-red-800">Trend Hatası</div>
          <div className="text-sm text-red-700 mt-1">
            {trendError?.message || 'Trend verisi yüklenemedi.'}
          </div>
          <button
            onClick={fetchTrend}
            className="mt-4 bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700"
          >
            Tekrar Dene
          </button>
        </div>
      ) : (
        <ProgressTrendChart
          weeklyData={trend?.weeklyData}
          monthlyData={trend?.monthlyData}
          weeklyPrediction={trend?.weeklyPrediction}
          monthlyPrediction={trend?.monthlyPrediction}
          isLoading={loadingTrend}
        />
      )}

      {/* ⭐ SUBJECT PROGRESS LIST - YENİDEN EKLENDİ */}
      <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
        <SubjectProgressList 
          subjects={subjects} 
          isLoading={loadingSubjects} 
        />
      </div>

      {/* Subjects Error */}
      {subjectsError && !loadingSubjects && (
        <div className="bg-red-50 border border-red-200 rounded-2xl p-6">
          <div className="font-semibold text-red-800">Ders Verisi Hatası</div>
          <div className="text-sm text-red-700 mt-1">
            {subjectsError.message}
          </div>
          <button
            onClick={fetchSubjects}
            className="mt-4 bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700"
          >
            Tekrar Dene
          </button>
        </div>
      )}
    </div>
  );
}
