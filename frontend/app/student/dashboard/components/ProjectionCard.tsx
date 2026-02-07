'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import { api } from '@/lib/api/client';
import FeedbackButtons from './FeedbackButtons';
import { useAuthReady } from '@/lib/hooks/useAuthReady';

type ApiSuccess<T> = { success: true; data: T };
type ApiFail = { success: false; error?: any; message?: string };

async function unwrap<T>(p: Promise<any>): Promise<T> {
  const res = (await p) as ApiSuccess<T> | ApiFail | T;
  if (res && typeof res === 'object' && 'success' in res) {
    const r = res as any;
    if (r.success) return r.data as T;
    throw r.error || new Error(r.message || 'API error');
  }
  return res as T;
}

type ProjectionData = {
  overall_progress: number; // 0.1 veya 10 gibi gelebilir (aşağıda normalize ediyoruz)
  estimated_completion_date: string;
  days_remaining: number;
  weekly_improvement: number;
  topics_mastered: number;
  topics_in_progress: number;
  topics_not_started: number;
};

const circularProgressParams = {
  size: 140,
  strokeWidth: 12,
  center: 70,
  radius: 64,
};

export default function ProjectionCard() {
  const { ready } = useAuthReady();

  const [projection, setProjection] = useState<ProjectionData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showDetails, setShowDetails] = useState(false);

  const retryRef = useRef(0);
  const timerRef = useRef<any>(null);
  const inFlightRef = useRef(false);
  const requestIdRef = useRef(0);

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

  const fetchProjection = useCallback(async () => {
    if (!ready) return;
    if (inFlightRef.current) return;
    inFlightRef.current = true;

    clearTimer();
    const myRequestId = ++requestIdRef.current;

    if (retryRef.current === 0) setIsLoading(true);
    setError(null);

    let scheduledRetry = false;

    const run = async function runFetch(): Promise<void> {
      try {
        // ✅ DOĞRU: GET + /student/progress/projection
        const data = await unwrap<ProjectionData>(api.get('/student/progress/projection'));

        if (myRequestId !== requestIdRef.current) return;

        retryRef.current = 0;
        setProjection(data);
      } catch (err: any) {
        if (myRequestId !== requestIdRef.current) return;

        if (err?.code === 'SESSION_NOT_READY') {
          const next = retryRef.current + 1;
          retryRef.current = next;

          if (next <= 10) {
            const delay = Math.min(4000, 250 * Math.pow(2, next - 1));
            scheduledRetry = true;

            timerRef.current = setTimeout(() => {
              inFlightRef.current = false;
              run(); // ✅ self reference yok
            }, delay);

            return;
          }

          setError('Oturum hazırlanamadı. Lütfen sayfayı yenileyin.');
          return;
        }

        setError(err?.message || 'Projeksiyon yüklenemedi');
      } finally {
        if (!scheduledRetry) {
          if (myRequestId === requestIdRef.current) setIsLoading(false);
          inFlightRef.current = false;
        }
      }
    };

    await run();
  }, [ready, clearTimer]);

  useEffect(() => {
    if (!ready) return;
    fetchProjection();
  }, [ready, fetchProjection]);

  if (!ready || isLoading) {
    return (
      <div className="bg-purple-100 rounded-2xl p-8 shadow-lg">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-purple-600 mx-auto mb-4" />
          <p className="text-gray-600">Projeksiyon hesaplanıyor...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border-2 border-red-300 rounded-2xl p-6">
        <div className="text-center">
          <div className="text-4xl mb-2">⚠️</div>
          <div className="text-red-700 font-bold mb-2">Projeksiyon Hatası</div>
          <div className="text-sm text-red-600 mb-4">{error}</div>
          <button
            onClick={() => {
              retryRef.current = 0;
              fetchProjection();
            }}
            className="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700"
          >
            Tekrar Dene
          </button>
        </div>
      </div>
    );
  }

  if (!projection) {
    return (
      <div className="bg-yellow-50 border-2 border-yellow-300 rounded-2xl p-8 text-center">
        <div className="text-6xl mb-4">📊</div>
        <h3 className="text-xl font-bold text-gray-800 mb-2">Henüz Projeksiyon Verisi Yok</h3>
        <p className="text-gray-600 mb-4">Projeksiyon için önce test sonucu girmelisin.</p>
        <a
          href="/student/test-entry"
          className="inline-block bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700"
        >
          Test Ekle
        </a>
      </div>
    );
  }

  // ✅ overall_progress bazen 0.1 (oran) bazen 10 (yüzde) olabilir
  const overallPercent =
    projection.overall_progress <= 1 ? projection.overall_progress * 100 : projection.overall_progress;

  const circumference = 2 * Math.PI * circularProgressParams.radius;
  const progressOffset = circumference - (overallPercent / 100) * circumference;

  const totalTopics =
    projection.topics_mastered + projection.topics_in_progress + projection.topics_not_started;

  const velocityText = (() => {
    if (projection.days_remaining <= 0) return 'Tarih geçti';
    if (projection.weekly_improvement <= 0) return 'Hız hesaplanamadı';
    return `${projection.weekly_improvement.toFixed(2)} puan/hafta`;
  })();

  const gradientColor =
    projection.days_remaining > 120
      ? 'from-red-500 to-red-700'
      : projection.days_remaining > 60
      ? 'from-orange-500 to-orange-700'
      : 'from-purple-500 to-indigo-600';

  return (
    <div className={`bg-gradient-to-r ${gradientColor} text-white rounded-2xl p-6 shadow-xl`}>
      <div className="flex items-center justify-between gap-4">
        <div>
          <div className="text-sm opacity-90">Tahmini Bitiş Tarihi</div>
          <div className="text-2xl font-bold">{projection.estimated_completion_date}</div>
          <div className="text-xs opacity-75 mt-1">
            {projection.topics_mastered}/{totalTopics} konu • Hız: {velocityText}
          </div>
        </div>

        <div className="relative" style={{ width: circularProgressParams.size, height: circularProgressParams.size }}>
          <svg width={circularProgressParams.size} height={circularProgressParams.size} className="-rotate-90">
            <circle
              cx={circularProgressParams.center}
              cy={circularProgressParams.center}
              r={circularProgressParams.radius}
              stroke="rgba(255,255,255,0.2)"
              strokeWidth={circularProgressParams.strokeWidth}
              fill="none"
            />
            <circle
              cx={circularProgressParams.center}
              cy={circularProgressParams.center}
              r={circularProgressParams.radius}
              stroke="white"
              strokeWidth={circularProgressParams.strokeWidth}
              fill="none"
              strokeDasharray={circumference}
              strokeDashoffset={progressOffset}
              strokeLinecap="round"
              className="transition-all duration-1000"
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <div className="text-3xl font-bold">{projection.days_remaining}</div>
            <div className="text-xs">gün kaldı</div>
          </div>
        </div>
      </div>

      <div className="mt-6 bg-white/10 rounded-xl p-4">
        <div className="text-sm font-bold mb-2">Genel İlerleme: %{overallPercent.toFixed(0)}</div>
        <div className="w-full h-3 bg-white/20 rounded-full overflow-hidden">
          <div className="h-full bg-green-400 transition-all" style={{ width: `${overallPercent}%` }} />
        </div>
      </div>

      <button
        onClick={() => setShowDetails(!showDetails)}
        className="mt-4 text-xs underline opacity-80 hover:opacity-100 w-full"
      >
        {showDetails ? '▲ Detayları Gizle' : '▼ Detayları Göster'}
      </button>

      {showDetails && (
        <div className="mt-4 space-y-2 text-xs">
          <div>Mastered: {projection.topics_mastered}</div>
          <div>In progress: {projection.topics_in_progress}</div>
          <div>Not started: {projection.topics_not_started}</div>
        </div>
      )}

      <div className="mt-4 pt-4 border-t border-white/20 flex justify-center">
        <FeedbackButtons
          componentType="projection_card"
          variant="like-dislike"
          size="sm"
          metadata={{
            overall_percent: overallPercent.toFixed(1),
            days_remaining: projection.days_remaining,
          }}
        />
      </div>
    </div>
  );
}
