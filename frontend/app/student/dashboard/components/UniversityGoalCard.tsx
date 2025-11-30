'use client';

import { useState, useMemo } from 'react';

// Arayüz Tanımlamaları (Mevcut kodlardan birleştirildi)
interface SubjectGoal {
  name: string;
  current: number;
  target: number;
}

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
}

// DEMO DATA (Birleştirilmiş ve Geliştirilmiş)
const DEMO_GOALS: UniversityGoal[] = [
  // ... (Mevcut DEMO_GOALS verisi buraya eklenecek)
  { priority: 1, universityName: 'Konya Teknik Ünv.', departmentName: 'Bilgisayar Müh.', requiredScore: 450, currentProgress: 85, status: 'achieved' },
  { priority: 2, universityName: 'Antalya Bilim Ünv.', departmentName: 'Bilgisayar Müh.', requiredScore: 475, currentProgress: 65, status: 'close' },
  { priority: 3, universityName: 'Ankara Üniversitesi', departmentName: 'Bilgisayar Müh.', requiredScore: 500, currentProgress: 45, status: 'inProgress' },
  { priority: 4, universityName: 'İstanbul Medeniyet', departmentName: 'Bilgisayar Müh.', requiredScore: 525, currentProgress: 25, status: 'distant' },
  { priority: 5, universityName: 'İstanbul Teknik Ünv.', departmentName: 'Bilgisayar Müh.', requiredScore: 550, currentProgress: 10, status: 'distant' }
];

// AKTİF HEDEF DATA (Mock data, merdivenden ayrı tutulur)
const ACTIVE_GOAL_DATA = {
  university: "Selçuk Üniversitesi", // Önceki görsellerdeki hedef
  department: "Bilgisayar Mühendisliği",
  level: 3, // (3. Tercih)
  targetNet: 400,
  currentNet: 280,
  progressPercent: 70,
  remainingNet: 120,
  daysToReach: 60,
  dailyIncreaseNeeded: 2.0,
  subjects: [
    { name: "Matematik", current: 8, target: 12 },
    { name: "Fizik", current: 6, target: 10 },
    { name: "Kimya", current: 7, target: 9 },
    { name: "Biyoloji", current: 5, target: 8 },
  ] as SubjectGoal[],
};

