'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api/client';
import FeedbackButtons from './FeedbackButtons';

// =====================
// Types
// =====================
interface ProjectionData {
  totalTopics: number;
  completedTopics: number;
  estimatedDays: number;
  estimatedDate: string;
}

// =====================
// FIX: Halka grafiği parametreleri
// =====================
const circularProgressParams = {
  size: 140,
  strokeWidth: 12,
  center: 70,
  radius: 64,
};

export default function ProjectionCard() {
  const [projection, setProjection] = useState<ProjectionData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showDetails, setShowDetails] = useState(false);

  useEffect(() => {
    fetchProjection();
  }, []);

  const fetchProjection = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = (await api.post('/student/projection')) as any;

      if (response?.status === 'no_data') {
        setProjection(null);
      } else if (response?.projection) {
        setProjection({
          totalTopics: Number(
            response.projection.total_topics ??
              response.projection.totalTopics ??
              0
          ),
          completedTopics: Number(
            response.projection.completed_topics ??
              response.projection.completedTopics ??
              0
          ),
          estimatedDays: Number(
            response.projection.estimated_days ??
              response.projection.estimatedDays ??
              0
          ),
          estimatedDate:
            response.projection.estimated_date ??
            response.projection.estimatedDate ??
            '',
        });
      }
    } catch (err: any) {
      setError(err?.message || 'Projeksiyon yüklenemedi');
    } finally {
      setIsLoading(false);
    }
  };

  // =====================
  // Loading / Error
  // =====================
  if (isLoading) {
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
          <div className="text-red-700 font-bold mb-2">
            Projeksiyon Hatası
          </div>
          <div className="text-sm text-red-600 mb-4">{error}</div>
          <button
            onClick={fetchProjection}
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
        <h3 className="text-xl font-bold text-gray-800 mb-2">
          Henüz Projeksiyon Verisi Yok
        </h3>
        <p className="text-gray-600 mb-4">
          Projeksiyon hesaplayabilmek için önce test sonuçları girmelisiniz.
        </p>
        <a
          href="/test-entry"
          className="inline-block bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700"
        >
          Test Ekle
        </a>
      </div>
    );
  }

  // =====================
  // Calculations
  // =====================
  const remainingTopics =
    projection.totalTopics - projection.completedTopics;

  const progressPercent =
    projection.totalTopics > 0
      ? Math.min(
          100,
          (projection.completedTopics / projection.totalTopics) * 100
        )
      : 0;

  const circumference =
    2 * Math.PI * circularProgressParams.radius;

  const progressOffset =
    circumference -
    Math.min(1, projection.estimatedDays / 365) * circumference;

  const velocityText = (() => {
    if (remainingTopics <= 0) return 'Tamamlandı 🎉';
    if (projection.estimatedDays <= 0) return 'Veri yetersiz';

    const daily = remainingTopics / projection.estimatedDays;
    return daily < 1
      ? `${(daily * 7).toFixed(1)} konu/hafta`
      : `${daily.toFixed(1)} konu/gün`;
  })();

  const gradientColor =
    projection.estimatedDays > 60
      ? 'from-red-500 to-red-700'
      : projection.estimatedDays > 30
      ? 'from-orange-500 to-orange-700'
      : 'from-purple-500 to-indigo-600';

  // =====================
  // Render
  // =====================
  return (
    <div
      className={`bg-gradient-to-r ${gradientColor} text-white rounded-2xl p-6 shadow-xl`}
    >
      {/* HEADER */}
      <div className="flex items-center justify-between gap-4">
        <div>
          <div className="text-sm opacity-90">
            Tahmini Bitiş Tarihi
          </div>
          <div className="text-2xl font-bold">
            {projection.estimatedDate}
          </div>
          <div className="text-xs opacity-75 mt-1">
            {projection.completedTopics}/{projection.totalTopics} konu •
            Hız: {velocityText}
          </div>
        </div>

        {/* CIRCULAR GRAPH */}
        <div
          className="relative"
          style={{
            width: circularProgressParams.size,
            height: circularProgressParams.size,
          }}
        >
          <svg
            width={circularProgressParams.size}
            height={circularProgressParams.size}
            className="-rotate-90"
          >
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
            <div className="text-3xl font-bold">
              {projection.estimatedDays}
            </div>
            <div className="text-xs">gün</div>
          </div>
        </div>
      </div>

      {/* PROGRESS BAR */}
      <div className="mt-6 bg-white/10 rounded-xl p-4">
        <div className="text-sm font-bold mb-2">
          Genel İlerleme: %{progressPercent.toFixed(0)}
        </div>
        <div className="w-full h-3 bg-white/20 rounded-full overflow-hidden">
          <div
            className="h-full bg-green-400 transition-all"
            style={{ width: `${progressPercent}%` }}
          />
        </div>
      </div>

      {/* DETAILS */}
      <button
        onClick={() => setShowDetails(!showDetails)}
        className="mt-4 text-xs underline opacity-80 hover:opacity-100 w-full"
      >
        {showDetails ? '▲ Detayları Gizle' : '▼ Detayları Göster'}
      </button>

      {showDetails && (
        <div className="mt-4 space-y-2 text-xs">
          <div>Kalan konu: {remainingTopics}</div>
          <div>Günlük hız: {velocityText}</div>
        </div>
      )}

      {/* FEEDBACK */}
      <div className="mt-4 pt-4 border-t border-white/20 flex justify-center">
        <FeedbackButtons
          componentType="projection_card"
          variant="like-dislike"
          size="sm"
          metadata={{
            estimated_days: projection.estimatedDays,
            progress_percent: progressPercent.toFixed(1),
          }}
        />
      </div>
    </div>
  );
}
