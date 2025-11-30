'use client';

import { useState } from 'react';

interface UniversityGoal {
  priority: number; // 1-5
  universityName: string;
  departmentName: string;
  requiredScore: number;
  currentProgress: number; // 0-100
  status: 'achieved' | 'close' | 'inProgress' | 'distant';
}

interface UniversityGoalCardProps {
  goals?: UniversityGoal[];
  overallProgress?: number;
}

// DEMO DATA - Backend'den gelecek
const DEMO_GOALS: UniversityGoal[] = [
  {
    priority: 1,
    universityName: 'Konya Teknik Ünv.',
    departmentName: 'Bilgisayar Müh.',
    requiredScore: 450,
    currentProgress: 85,
    status: 'achieved'
  },
  {
    priority: 2,
    universityName: 'Antalya Bilim Ünv.',
    departmentName: 'Bilgisayar Müh.',
    requiredScore: 475,
    currentProgress: 65,
    status: 'close'
  },
  {
    priority: 3,
    universityName: 'Ankara Üniversitesi',
    departmentName: 'Bilgisayar Müh.',
    requiredScore: 500,
    currentProgress: 45,
    status: 'inProgress'
  },
  {
    priority: 4,
    universityName: 'İstanbul Medeniyet',
    departmentName: 'Bilgisayar Müh.',
    requiredScore: 525,
    currentProgress: 25,
    status: 'distant'
  },
  {
    priority: 5,
    universityName: 'İstanbul Teknik Ünv.',
    departmentName: 'Bilgisayar Müh.',
    requiredScore: 550,
    currentProgress: 10,
    status: 'distant'
  }
];

export default function UniversityGoalCard({ goals = DEMO_GOALS, overallProgress = 65 }: UniversityGoalCardProps) {
  const [showLadder, setShowLadder] = useState(false);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'achieved': return '🟢';
      case 'close': return '🟡';
      case 'inProgress': return '🟠';
      case 'distant': return '🔴';
      default: return '⚪';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'achieved': return 'Başarıldı';
      case 'close': return 'Çok Yakın';
      case 'inProgress': return 'Çalışıyor';
      case 'distant': return 'Henüz Uzak';
      default: return '';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'achieved': return 'bg-green-500';
      case 'close': return 'bg-yellow-500';
      case 'inProgress': return 'bg-orange-500';
      case 'distant': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  // Ağırlıklı genel ilerleme hesaplama (5. seviye en önemli)
  const calculateOverallProgress = () => {
    const weights = [1, 2, 3, 4, 5]; // Priority 5 en yüksek ağırlık
    let totalWeighted = 0;
    let totalWeight = 0;

    goals.forEach((goal, index) => {
      totalWeighted += goal.currentProgress * weights[index];
      totalWeight += weights[index];
    });

    return Math.round(totalWeighted / totalWeight);
  };

  const overallCalc = calculateOverallProgress();

  return (
    <div className="bg-gradient-to-br from-purple-500 to-indigo-600 text-white rounded-2xl p-6 shadow-xl">
      {/* Kompakt Görünüm */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="text-5xl">🏆</div>
          <div>
            <div className="text-sm opacity-90 font-medium">Nihai Hedef Yolculuğun</div>
            <div className="text-2xl font-bold">
              {goals[1].status === 'achieved' ? `🟢 ${goals[1].priority}. Seviye Başarıldı!` : `Hedefine Doğru İlerliyorsun`}
            </div>
            <div className="text-xs opacity-75 mt-1">
              Genel İlerleme: <span className="font-bold">%{overallCalc}</span>
            </div>
          </div>
        </div>

        {/* İlerleme Halkası */}
        <div className="relative w-20 h-20">
          <svg viewBox="0 0 100 100" className="transform -rotate-90">
            <circle
              cx="50"
              cy="50"
              r="45"
              stroke="rgba(255,255,255,0.2)"
              strokeWidth="8"
              fill="none"
            />
            <circle
              cx="50"
              cy="50"
              r="45"
              stroke="white"
              strokeWidth="8"
              fill="none"
              strokeDasharray="282.6"
              strokeDashoffset={282.6 * (1 - overallCalc / 100)}
              strokeLinecap="round"
              className="transition-all duration-1000"
            />
          </svg>
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-lg font-bold">{overallCalc}%</span>
          </div>
        </div>
      </div>

      {/* Merdiven Detayları (Accordion) */}
      {showLadder && (
        <div className="mt-6 pt-6 border-t border-white/20 space-y-3 animate-fade-in">
          {[...goals].reverse().map((goal) => (
            <div
              key={goal.priority}
              className="bg-white/10 backdrop-blur-sm rounded-xl p-4 hover:bg-white/20 transition-all cursor-pointer"
            >
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <span className="text-2xl">{getStatusIcon(goal.status)}</span>
                  <div>
                    <div className="font-bold text-sm">
                      {goal.priority}. Seviye: {goal.universityName}
                    </div>
                    <div className="text-xs opacity-75">{goal.departmentName}</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-lg font-bold">%{goal.currentProgress}</div>
                  <div className="text-xs opacity-75">{getStatusText(goal.status)}</div>
                </div>
              </div>

              {/* İlerleme Barı */}
              <div className="w-full bg-white/20 rounded-full h-2 overflow-hidden">
                <div
                  className={`h-full ${getStatusColor(goal.status)} transition-all duration-500`}
                  style={{ width: `${goal.currentProgress}%` }}
                />
              </div>

              {/* Net Bilgisi */}
              <div className="mt-2 text-xs opacity-75">
                Gereken Net: <span className="font-semibold">{goal.requiredScore}</span>
              </div>
            </div>
          ))}

          {/* Motivasyon Mesajı */}
          <div className="bg-yellow-500/20 rounded-xl p-3 text-xs">
            <span className="font-bold">💡 Koçluk İpucu:</span> En üst hedefine odaklan, 
            diğerleri doğal olarak gelecek!
          </div>
        </div>
      )}

      {/* Merdiven Butonu */}
      <button
        onClick={() => setShowLadder(!showLadder)}
        className="mt-4 text-xs opacity-75 hover:opacity-100 transition-opacity underline"
      >
        {showLadder ? '▲ Merdiveni Gizle' : '▼ Merdiveni Göster'}
      </button>
    </div>
  );
}
