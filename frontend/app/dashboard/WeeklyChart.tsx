'use client';

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
  Filler
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

interface WeeklyChartProps {
  weeklyData: Array<{ day: string; net: number }>;
}

export default function WeeklyChart({ weeklyData }: WeeklyChartProps) {
  const labels = weeklyData.map(d => d.day);
  const netValues = weeklyData.map(d => d.net);
  
  // Trend hesapla
  const firstNet = netValues[0] || 0;
  const lastNet = netValues[netValues.length - 1] || 0;
  const trend = firstNet > 0 ? ((lastNet - firstNet) / firstNet * 100).toFixed(0) : '0';
  const trendPositive = parseFloat(trend) >= 0;

  const data = {
    labels,
    datasets: [
      {
        label: 'Günlük Net Ortalaması',
        data: netValues,
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.4,
        fill: true,
        pointRadius: 6,
        pointHoverRadius: 8,
        pointBackgroundColor: 'rgb(59, 130, 246)',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
      },
      {
        label: 'Hedef Net',
        data: Array(7).fill(25),
        borderColor: 'rgb(239, 68, 68)',
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
        borderDash: [5, 5],
        tension: 0,
        fill: false,
        pointRadius: 0,
      }
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'top' as const,
      },
      title: {
        display: false,
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        padding: 12,
        titleFont: {
          size: 14,
        },
        bodyFont: {
          size: 13,
        },
        callbacks: {
          label: function(context: any) {
            return context.dataset.label + ': ' + context.parsed.y.toFixed(1) + ' net';
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 30,
        ticks: {
          stepSize: 5,
          callback: function(value: any) {
            return value + ' net';
          }
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)',
        }
      },
      x: {
        grid: {
          display: false,
        }
      }
    },
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
          📈 Haftalık Gelişim
        </h2>
        <div className="text-right">
          <p className="text-sm text-gray-600">Trend</p>
          <p className={`text-xl font-bold ${trendPositive ? 'text-green-600' : 'text-red-600'}`}>
            {trendPositive ? '+' : ''}{trend}% {trendPositive ? '📈' : '📉'}
          </p>
        </div>
      </div>
      
      <div style={{ height: '300px' }}>
        <Line data={data} options={options} />
      </div>

      <div className="mt-4 flex justify-between items-center bg-blue-50 p-4 rounded-lg">
        <div>
          <p className="text-sm text-gray-600">Son Net</p>
          <p className="text-2xl font-bold text-blue-600">{lastNet.toFixed(1)}</p>
        </div>
        <div className="text-right">
          <p className="text-sm text-gray-600">Hedefe Kalan</p>
          <p className="text-2xl font-bold text-orange-600">{(25 - lastNet).toFixed(1)} net</p>
        </div>
      </div>
    </div>
  );
}