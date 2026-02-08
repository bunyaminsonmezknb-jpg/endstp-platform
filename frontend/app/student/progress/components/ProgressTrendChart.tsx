'use client';

import { useMemo, useRef, useState, useEffect, useCallback } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';

import { api } from '@/lib/api/client';
import { useAuthReady } from '@/lib/hooks/useAuthReady';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

interface TrendChartProps {
  weeklyData: any;
  monthlyData: any;
  weeklyPrediction?: any;
  monthlyPrediction?: any;
  isLoading: boolean;
}

const PREDICTION_ENDPOINT = '/student/prediction';

function sleep(ms: number) {
  return new Promise((r) => setTimeout(r, ms));
}

export default function ProgressTrendChart({
  weeklyData,
  monthlyData,
  weeklyPrediction,
  monthlyPrediction,
  isLoading,
}: TrendChartProps) {
  const { ready } = useAuthReady();

  const [period, setPeriod] = useState<'weekly' | 'monthly'>('weekly');
  const [showPrediction, setShowPrediction] = useState(false);
  const [showSubjects, setShowSubjects] = useState(false);

  const [internalWeeklyPred, setInternalWeeklyPred] = useState<any | null>(null);
  const [internalMonthlyPred, setInternalMonthlyPred] = useState<any | null>(null);
  const [predLoading, setPredLoading] = useState(false);
  const [predError, setPredError] = useState<string | null>(null);

  const data = period === 'weekly' ? weeklyData : monthlyData;
  const prediction =
    period === 'weekly'
      ? (weeklyPrediction ?? internalWeeklyPred)
      : (monthlyPrediction ?? internalMonthlyPred);

  const mountedRef = useRef(false);
  const requestIdRef = useRef(0);
  const inFlightRef = useRef(false);
  const retryRef = useRef(0);

  useEffect(() => {
    mountedRef.current = true;
    return () => {
      mountedRef.current = false;
      requestIdRef.current += 1;
      inFlightRef.current = false;
    };
  }, []);

  const fetchPrediction = useCallback(
    async (p: 'weekly' | 'monthly') => {
      if (!ready) return;
      if (!mountedRef.current) return;

      if (p === 'weekly' && weeklyPrediction) return;
      if (p === 'monthly' && monthlyPrediction) return;

      if (inFlightRef.current) return;
      inFlightRef.current = true;

      const myRequestId = ++requestIdRef.current;

      setPredError(null);
      setPredLoading(true);

      try {
        retryRef.current = 0;

        while (true) {
          try {
            const res = (await api.post(PREDICTION_ENDPOINT, { period: p })) as any;

            if (!mountedRef.current || myRequestId !== requestIdRef.current) return;

            if (p === 'weekly') setInternalWeeklyPred(res);
            else setInternalMonthlyPred(res);

            break;
          } catch (err: any) {
            if (!mountedRef.current || myRequestId !== requestIdRef.current) return;

            if (err?.code === 'SESSION_NOT_READY') {
              const next = retryRef.current + 1;
              retryRef.current = next;

              if (next <= 6) {
                const delay = Math.min(2000, 250 * Math.pow(2, next - 1));
                await sleep(delay);
                continue;
              }

              setPredError('Oturum hazırlanamadı. Tahmin verisi alınamadı.');
              break;
            }

            setPredError(err?.message || 'Tahmin verisi alınamadı.');
            break;
          }
        }
      } finally {
        if (mountedRef.current && myRequestId === requestIdRef.current) {
          setPredLoading(false);
        }
        inFlightRef.current = false;
      }
    },
    [ready, weeklyPrediction, monthlyPrediction]
  );

  const futureLabels = useMemo(() => {
    return period === 'weekly'
      ? ['Gelecek hafta', '2 hafta sonra', '3 hafta sonra', '4 hafta sonra']
      : ['Gelecek ay', '2 ay sonra', '3 ay sonra', '4 ay sonra'];
  }, [period]);

  // ⭐ RENK PALETİ
  const subjectColors = [
    'rgb(147, 51, 234)',  // Mor
    'rgb(59, 130, 246)',  // Mavi
    'rgb(34, 197, 94)',   // Yeşil
    'rgb(249, 115, 22)'   // Turuncu
  ];

  const chartData = useMemo(() => {
    if (!data || !Array.isArray(data.labels) || data.labels.length === 0) {
      return {
        labels: [],
        datasets: [],
      };
    }

    // ⭐ GENEL ORTALAMA (İNDİGO)
    const overallDataset = {
      label: 'Genel Ortalama',
      data: data.overall_trend || [],
      borderColor: 'rgb(99, 102, 241)', // İndigo
      backgroundColor: 'rgba(99, 102, 241, 0.1)',
      borderWidth: 4,
      pointRadius: 6,
      pointHoverRadius: 8,
      tension: 0.4,
      fill: true,
    };

    // ⭐ DERSLER (RENKLERLE)
    const subjectDatasets = (data.datasets || []).map((ds: any, idx: number) => {
      const color = subjectColors[idx % subjectColors.length];
      
      return {
        label: ds.label,
        data: ds.data,
        borderColor: color,
        backgroundColor: color.replace('rgb', 'rgba').replace(')', ', 0.1)'),
        borderWidth: 2,
        pointRadius: 4,
        pointHoverRadius: 6,
        tension: 0.4,
        fill: true,
        subjectId: ds.subject_id,
      };
    });

    // ⭐ TAHMİN DATASETS
    const predictionDatasets: any[] = [];
    const preds = prediction?.predictions;

    if (showPrediction && preds) {
      const firstSubjectId = Object.keys(preds)[0];
      if (firstSubjectId) {
        const firstPred = preds[firstSubjectId];
        predictionDatasets.push({
          label: 'Genel Ortalama (Senaryo)',
          data: [
            ...Array(data.labels.length - 1).fill(null),
            firstPred.current,
            ...firstPred.future,
          ],
          borderColor: 'rgba(99, 102, 241, 0.5)',
          backgroundColor: 'transparent',
          borderWidth: 4,
          borderDash: [5, 5],
          pointRadius: 4,
          tension: 0.4,
          fill: false,
        });
      }

      if (showSubjects) {
        subjectDatasets.forEach((ds: any, idx: number) => {
          const pred = preds[ds.subjectId];
          if (pred) {
            const color = subjectColors[idx % subjectColors.length];
            predictionDatasets.push({
              label: `${ds.label} (Senaryo)`,
              data: [
                ...Array(data.labels.length - 1).fill(null),
                pred.current,
                ...pred.future,
              ],
              borderColor: color.replace(')', ', 0.5)'),
              backgroundColor: 'transparent',
              borderWidth: 2,
              borderDash: [5, 5],
              pointRadius: 3,
              tension: 0.4,
              fill: false,
            });
          }
        });
      }
    }

    return {
      labels: showPrediction ? [...data.labels, ...futureLabels] : data.labels,
      datasets: [
        overallDataset,
        ...(showSubjects ? subjectDatasets : []),
        ...predictionDatasets,
      ],
    };
  }, [data, showPrediction, showSubjects, prediction, futureLabels, subjectColors]);

  const options: any = useMemo(() => {
    return {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: {
          position: 'bottom',
          labels: { usePointStyle: true, padding: 15, font: { size: 12 } },
        },
        tooltip: {
          callbacks: {
            title: (context: any) => {
              const label = context?.[0]?.label;
              return futureLabels.includes(label) ? `⚠️ ${label} (Senaryo)` : label;
            },
            label: (context: any) => {
              let label = context.dataset.label || '';
              if (label) label += ': ';
              label += context.parsed.y != null ? `${context.parsed.y}%` : 'Veri yok';
              if (context.dataset.borderDash) label += ' (test çözülmezse)';
              return label;
            },
          },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          ticks: { callback: (v: any) => `${v}%` },
        },
        x: { grid: { display: false } },
      },
    };
  }, [futureLabels]);

  if (isLoading) {
    return (
      <div className="animate-pulse space-y-4">
        <div className="h-8 bg-gray-200 rounded w-1/4"></div>
        <div className="h-64 bg-gray-200 rounded"></div>
      </div>
    );
  }

  if (!data || !Array.isArray(data.labels) || data.labels.length === 0) {
    return (
      <div className="bg-gray-50 border border-gray-200 rounded-2xl p-6 text-gray-600">
        Henüz trend verisi yok.
      </div>
    );
  }

  return (
    <div>
      {showPrediction && (predLoading || predError) && (
        <div className="mb-4 p-4 bg-gray-50 border border-gray-200 rounded-xl flex items-center gap-3">
          <span className="text-2xl">{predLoading ? '⏳' : '⚠️'}</span>
          <div>
            <p className="font-semibold text-gray-900">
              {predLoading ? 'Senaryo verisi hazırlanıyor…' : 'Senaryo verisi alınamadı'}
            </p>
            <p className="text-sm text-gray-600">
              {predLoading ? 'Oturum hazır olunca otomatik yüklenecek.' : predError}
            </p>
          </div>
        </div>
      )}

      {showPrediction && prediction?.steepest_decline && (
        <div className="mb-4 p-4 bg-yellow-50 border border-yellow-200 rounded-xl flex items-center gap-3">
          <span className="text-2xl">💡</span>
          <div>
            <p className="font-semibold text-yellow-900">
              {prediction.steepest_decline.subject_name} için test boşluğu oluşuyor
            </p>
            <p className="text-sm text-yellow-700">
              Bu şekilde devam ederse, 4 haftada ~%{prediction.steepest_decline.decline_rate}{' '}
              değişim olası.
            </p>
          </div>
        </div>
      )}

      <div className="flex items-center justify-between mb-6">
        <div className="flex gap-3">
          <button
            onClick={() => setShowSubjects(!showSubjects)}
            className={`px-4 py-2 rounded-lg font-medium transition-all ${
              showSubjects
                ? 'bg-blue-500 text-white shadow-md'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            {showSubjects ? '📚 Dersler Açık' : '📚 Ders Detayları'}
          </button>

          <button
            onClick={() => {
              const next = !showPrediction;
              setShowPrediction(next);
              if (next) fetchPrediction(period);
            }}
            className={`px-4 py-2 rounded-lg font-medium transition-all ${
              showPrediction
                ? 'bg-orange-500 text-white shadow-md'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            {showPrediction ? '🔮 Senaryo Açık' : '🔮 Gelecek Senaryosu'}
          </button>

          <div className="flex gap-2 bg-gray-100 p-1 rounded-lg">
            <button
              onClick={() => {
                setPeriod('weekly');
                if (showPrediction) fetchPrediction('weekly');
              }}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                period === 'weekly'
                  ? 'bg-purple-600 text-white shadow-md'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Haftalık
            </button>
            <button
              onClick={() => {
                setPeriod('monthly');
                if (showPrediction) fetchPrediction('monthly');
              }}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                period === 'monthly'
                  ? 'bg-purple-600 text-white shadow-md'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Aylık
            </button>
          </div>
        </div>
      </div>

      <div className="h-80">
        <Line data={chartData} options={options} />
      </div>

      {showPrediction && (
        <div className="mt-4 p-3 bg-purple-50 rounded-lg">
          <p className="text-sm text-purple-700">
            💡 <strong>Kesikli çizgiler</strong> test çözülmediği takdirde olası evrimi gösterir.
          </p>
        </div>
      )}
    </div>
  );
}
