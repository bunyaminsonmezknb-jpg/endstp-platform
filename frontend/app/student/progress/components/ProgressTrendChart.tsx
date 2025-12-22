'use client';

import { useState } from 'react';
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

// ✅ DOĞRU interface - page.tsx'e uyumlu
interface ProgressTrendChartProps {
  weeklyData: any | null;
  monthlyData: any | null;
  isLoading?: boolean;
}

function ProgressTrendChart({ weeklyData, monthlyData, isLoading = false }: ProgressTrendChartProps) {
  const [currentPeriod, setCurrentPeriod] = useState<'weekly' | 'monthly'>('weekly');

  // ✅ Period'a göre data seç
  const currentData = currentPeriod === 'weekly' ? weeklyData : monthlyData;

  // ✅ Loading state
  if (isLoading || !currentData) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gray-200 rounded-xl animate-pulse"></div>
            <div className="h-6 bg-gray-200 rounded w-40 animate-pulse"></div>
          </div>
          <div className="flex gap-2">
            <div className="h-10 bg-gray-200 rounded w-24 animate-pulse"></div>
            <div className="h-10 bg-gray-200 rounded w-24 animate-pulse"></div>
          </div>
        </div>
        <div className="h-64 bg-gray-100 rounded animate-pulse"></div>
      </div>
    );
  }

  // ✅ Safe data extraction
  const labels = currentData.labels || ['Veri yok'];
  const overallTrend = currentData.overall_trend || [0];
  const datasets = currentData.datasets || [];

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Genel Ortalama',
        data: overallTrend,
        borderColor: 'rgb(147, 51, 234)',
        backgroundColor: 'rgba(147, 51, 234, 0.1)',
        borderWidth: 3,
        fill: true,
        tension: 0.4,
      },
      ...datasets.map((ds: any, idx: number) => {
        const colors = [
          { border: 'rgb(59, 130, 246)', bg: 'rgba(59, 130, 246, 0.1)' },
          { border: 'rgb(16, 185, 129)', bg: 'rgba(16, 185, 129, 0.1)' },
          { border: 'rgb(245, 158, 11)', bg: 'rgba(245, 158, 11, 0.1)' },
        ];
        const color = colors[idx % colors.length];
        
        return {
          label: ds.label,
          data: ds.data,
          borderColor: color.border,
          backgroundColor: color.bg,
          borderWidth: 2,
          fill: true,
          tension: 0.4,
        };
      }),
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom' as const,
        labels: {
          usePointStyle: true,
          padding: 15,
        },
      },
      tooltip: {
        mode: 'index' as const,
        intersect: false,
        callbacks: {
          label: function(context: any) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            if (context.parsed.y !== null) {
              label += context.parsed.y.toFixed(1) + '%';
            }
            return label;
          }
        }
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        ticks: {
          callback: function(value: any) {
            return value + '%';
          }
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
        },
      },
      x: {
        grid: {
          display: false,
        },
      },
    },
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl flex items-center justify-center">
            <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
            </svg>
          </div>
          <h2 className="text-xl font-bold text-gray-900">İlerleme Trendi</h2>
        </div>

        <div className="flex gap-2">
          <button
            onClick={() => setCurrentPeriod('weekly')}
            disabled={!weeklyData}
            className={`px-4 py-2 rounded-lg font-medium transition-all ${
              currentPeriod === 'weekly'
                ? 'bg-purple-600 text-white shadow-md'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed'
            }`}
          >
            Haftalık
          </button>
          <button
            onClick={() => setCurrentPeriod('monthly')}
            disabled={!monthlyData}
            className={`px-4 py-2 rounded-lg font-medium transition-all ${
              currentPeriod === 'monthly'
                ? 'bg-purple-600 text-white shadow-md'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed'
            }`}
          >
            Aylık
          </button>
        </div>
      </div>

      <div style={{ height: '300px' }}>
        <Line data={chartData} options={chartOptions} />
      </div>
    </div>
  );
}

export default ProgressTrendChart;