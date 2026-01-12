'use client';

import { useState, useEffect } from 'react';
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

interface TrendChartProps {
  weeklyData: any;
  monthlyData: any;
  isLoading: boolean;
}

export default function ProgressTrendChart({ 
  weeklyData, 
  monthlyData, 
  isLoading 
}: TrendChartProps) {
  const [period, setPeriod] = useState<'weekly' | 'monthly'>('weekly');
  const [prediction, setPrediction] = useState<any>(null);
  const [showPrediction, setShowPrediction] = useState(false); // ✅ YENİ: Tahmin toggle
  const [showSubjects, setShowSubjects] = useState(false); // ✅ YENİ: Ders toggle

  // Prediction data fetch
  useEffect(() => {
    const fetchPrediction = async () => {
      try {
        const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
        
        const res = await fetch(`${API_BASE}/student/progress/prediction?period=${period}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (res.ok) {
          const result = await res.json();
          setPrediction(result.data);
        }
      } catch (error) {
        console.error('Prediction fetch error:', error);
      }
    };

    fetchPrediction();
  }, [period]);

  const data = period === 'weekly' ? weeklyData : monthlyData;

  if (isLoading || !data) {
    return (
      <div className="animate-pulse space-y-4">
        <div className="h-8 bg-gray-200 rounded w-1/4"></div>
        <div className="h-64 bg-gray-200 rounded"></div>
      </div>
    );
  }

  // Gelecek period label'ları
  const futureLabels = period === 'weekly'
    ? ['Gelecek hafta', '2 hafta sonra', '3 hafta sonra', '4 hafta sonra']
    : ['Gelecek ay', '2 ay sonra', '3 ay sonra', '4 ay sonra'];

  // ===== ✅ YENİ: GENEL ORTALAMA DATASET (HER ZAMAN GÖSTER) =====
  const overallDataset = {
    label: 'Genel Ortalama',
    data: data.overall_trend || [],
    borderColor: 'rgb(99, 102, 241)', // İndigo
    backgroundColor: 'rgba(99, 102, 241, 0.1)',
    borderWidth: 4, // ✅ KALIN ÇİZGİ
    pointRadius: 6,
    pointHoverRadius: 8,
    tension: 0.4,
    fill: true
  };

  // ===== DERS DATASETS (TOGGLE İLE GÖSTER) =====
  const subjectDatasets = (data.datasets || []).map((ds: any, idx: number) => {
    const colors = [
      'rgb(147, 51, 234)',  // Mor
      'rgb(59, 130, 246)',  // Mavi
      'rgb(34, 197, 94)',   // Yeşil
      'rgb(249, 115, 22)'   // Turuncu
    ];
    
    const color = colors[idx % colors.length];

    return {
      label: ds.label,
      data: ds.data,
      borderColor: color,
      backgroundColor: color.replace('rgb', 'rgba').replace(')', ', 0.1)'),
      borderWidth: 2, // ✅ İNCE ÇİZGİ
      pointRadius: 4,
      pointHoverRadius: 6,
      tension: 0.4,
      fill: true,
      subjectId: ds.subject_id // Tahmin için gerekli
    };
  });

  // ===== TAHMİN DATASETS (TOGGLE İLE GÖSTER) =====
  const predictionDatasets: any[] = [];
  
  if (showPrediction && prediction && prediction.predictions) {
    // Genel ortalama tahmini (her zaman)
    const firstSubjectId = Object.keys(prediction.predictions)[0];
    if (firstSubjectId) {
      const firstPred = prediction.predictions[firstSubjectId];
      
      predictionDatasets.push({
        label: 'Genel Ortalama (Senaryo)',
        data: [
          ...Array(data.labels.length - 1).fill(null),
          firstPred.current,
          ...firstPred.future
        ],
        borderColor: 'rgba(99, 102, 241, 0.5)',
        backgroundColor: 'transparent',
        borderWidth: 4,
        borderDash: [5, 5],
        pointRadius: 4,
        tension: 0.4,
        fill: false
      });
    }

    // Ders tahminleri (sadece dersler açıksa)
    if (showSubjects) {
      subjectDatasets.forEach((ds: any) => {
        const pred = prediction.predictions[ds.subjectId];
        if (pred) {
          predictionDatasets.push({
            label: `${ds.label} (Senaryo)`,
            data: [
              ...Array(data.labels.length - 1).fill(null),
              pred.current,
              ...pred.future
            ],
            borderColor: ds.borderColor.replace(')', ', 0.5)'),
            backgroundColor: 'transparent',
            borderWidth: 2,
            borderDash: [5, 5],
            pointRadius: 3,
            tension: 0.4,
            fill: false
          });
        }
      });
    }
  }

  // ===== FİNAL CHART DATA =====
  const chartData = {
    labels: showPrediction ? [...data.labels, ...futureLabels] : data.labels,
    datasets: [
      overallDataset, // Her zaman göster
      ...(showSubjects ? subjectDatasets : []), // Toggle ile göster
      ...predictionDatasets // Toggle ile göster
    ]
  };

  // ===== CHART OPTIONS =====
  const options = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: 'index' as const,
      intersect: false,
    },
    plugins: {
      legend: {
        position: 'bottom' as const,
        labels: {
          usePointStyle: true,
          padding: 15,
          font: { size: 12 }
        },
        // ✅ YENİ: TIKLANABİLİR LEGEND
        onClick: function(e: any, legendItem: any, legend: any) {
          const index = legendItem.datasetIndex;
          const chart = legend.chart;
          const meta = chart.getDatasetMeta(index);
          
          // Toggle visibility
          meta.hidden = meta.hidden === null ? !chart.data.datasets[index].hidden : null;
          chart.update();
        }
      },
      tooltip: {
        callbacks: {
          title: (context: any) => {
            const label = context[0].label;
            if (futureLabels.includes(label)) {
              return `⚠️ ${label} (Senaryo)`;
            }
            return label;
          },
          label: (context: any) => {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            label += context.parsed.y !== null ? `${context.parsed.y}%` : 'Veri yok';
            
            // Tahmin dataseti ise açıklama ekle
            if (context.dataset.borderDash) {
              label += ' (test çözülmezse)';
            }
            return label;
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        ticks: {
          callback: (value: any) => `${value}%`
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)'
        }
      },
      x: {
        grid: {
          display: false
        }
      }
    }
  };

  return (
    <div>
      {/* ===== ✅ YENİ: YUMUŞAK UYARI KUTUSU ===== */}
      {showPrediction && prediction?.steepest_decline && (
        <div className="mb-4 p-4 bg-yellow-50 border border-yellow-200 rounded-xl flex items-center gap-3">
          <span className="text-2xl">💡</span>
          <div>
            <p className="font-semibold text-yellow-900">
              {prediction.steepest_decline.subject_name} için test boşluğu oluşuyor
            </p>
            <p className="text-sm text-yellow-700">
              Bu şekilde devam ederse, 4 haftada ~<strong>%{prediction.steepest_decline.decline_rate}</strong> değişim olası. 
              İstersen projeksiyon detaylarını inceleyebilirsin.
            </p>
          </div>
        </div>
      )}

      {/* ===== HEADER + TOGGLES ===== */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
        </div>
        
        <div className="flex gap-3">
          {/* ✅ YENİ: DERS DETAYLARI TOGGLE */}
          <button
            onClick={() => setShowSubjects(!showSubjects)}
            className={`px-4 py-2 rounded-lg font-medium transition-all flex items-center gap-2 ${
              showSubjects
                ? 'bg-blue-500 text-white shadow-md'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            {showSubjects ? '📚 Dersler Açık' : '📚 Ders Detayları'}
          </button>

          {/* ✅ YENİ: TAHMİN TOGGLE */}
          <button
            onClick={() => setShowPrediction(!showPrediction)}
            className={`px-4 py-2 rounded-lg font-medium transition-all flex items-center gap-2 ${
              showPrediction
                ? 'bg-orange-500 text-white shadow-md'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            {showPrediction ? '🔮 Senaryo Açık' : '🔮 Gelecek Senaryosu'}
          </button>

          {/* HAFTALıK/AYLIK TOGGLE */}
          <div className="flex gap-2 bg-gray-100 p-1 rounded-lg">
            <button
              onClick={() => setPeriod('weekly')}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                period === 'weekly'
                  ? 'bg-purple-600 text-white shadow-md'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Haftalık
            </button>
            <button
              onClick={() => setPeriod('monthly')}
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

      {/* ===== CHART ===== */}
      <div className="h-80">
        <Line data={chartData} options={options} />
      </div>

      {/* ===== AÇIKLAMA (SADECE TAHMİN AÇIKSA) ===== */}
      {showPrediction && (
        <div className="mt-4 p-3 bg-purple-50 rounded-lg">
          <p className="text-sm text-purple-700">
            💡 <strong>Kesikli çizgiler</strong> test çözülmediği takdirde olası evrimi gösterir.
            Proaktif çalışarak performansını koruyabilirsin!
          </p>
        </div>
      )}
    </div>
  );
}