export default function UniversityGoalCard({ goals = DEMO_GOALS }: UniversityGoalCardProps) {
  // 1. Durum Yönetimi
  const [showLadder, setShowLadder] = useState(false);
  const [showActiveDetails, setShowActiveDetails] = useState(false); // Yeni detay açma/kapama durumu

  // Helper fonksiyonları (Mevcut kodlardan kopyalandı)
  const getStatusIcon = (status: string) => {
    // ... (Mevcut getStatusIcon fonksiyonu)
    switch (status) {
      case 'achieved': return '🟢';
      case 'close': return '🟡';
      case 'inProgress': return '🟠';
      case 'distant': return '🔴';
      default: return '⚪';
    }
  };

  const getStatusText = (status: string) => {
    // ... (Mevcut getStatusText fonksiyonu)
    switch (status) {
      case 'achieved': return 'Başarıldı';
      case 'close': return 'Çok Yakın';
      case 'inProgress': return 'Çalışıyor';
      case 'distant': return 'Henüz Uzak';
      default: return '';
    }
  };
  
  const getStatusColor = (status: string) => {
    // ... (Mevcut getStatusColor fonksiyonu)
    switch (status) {
      case 'achieved': return 'bg-green-500';
      case 'close': return 'bg-yellow-500';
      case 'inProgress': return 'bg-orange-500';
      case 'distant': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  const calculateOverallProgress = () => {
    // ... (Mevcut calculateOverallProgress fonksiyonu)
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
  
  // Aktif Hedef için Renkler
  const getProgressColor = (percent: number) => {
    if (percent >= 80) return 'from-green-400 to-green-600';
    if (percent >= 60) return 'from-yellow-400 to-yellow-600';
    return 'from-orange-400 to-orange-600';
  };

  const getStatusEmoji = (percent: number) => {
    if (percent >= 80) return '🔥';
    if (percent >= 60) return '💪';
    return '📈';
  };

  // Aktif Hedef Verisi
  const goal = ACTIVE_GOAL_DATA;


  return (
    <div className="bg-gradient-to-br from-purple-500 to-indigo-600 text-white rounded-2xl p-6 shadow-xl min-w-80">
      {/* -------------------- ANA BAŞLIK BÖLÜMÜ (Sabit) -------------------- */}
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-4">
          <div className="text-5xl">🏆</div>
          <div>
            <div className="text-sm opacity-90 font-medium">Nihai Hedef Yolculuğun</div>
            <div className="text-2xl font-bold leading-tight">
              Hedefine Doğru İlerliyorsun
            </div>
            <div className="text-xs opacity-75 mt-1">
              Genel İlerleme: <span className="font-bold">%{overallCalc}</span>
            </div>
          </div>
        </div>

        {/* İlerleme Halkası */}
        <div className="relative w-16 h-16 sm:w-20 sm:h-20 flex-shrink-0">
          <svg viewBox="0 0 100 100" className="transform -rotate-90">
            {/* Arkaplan Çizgisi */}
            <circle cx="50" cy="50" r="45" stroke="rgba(255,255,255,0.2)" strokeWidth="8" fill="none" />
            {/* İlerleme Çizgisi */}
            <circle
              cx="50" cy="50" r="45" stroke="white" strokeWidth="8" fill="none"
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
      
      {/* -------------------- ANA İÇERİK BÖLÜMÜ (Dinamik) -------------------- */}
      <div className={`mt-6 pt-6 ${!showLadder ? 'border-t border-white/20' : ''}`}>
        
        {/* MERDİVEN GİZLİ (Aktif Hedef Görünümü) */}
        {!showLadder && (
          <div className="space-y-4">
            {/* Aktif Hedef Özet Alanı (Beyaz Karttan Kopyalandı) */}
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 border-2 border-white/30 transition-all duration-300">
              
              {/* Başlık ve Net Bilgisi */}
              <div className="flex items-center gap-2 mb-3">
                <span className="text-2xl">{getStatusEmoji(goal.progressPercent)}</span>
                <div className="flex-1">
                  <div className="text-xs opacity-90 font-medium">Aktif Hedef ({goal.level}. Tercih)</div>
                  <div className="text-lg font-bold leading-tight">{goal.university}</div>
                  <div className="text-xs opacity-75">{goal.department}</div>
                </div>
              </div>

              {/* Progress Bar ve Özet */}
              <div className="bg-white/10 rounded-lg p-3 mb-3">
                <div className="flex justify-between items-center mb-2">
                  <div className="text-sm">
                    <span className="opacity-75">Mevcut Net:</span>
                    <span className="font-bold ml-2 text-xl">{goal.currentNet}</span>
                  </div>
                  <div className="text-sm">
                    <span className="opacity-75">Hedef:</span>
                    <span className="font-bold ml-2 text-xl">{goal.targetNet}</span>
                  </div>
                </div>
                <div className="w-full h-3 bg-white/20 rounded-full overflow-hidden">
                  <div
                    className={`h-full bg-gradient-to-r ${getProgressColor(goal.progressPercent)} transition-all duration-1000`}
                    style={{ width: `${goal.progressPercent}%` }}
                  />
                </div>
                <div className="flex justify-between text-xs opacity-75 mt-1">
                  <span>0</span>
                  <span className="font-bold">%{goal.progressPercent}</span>
                  <span>{goal.targetNet}</span>
                </div>
              </div>
              
              {/* Durum Mesajı (120 net daha gerekli vb.) */}
              <div className="space-y-2 text-sm">
                {goal.remainingNet > 0 && (
                  <>
                    <div className="flex items-center gap-2">
                      <span className="text-orange-200">⚠️</span>
                      <span><strong>{goal.remainingNet} net</strong> daha gerekli</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-blue-200">💡</span>
                      <span>
                        Günde <strong>{goal.dailyIncreaseNeeded} net</strong> artırsan{' '}
                        <strong>{goal.daysToReach} günde</strong> hedefe ulaşırsın
                      </span>
                    </div>
                  </>
                )}
              </div>
              
              {/* Aktif Detayları Göster Butonu */}
              <button
                onClick={() => setShowActiveDetails(!showActiveDetails)}
                className="mt-4 text-xs opacity-75 hover:opacity-100 transition-opacity underline w-full text-center"
              >
                {showActiveDetails ? '▲ Ders detaylarını gizle' : '▼ Ders detaylarını göster'}
              </button>
              
              {/* Aktif Detaylar (Ders Bazlı Net) */}
              {showActiveDetails && goal.subjects && (
                <div className="mt-3 pt-3 border-t border-white/20 space-y-2 animate-fade-in">
                  <div className="text-xs font-bold opacity-90 mb-2">📚 DERS BAZLI HEDEFLER</div>
                  {goal.subjects.map((subject, index) => {
                    const subjectProgress = (subject.current / subject.target) * 100;
                    const subjectRemaining = subject.target - subject.current;
                    return (
                      <div key={index} className="bg-white/5 rounded-lg p-2">
                        <div className="flex justify-between text-xs mb-1">
                          <span className="font-medium">{subject.name}</span>
                          <span className="opacity-75">
                            {subject.current} / {subject.target} net
                          </span>
                        </div>
                        <div className="w-full h-1.5 bg-white/20 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-white/60 transition-all"
                            style={{ width: `${subjectProgress}%` }}
                          />
                        </div>
                        {subjectRemaining > 0 && (
                          <div className="text-xs opacity-75 mt-1">
                            **+{subjectRemaining} net gerekli**
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              )}
              
            </div>
            
          </div>
        )}

        {/* MERDİVEN AÇIK (5 Tercihli Merdiven Görünümü) */}
        {showLadder && (
          <div className="space-y-3 animate-fade-in">
            {/* Merdiven Detayları */}
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
      </div>

      {/* -------------------- Merdiven Açma/Kapama Butonu -------------------- */}
      <button
        onClick={() => {
          setShowLadder(!showLadder);
          // Merdiven açıldığında ders detaylarını gizlemek iyi bir UX kuralıdır.
          if (!showLadder) {
            setShowActiveDetails(false);
          }
        }}
        className="mt-4 text-xs opacity-75 hover:opacity-100 transition-opacity underline w-full text-center"
      >
        {showLadder ? '▲ Merdiveni Gizle' : '▼ Merdiveni Göster'}
      </button>
    </div>
  );
}