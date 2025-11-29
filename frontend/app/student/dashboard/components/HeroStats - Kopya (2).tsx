'use client';

import { useState } from 'react';

interface HeroStatsProps {
  dailyGoal: {
    current: number;
    target: number;
  };
  weeklySuccess: number;
  weeklyTarget: number;
  studyTimeToday: number;
  weeklyQuestions: number;
  weeklyIncrease: number;
  projection?: {
    status: string;
    totalTopics: number;
    completedTopics: number;
    remainingTopics: number;
    estimatedDays: number;
    estimatedDate: string;
    velocity: string;
    requiredVelocity?: string;
    warningLevel: string;
    message: string;
    velocityWarning?: string;
    daysUntilExam?: number;
  };
}

export default function HeroStats({ 
  dailyGoal, 
  weeklySuccess, 
  weeklyTarget, 
  studyTimeToday, 
  weeklyQuestions,
  weeklyIncrease,
  projection
}: HeroStatsProps) {
  const [flippedCard, setFlippedCard] = useState<string | null>(null);

  const dailyProgress = (dailyGoal.current / dailyGoal.target) * 100;
  const weeklyProgress = (weeklySuccess / weeklyTarget) * 100;

  const toggleFlip = (cardId: string) => {
    setFlippedCard(flippedCard === cardId ? null : cardId);
  };

  // Dinamik hedef hesaplama
  const calculateDynamicGoal = () => {
    const currentWeeklySuccess = weeklySuccess;
    const dynamicGoal = Math.min(currentWeeklySuccess + 10, 100);
    const gap = dynamicGoal - currentWeeklySuccess;
    
    let goalMessage = '';
    if (gap <= 5) {
      goalMessage = `Hedefine çok yakınsın! ${gap} puan kaldı 🎯`;
    } else if (gap <= 10) {
      goalMessage = `Bu hafta ${gap} puan daha iyisini hedefle! 💪`;
    } else {
      goalMessage = `${gap} puanlık gelişim için hazır mısın? 🚀`;
    }
    
    return {
      current: currentWeeklySuccess,
      target: dynamicGoal,
      message: goalMessage,
      isRealistic: gap <= 15
    };
  };

  const dynamicGoal = calculateDynamicGoal();

  return (
    <div className="mb-6">
      <div className="bg-white rounded-3xl p-8 shadow-lg">
        <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
          📊 Bugünkü Durum
          <span className="text-xs text-gray-500 font-normal ml-2">(Detayları görmek için karta tıkla)</span>
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* KART 1: Günlük Hedef */}
          <div 
            className="relative h-64 cursor-pointer group"
            onClick={() => toggleFlip('daily')}
            style={{ perspective: '1000px' }}
          >
            <div
              className="absolute w-full h-full transition-transform duration-500"
              style={{
                transformStyle: 'preserve-3d',
                transform: flippedCard === 'daily' ? 'rotateY(180deg)' : 'rotateY(0deg)'
              }}
            >
              {/* Ön Yüz */}
              <div
                className="absolute w-full h-full bg-gradient-to-br from-cyan-50 to-cyan-100 rounded-2xl p-6 border-2 border-cyan-200 group-hover:shadow-xl transition-shadow"
                style={{ backfaceVisibility: 'hidden' }}
              >
                <div className="text-center mb-4">
                  <div className="text-5xl mb-2">🎯</div>
                  <div className="text-4xl font-bold text-gray-800">
                    {dailyGoal.current} / {dailyGoal.target}
                  </div>
                  <div className="text-sm text-gray-600 mt-1">Bugünkü Hedefin</div>
                </div>
                <div className="w-full bg-white/50 rounded-full h-3 overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-cyan-400 to-cyan-600 transition-all duration-500"
                    style={{ width: `${Math.min(dailyProgress, 100)}%` }}
                  />
                </div>
                <div className="text-center mt-4 text-xs text-gray-500">
                  📚 Bu hafta {weeklyQuestions} soru (+%{weeklyIncrease})
                </div>
              </div>

              {/* Arka Yüz */}
              <div
                className="absolute w-full h-full bg-gradient-to-br from-cyan-100 to-cyan-200 rounded-2xl p-6 border-2 border-cyan-300"
                style={{ 
                  backfaceVisibility: 'hidden',
                  transform: 'rotateY(180deg)'
                }}
              >
                <div className="text-center mb-3">
                  <div className="text-3xl mb-2">📋</div>
                  <div className="text-lg font-bold text-gray-800">Kalan {dailyGoal.target - dailyGoal.current} Görev</div>
                </div>
                <div className="space-y-2 text-sm">
                  <div className="bg-white rounded-lg p-2 flex items-center gap-2">
                    <span>🎥</span>
                    <span>2 Video (Fizik)</span>
                  </div>
                  <div className="bg-white rounded-lg p-2 flex items-center gap-2">
                    <span>📝</span>
                    <span>40 Soru (Matematik)</span>
                  </div>
                  <div className="bg-white rounded-lg p-2 flex items-center gap-2">
                    <span>📊</span>
                    <span>1 Deneme Analizi</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* KART 2: Haftalık Başarı - DİNAMİK HEDEF */}
          <div 
            className="relative h-64 cursor-pointer group"
            onClick={() => toggleFlip('weekly')}
            style={{ perspective: '1000px' }}
          >
            <div
              className="absolute w-full h-full transition-transform duration-500"
              style={{
                transformStyle: 'preserve-3d',
                transform: flippedCard === 'weekly' ? 'rotateY(180deg)' : 'rotateY(0deg)'
              }}
            >
              {/* Ön Yüz */}
              <div
                className="absolute w-full h-full bg-gradient-to-br from-purple-50 to-purple-100 rounded-2xl p-6 border-2 border-purple-200 group-hover:shadow-xl transition-shadow"
                style={{ backfaceVisibility: 'hidden' }}
              >
                <div className="text-center mb-4">
                  <div className="text-5xl mb-2">📈</div>
                  <div className="text-4xl font-bold text-gray-800">
                    %{weeklySuccess}
                  </div>
                  <div className="text-sm text-gray-600 mt-1">Son 7 Gün Başarı</div>
                </div>
                <div className="w-full bg-white/50 rounded-full h-3 overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-purple-400 to-purple-600 transition-all duration-500"
                    style={{ width: `${Math.min(weeklyProgress, 100)}%` }}
                  />
                </div>
                <div className="text-center mt-4 text-xs text-gray-600">
                  🎯 {dynamicGoal.message}
                </div>
                <div className="text-center mt-1 text-xs font-semibold text-purple-600">
                  Hedef: %{dynamicGoal.target}
                </div>
              </div>

              {/* Arka Yüz */}
              <div
                className="absolute w-full h-full bg-gradient-to-br from-purple-100 to-purple-200 rounded-2xl p-6 border-2 border-purple-300"
                style={{ 
                  backfaceVisibility: 'hidden',
                  transform: 'rotateY(180deg)'
                }}
              >
                <div className="text-center mb-3">
                  <div className="text-3xl mb-2">🔍</div>
                  <div className="text-lg font-bold text-gray-800">Suçlu Kim?</div>
                </div>
                <div className="space-y-2 text-sm">
                  <div className="bg-red-100 rounded-lg p-2">
                    <div className="font-bold text-red-700 mb-1">📉 Ortalamayı Düşürenler:</div>
                    <div className="text-gray-700">• Kimya (%40)</div>
                  </div>
                  <div className="bg-green-100 rounded-lg p-2">
                    <div className="font-bold text-green-700 mb-1">📈 Sırtlayanlar:</div>
                    <div className="text-gray-700">• Tarih (%90)</div>
                    <div className="text-gray-700">• Edebiyat (%85)</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* KART 3: Çalışma Süresi */}
          <div 
            className="relative h-64 cursor-pointer group"
            onClick={() => toggleFlip('time')}
            style={{ perspective: '1000px' }}
          >
            <div
              className="absolute w-full h-full transition-transform duration-500"
              style={{
                transformStyle: 'preserve-3d',
                transform: flippedCard === 'time' ? 'rotateY(180deg)' : 'rotateY(0deg)'
              }}
            >
              {/* Ön Yüz */}
              <div
                className="absolute w-full h-full bg-gradient-to-br from-blue-50 to-blue-100 rounded-2xl p-6 border-2 border-blue-200 group-hover:shadow-xl transition-shadow"
                style={{ backfaceVisibility: 'hidden' }}
              >
                <div className="text-center mb-4">
                  <div className="text-5xl mb-2">⏱️</div>
                  <div className="text-4xl font-bold text-gray-800">
                    {(studyTimeToday / 60).toFixed(1)} sa
                  </div>
                  <div className="text-sm text-gray-600 mt-1">Bugün Çalışma Süresi</div>
                </div>
                <div className="w-full bg-white/50 rounded-full h-3 overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-blue-400 to-blue-600 transition-all duration-500"
                    style={{ width: `${Math.min((studyTimeToday / 180) * 100, 100)}%` }}
                  />
                </div>
                <div className="text-center mt-4 text-xs text-gray-500">
                  {studyTimeToday < 60 ? '⚡ Daha fazla çalışabilirsin!' : '🔥 Harika gidiyorsun!'}
                </div>
              </div>

              {/* Arka Yüz */}
              <div
                className="absolute w-full h-full bg-gradient-to-br from-blue-100 to-blue-200 rounded-2xl p-6 border-2 border-blue-300"
                style={{ 
                  backfaceVisibility: 'hidden',
                  transform: 'rotateY(180deg)'
                }}
              >
                <div className="text-center mb-3">
                  <div className="text-3xl mb-2">⏳</div>
                  <div className="text-lg font-bold text-gray-800">Zaman Dağılımı</div>
                </div>
                <div className="space-y-2 text-sm">
                  <div className="bg-white rounded-lg p-2 flex justify-between items-center">
                    <span className="flex items-center gap-2">
                      <span>🎥</span>
                      <span>Video</span>
                    </span>
                    <span className="font-bold">1.5 sa</span>
                  </div>
                  <div className="bg-white rounded-lg p-2 flex justify-between items-center">
                    <span className="flex items-center gap-2">
                      <span>📝</span>
                      <span>Test</span>
                    </span>
                    <span className="font-bold">1 sa</span>
                  </div>
                </div>
                <div className="mt-3 bg-orange-100 rounded-lg p-2 text-center">
                  <div className="text-xs text-orange-700 font-semibold">
                    💡 Test süreni artırmalısın!
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
