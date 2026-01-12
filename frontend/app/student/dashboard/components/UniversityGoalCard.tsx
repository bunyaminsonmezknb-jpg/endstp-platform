'use client';
import { useState, useEffect } from 'react';
import { api } from '@/lib/api/client';
import FeedbackButtons from './FeedbackButtons';

// Arayüz Tanımlamaları
interface SubjectGoal {
  name: string;
  current: number;
  target: number;
}

interface UniversityGoal {
  priority: number;
  universityName: string;
  departmentName: string;
  requiredTYT: number;
  requiredAYT: number;
  currentProgress: number;
  status: 'achieved' | 'close' | 'inProgress' | 'distant';
}

interface GoalData {
  overall_progress: number;
  days_remaining: number;
  tyt: {
    current_net: number;
    target_net: number;
    progress_percent: number;
    remaining_net: number;
    daily_increase_needed: number;
    subjects: SubjectGoal[];
  };
  ayt: {
    current_net: number;
    target_net: number;
    progress_percent: number;
    remaining_net: number;
    daily_increase_needed: number;
    subjects: SubjectGoal[];
  };
  active_goal: {
    university: string;
    department: string;
    level: number;
  };
  ladder: UniversityGoal[];
}

export default function UniversityGoalCard() {
  const [goalData, setGoalData] = useState<GoalData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showLadder, setShowLadder] = useState(false);
  const [showTYTDetails, setShowTYTDetails] = useState(false);
  const [showAYTDetails, setShowAYTDetails] = useState(false);

  useEffect(() => {
    fetchGoalData();
  }, []);

  const fetchGoalData = async () => {
    setIsLoading(true);
    setError(null);

    try {
      if (!userStr || !accessToken) {
        throw new Error('Lütfen giriş yapın');
      }

      const user = JSON.parse(userStr);

      const response = await api.post('/student/goal') as any;
      if (response.status === 'no_data') {
        setGoalData(null);
        } else {
          setGoalData(response);
        }
    } catch (err: any) {
      setError(err.message || 'Hedef bilgisi yüklenemedi');
    } finally {
      setIsLoading(false);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'achieved': return '✅';  // Yeşil tick
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

  if (isLoading) {
    return (
      <div className="bg-purple-100 rounded-2xl p-8 shadow-lg min-w-80">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-purple-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Hedef bilgisi yükleniyor...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border-2 border-red-300 rounded-2xl p-6 min-w-80">
        <div className="text-center">
          <div className="text-4xl mb-2">⚠️</div>
          <div className="text-red-700 font-bold mb-2">Hedef Bilgisi Hatası</div>
          <div className="text-sm text-red-600 mb-4">{error}</div>
          <button
            onClick={fetchGoalData}
            className="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700"
          >
            Tekrar Dene
          </button>
        </div>
      </div>
    );
  }

  if (!goalData) {
    return (
      <div className="bg-yellow-50 border-2 border-yellow-300 rounded-2xl p-8 text-center min-w-80">
        <div className="text-6xl mb-4">🎯</div>
        <h3 className="text-xl font-bold text-gray-800 mb-2">Henüz Hedef Verisi Yok</h3>
        <p className="text-gray-600 mb-4">
          Hedef hesaplayabilmek için önce test sonuçları girmelisiniz.
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

  return (
    <div className="bg-gradient-to-br from-purple-500 to-indigo-600 text-white rounded-2xl p-6 shadow-xl min-w-80">
      {/* ANA BAŞLIK */}
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-4">
          <div className="text-5xl">🏆</div>
          <div>
            <div className="text-sm opacity-90 font-medium">Nihai Hedef Yolculuğun</div>
            <div className="text-2xl font-bold leading-tight">
              Hedefine Doğru İlerliyorsun
            </div>
            <div className="text-xs opacity-75 mt-1">
              Genel İlerleme: <span className="font-bold">%{goalData.overall_progress}</span>
            </div>
          </div>
        </div>

        {/* İlerleme Halkası */}
        <div className="relative w-16 h-16 sm:w-20 sm:h-20 flex-shrink-0">
          <svg viewBox="0 0 100 100" className="transform -rotate-90">
            <circle cx="50" cy="50" r="45" stroke="rgba(255,255,255,0.2)" strokeWidth="8" fill="none" />
            <circle
              cx="50" cy="50" r="45" stroke="white" strokeWidth="8" fill="none"
              strokeDasharray="282.6"
              strokeDashoffset={282.6 * (1 - goalData.overall_progress / 100)}
              strokeLinecap="round"
              className="transition-all duration-1000"
            />
          </svg>
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-lg font-bold">{goalData.overall_progress}%</span>
          </div>
        </div>
      </div>

      {/* ANA İÇERİK */}
      <div className={`mt-6 pt-6 ${!showLadder ? 'border-t border-white/20' : ''}`}>
        
        {/* MERDİVEN GİZLİ - AKTİF HEDEF */}
        {!showLadder && (
          <div className="space-y-4">
            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 border-2 border-white/30">
              
              {/* Başlık */}
              <div className="flex items-center gap-2 mb-3">
                <span className="text-2xl">{getStatusEmoji(goalData.overall_progress)}</span>
                <div className="flex-1">
                  <div className="text-xs opacity-90 font-medium">Aktif Hedef ({goalData.active_goal.level}. Tercih)</div>
                  <div className="text-lg font-bold leading-tight">{goalData.active_goal.university}</div>
                  <div className="text-xs opacity-75">{goalData.active_goal.department}</div>
                </div>
              </div>

              {/* TYT BÖLÜMÜ */}
              <div className="bg-white/10 rounded-lg p-3 mb-3">
                <div className="flex justify-between items-center mb-2">
                  <div className="text-sm font-bold">📘 TYT</div>
                  <div className="text-sm">
                    <span className="font-bold text-xl">{goalData.tyt.current_net}</span>
                    <span className="opacity-75">/{goalData.tyt.target_net}</span>
                  </div>
                </div>
                <div className="w-full h-3 bg-white/20 rounded-full overflow-hidden">
                  <div
                    className={`h-full bg-gradient-to-r ${getProgressColor(goalData.tyt.progress_percent)} transition-all duration-1000`}
                    style={{ width: `${goalData.tyt.progress_percent}%` }}
                  />
                </div>
                <div className="flex justify-between text-xs opacity-75 mt-1">
                  <span>0</span>
                  <span className="font-bold">%{goalData.tyt.progress_percent}</span>
                  <span>{goalData.tyt.target_net}</span>
                </div>
                
                {/* TYT Detaylar */}
                <button
                  onClick={() => setShowTYTDetails(!showTYTDetails)}
                  className="mt-2 text-xs opacity-75 hover:opacity-100 transition-opacity underline w-full text-center"
                >
                  {showTYTDetails ? '▲ Ders detaylarını gizle' : '▼ Ders detaylarını göster'}
                </button>
                
                {showTYTDetails && (
                  <div className="mt-3 pt-3 border-t border-white/20 space-y-2">
                    {goalData.tyt.subjects.map((subject, index) => {
                      const subjectProgress = (subject.current / subject.target) * 100;
                      return (
                        <div key={index} className="bg-white/5 rounded-lg p-2">
                          <div className="flex justify-between text-xs mb-1">
                            <span className="font-medium">{subject.name}</span>
                            <span className="opacity-75">{subject.current} / {subject.target} net</span>
                          </div>
                          <div className="w-full h-1.5 bg-white/20 rounded-full overflow-hidden">
                            <div
                              className="h-full bg-white/60 transition-all"
                              style={{ width: `${subjectProgress}%` }}
                            />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>

              {/* AYT BÖLÜMÜ */}
              <div className="bg-white/10 rounded-lg p-3 mb-3">
                <div className="flex justify-between items-center mb-2">
                  <div className="text-sm font-bold">📗 AYT</div>
                  <div className="text-sm">
                    <span className="font-bold text-xl">{goalData.ayt.current_net}</span>
                    <span className="opacity-75">/{goalData.ayt.target_net}</span>
                  </div>
                </div>
                <div className="w-full h-3 bg-white/20 rounded-full overflow-hidden">
                  <div
                    className={`h-full bg-gradient-to-r ${getProgressColor(goalData.ayt.progress_percent)} transition-all duration-1000`}
                    style={{ width: `${goalData.ayt.progress_percent}%` }}
                  />
                </div>
                <div className="flex justify-between text-xs opacity-75 mt-1">
                  <span>0</span>
                  <span className="font-bold">%{goalData.ayt.progress_percent}</span>
                  <span>{goalData.ayt.target_net}</span>
                </div>
                
                {/* AYT Detaylar */}
                <button
                  onClick={() => setShowAYTDetails(!showAYTDetails)}
                  className="mt-2 text-xs opacity-75 hover:opacity-100 transition-opacity underline w-full text-center"
                >
                  {showAYTDetails ? '▲ Ders detaylarını gizle' : '▼ Ders detaylarını göster'}
                </button>
                
                {showAYTDetails && (
                  <div className="mt-3 pt-3 border-t border-white/20 space-y-2">
                    {goalData.ayt.subjects.map((subject, index) => {
                      const subjectProgress = (subject.current / subject.target) * 100;
                      return (
                        <div key={index} className="bg-white/5 rounded-lg p-2">
                          <div className="flex justify-between text-xs mb-1">
                            <span className="font-medium">{subject.name}</span>
                            <span className="opacity-75">{subject.current} / {subject.target} net</span>
                          </div>
                          <div className="w-full h-1.5 bg-white/20 rounded-full overflow-hidden">
                            <div
                              className="h-full bg-white/60 transition-all"
                              style={{ width: `${subjectProgress}%` }}
                            />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
              
              {/* DURUM MESAJI */}
              <div className="space-y-2 text-sm">
                {/* Sınav Tarihi Geçtiyse */}
                {goalData.days_remaining <= 0 && (
                  <div className="flex items-center gap-2 bg-red-500/20 rounded-lg p-2">
                    <span className="text-red-200">⚠️</span>
                    <span className="text-red-200">
                      Sınav tarihi geçti! Yeni bir hedef ve tarih belirlemelisin.
                    </span>
                  </div>
                )}
                
                {/* Sınav Henüz Gelmemişse */}
                {goalData.days_remaining > 0 && (
                  <>
                    {/* TYT Mesajı */}
                    {goalData.tyt.remaining_net > 0 ? (
                      <div className="flex items-center gap-2">
                        <span className="text-blue-200">📘</span>
                        <span>
                          <strong>{goalData.tyt.remaining_net} net</strong> daha gerekli (TYT)
                          {goalData.tyt.daily_increase_needed > 0 && (
                            <> • Günde <strong>{goalData.tyt.daily_increase_needed}</strong> net artırsan yetişir</>
                          )}
                        </span>
                      </div>
                    ) : (
                      <div className="flex items-center gap-2 bg-green-500/20 rounded-lg p-2">
                        <span className="text-green-200">🎉</span>
                        <span className="text-green-200 font-bold">TYT hedefini başardın!</span>
                      </div>
                    )}
                    
                    {/* AYT Mesajı */}
                    {goalData.ayt.remaining_net > 0 ? (
                      <div className="flex items-center gap-2">
                        <span className="text-orange-200">📗</span>
                        <span>
                          <strong>{goalData.ayt.remaining_net} net</strong> daha gerekli (AYT)
                          {goalData.ayt.daily_increase_needed > 0 && (
                            <> • Günde <strong>{goalData.ayt.daily_increase_needed}</strong> net artırsan yetişir</>
                          )}
                        </span>
                      </div>
                    ) : (
                      <div className="flex items-center gap-2 bg-green-500/20 rounded-lg p-2">
                        <span className="text-green-200">🎉</span>
                        <span className="text-green-200 font-bold">AYT hedefini başardın!</span>
                      </div>
                    )}
                    
                    {/* Geri Sayım */}
                    <div className="flex items-center gap-2">
                      <span className="text-yellow-200">⏰</span>
                      <span>Sınava <strong>{goalData.days_remaining} gün</strong> kaldı!</span>
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
        )}

        {/* MERDİVEN AÇIK */}
        {showLadder && (
          <div className="space-y-3 animate-fade-in">
            {[...goalData.ladder].reverse().map((goal) => (
              <div
                key={goal.priority}
                className={`${
                  goal.status === 'achieved' 
                    ? 'bg-green-500/30 border-2 border-green-400' 
                    : 'bg-white/10'
                } backdrop-blur-sm rounded-xl p-4 hover:bg-white/20 transition-all cursor-pointer`}
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

                <div className="w-full bg-white/20 rounded-full h-2 overflow-hidden">
                  <div
                    className={`h-full ${getStatusColor(goal.status)} transition-all duration-500`}
                    style={{ width: `${goal.currentProgress}%` }}
                  />
                </div>

                <div className="mt-2 text-xs opacity-75">
                  TYT: {goal.requiredTYT} • AYT: {goal.requiredAYT}
                </div>
              </div>
            ))}

            <div className="bg-yellow-500/20 rounded-xl p-3 text-xs">
              <span className="font-bold">💡 Koçluk İpucu:</span> En üst hedefine odaklan, 
              diğerleri doğal olarak gelecek!
            </div>
          </div>
        )}
      </div>

      {/* MERDİVEN AÇMA/KAPAMA */}
      <button
        onClick={() => {
          setShowLadder(!showLadder);
          if (!showLadder) {
            setShowTYTDetails(false);
            setShowAYTDetails(false);
          }
        }}
        className="mt-4 text-xs opacity-75 hover:opacity-100 transition-opacity underline w-full text-center"
      >
        {showLadder ? '▲ Merdiveni Gizle' : '▼ Merdiveni Göster'}
      </button>

      {/* FEEDBACK BUTONU */}
      <div className="mt-4 pt-4 border-t border-white/20 flex justify-center">
        <FeedbackButtons
          componentType="goal_card"
          variant="like-dislike"
          size="sm"
          metadata={{ 
            overall_progress: goalData.overall_progress,
            tyt_progress: goalData.tyt.progress_percent,
            ayt_progress: goalData.ayt.progress_percent
          }}
        />
      </div>
    </div>
  );
}