'use client';

import React, { useState, useMemo, useCallback } from 'react';

/**
 * ✅ ALTIN STANDART HERO STATS (FINAL)
 * - Null/undefined tolerant UI (asla çökmez)
 * - Division by zero guards (Infinity/NaN yok)
 * - any[] yerine tipli veri modelleri
 * - Mevcut tüm özellikler: flip kartlar, dinamik hedef, görev listesi, ders katkı paneli, zaman dağılımı
 */

// ====== TYPES (ALTIN STANDART) ======
type TaskStatus = 'pending' | 'completed';
type TaskType = 'test' | 'study';

interface Task {
  id: string;
  status: TaskStatus;
  task_type: TaskType;
  topic_name?: string | null;
  estimated_time_minutes: number;
}

interface WeeklySubjectItem {
  name?: string | null;
  avg_success?: number | null;
  total_tests?: number | null;
}

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
  tasksList?: Task[];
  weeklySubjects?: {
    worst_subjects: WeeklySubjectItem[];
    best_subjects: WeeklySubjectItem[];
    all_subjects: WeeklySubjectItem[];
  };
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

function HeroStats({
  dailyGoal,
  weeklySuccess,
  weeklyTarget,
  studyTimeToday,
  weeklyQuestions,
  weeklyIncrease,
  tasksList = [],
  weeklySubjects = { worst_subjects: [], best_subjects: [], all_subjects: [] },
  projection,
}: HeroStatsProps) {
  const [flippedCard, setFlippedCard] = useState<string | null>(null);

  const toggleFlip = useCallback((cardId: string) => {
    setFlippedCard((prev) => (prev === cardId ? null : cardId));
  }, []);

  const formatTime = useCallback((minutes: number): string => {
    const safe = Number.isFinite(minutes) ? Math.max(0, Math.floor(minutes)) : 0;
    if (safe === 0) return '0 dk';
    if (safe < 60) return `${safe} dk`;

    const hours = Math.floor(safe / 60);
    const mins = safe % 60;

    if (mins === 0) return `${hours} sa`;
    return `${hours} sa ${mins} dk`;
  }, []);

  // ✅ ALTIN STANDART: Division by zero / NaN guard
  const dailyProgress = useMemo(() => {
    const target = Number.isFinite(dailyGoal?.target) ? dailyGoal.target : 0;
    const current = Number.isFinite(dailyGoal?.current) ? dailyGoal.current : 0;
    if (!target || target <= 0) return 0;
    return (current / target) * 100;
  }, [dailyGoal?.current, dailyGoal?.target]);

  const weeklyProgress = useMemo(() => {
    const target = Number.isFinite(weeklyTarget) ? weeklyTarget : 0;
    const current = Number.isFinite(weeklySuccess) ? weeklySuccess : 0;
    if (!target || target <= 0) return 0;
    return (current / target) * 100;
  }, [weeklySuccess, weeklyTarget]);

  const dynamicGoal = useMemo(() => {
    const currentWeeklySuccess = Number.isFinite(weeklySuccess) ? weeklySuccess : 0;
    const dynamicTarget = Math.min(currentWeeklySuccess + 10, 100);
    const gap = dynamicTarget - currentWeeklySuccess;

    let message = '';
    if (gap <= 5) {
      message = `Hedefine çok yakınsın! ${gap} puan kaldı 🎯`;
    } else if (gap <= 10) {
      message = `Bu hafta ${gap} puan daha iyisini hedefle! 💪`;
    } else {
      message = `${gap} puanlık gelişim için hazır mısın? 🚀`;
    }

    return {
      current: currentWeeklySuccess,
      target: dynamicTarget,
      message,
      isRealistic: gap <= 15,
    };
  }, [weeklySuccess]);

  const pendingTasks = useMemo(
    () => tasksList.filter((t) => t?.status === 'pending'),
    [tasksList]
  );

  const completedTasks = useMemo(
    () => tasksList.filter((t) => t?.status === 'completed'),
    [tasksList]
  );

  const testTime = useMemo(() => {
    return completedTasks
      .filter((t) => t?.task_type === 'test')
      .reduce((sum, t) => sum + (Number.isFinite(t.estimated_time_minutes) ? t.estimated_time_minutes : 0), 0);
  }, [completedTasks]);

  const studyTime = useMemo(() => {
    return completedTasks
      .filter((t) => t?.task_type === 'study')
      .reduce((sum, t) => sum + (Number.isFinite(t.estimated_time_minutes) ? t.estimated_time_minutes : 0), 0);
  }, [completedTasks]);

  // (projection şu an UI’da kullanılmıyor — mevcut davranışı bozmamak için aynen bırakıldı)
  void projection;

  // Safe numbers for UI
  const safeDailyCurrent = Number.isFinite(dailyGoal?.current) ? dailyGoal.current : 0;
  const safeDailyTarget = Number.isFinite(dailyGoal?.target) ? dailyGoal.target : 0;
  const remainingDaily = Math.max(0, safeDailyTarget - safeDailyCurrent);

  const safeStudyTimeToday = Number.isFinite(studyTimeToday) ? studyTimeToday : 0;
  const safeWeeklyQuestions = Number.isFinite(weeklyQuestions) ? weeklyQuestions : 0;
  const safeWeeklyIncrease = Number.isFinite(weeklyIncrease) ? weeklyIncrease : 0;

  return (
    <div className="mb-6">
      <div className="bg-white rounded-3xl p-8 shadow-lg">
        <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
          📊 Bugünkü Durum
          <span className="text-xs text-gray-500 font-normal ml-2">
            (Detayları görmek için karta tıkla)
          </span>
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
                transform: flippedCard === 'daily' ? 'rotateY(180deg)' : 'rotateY(0deg)',
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
                    {safeDailyCurrent} / {safeDailyTarget}
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
                  📚 Bu hafta {safeWeeklyQuestions} soru (+%{safeWeeklyIncrease})
                </div>
              </div>

              {/* Arka Yüz */}
              <div
                className="absolute w-full h-full bg-gradient-to-br from-cyan-100 to-cyan-200 rounded-2xl p-6 border-2 border-cyan-300"
                style={{
                  backfaceVisibility: 'hidden',
                  transform: 'rotateY(180deg)',
                }}
              >
                <div className="text-center mb-3">
                  <div className="text-3xl mb-2">📋</div>
                  <div className="text-lg font-bold text-gray-800">
                    Kalan {remainingDaily} Görev
                  </div>
                </div>

                <div className="space-y-2 text-sm max-h-40 overflow-y-auto">
                  {pendingTasks.length > 0 ? (
                    pendingTasks.slice(0, 4).map((task) => (
                      <div key={task.id} className="bg-white rounded-lg p-2 flex items-center gap-2">
                        <span>{task.task_type === 'test' ? '📝' : '📚'}</span>
                        <span className="flex-1 text-xs">{task.topic_name ?? 'Konu Adı Yok'}</span>
                        <span className="text-xs font-semibold text-gray-600">
                          {Number.isFinite(task.estimated_time_minutes) ? task.estimated_time_minutes : 0} dk
                        </span>
                      </div>
                    ))
                  ) : (
                    <div className="bg-green-50 rounded-lg p-3 text-center">
                      <span className="text-2xl">🎉</span>
                      <p className="text-xs text-green-700 mt-1">Tüm görevler tamamlandı!</p>
                    </div>
                  )}

                  {pendingTasks.length > 4 && (
                    <div className="text-center text-xs text-gray-500 pt-1">
                      +{pendingTasks.length - 4} görev daha
                    </div>
                  )}
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
                transform: flippedCard === 'weekly' ? 'rotateY(180deg)' : 'rotateY(0deg)',
              }}
            >
              {/* Ön Yüz */}
              <div
                className="absolute w-full h-full bg-gradient-to-br from-purple-50 to-purple-100 rounded-2xl p-6 border-2 border-purple-200 group-hover:shadow-xl transition-shadow"
                style={{ backfaceVisibility: 'hidden' }}
              >
                <div className="text-center mb-4">
                  <div className="text-5xl mb-2">📈</div>
                  <div className="text-4xl font-bold text-gray-800">%{Number.isFinite(weeklySuccess) ? weeklySuccess : 0}</div>
                  <div className="text-sm text-gray-600 mt-1">Son 7 Gün Başarı</div>
                </div>

                <div className="w-full bg-white/50 rounded-full h-3 overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-purple-400 to-purple-600 transition-all duration-500"
                    style={{ width: `${Math.min(weeklyProgress, 100)}%` }}
                  />
                </div>

                <div className="text-center mt-4 text-xs text-gray-600">🎯 {dynamicGoal.message}</div>
                <div className="text-center mt-1 text-xs font-semibold text-purple-600">
                  Hedef: %{dynamicGoal.target}
                </div>
              </div>

              {/* Arka Yüz */}
              <div
                className="absolute w-full h-full bg-gradient-to-br from-purple-100 to-purple-200 rounded-2xl p-6 border-2 border-purple-300"
                style={{
                  backfaceVisibility: 'hidden',
                  transform: 'rotateY(180deg)',
                }}
              >
                <div className="text-center mb-3">
                  <div className="text-3xl mb-2">🔍</div>
                  <div className="text-lg font-bold text-gray-800">Suçlu Kim?</div>
                </div>

                <div className="space-y-2 text-sm">
                  {/* Ortalamayı Düşürenler */}
                  {weeklySubjects?.worst_subjects?.length > 0 ? (
                    <div className="bg-red-100 rounded-lg p-2">
                      <div className="font-bold text-red-700 mb-1">📉 Ortalamayı Düşürenler:</div>
                      {weeklySubjects.worst_subjects.map((subject, idx) => (
                        <div key={idx} className="text-gray-700 text-xs">
                          • {subject.name ?? 'Ders Adı Yok'} (%{subject.avg_success ?? 0}) - {subject.total_tests ?? 0} test
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="bg-gray-100 rounded-lg p-2">
                      <div className="text-gray-600 text-xs text-center">Henüz yeterli veri yok</div>
                    </div>
                  )}

                  {/* Sırtlayanlar */}
                  {weeklySubjects?.best_subjects?.length > 0 ? (
                    <div className="bg-green-100 rounded-lg p-2">
                      <div className="font-bold text-green-700 mb-1">📈 Sırtlayanlar:</div>
                      {weeklySubjects.best_subjects.map((subject, idx) => (
                        <div key={idx} className="text-gray-700 text-xs">
                          • {subject.name ?? 'Ders Adı Yok'} (%{subject.avg_success ?? 0}) - {subject.total_tests ?? 0} test
                        </div>
                      ))}
                    </div>
                  ) : weeklySubjects?.worst_subjects?.length > 0 ? (
                    <div className="bg-blue-100 rounded-lg p-2">
                      <div className="text-blue-700 text-xs text-center">Tüm dersler aynı seviyede</div>
                    </div>
                  ) : null}
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
                transform: flippedCard === 'time' ? 'rotateY(180deg)' : 'rotateY(0deg)',
              }}
            >
              {/* Ön Yüz */}
              <div
                className="absolute w-full h-full bg-gradient-to-br from-blue-50 to-blue-100 rounded-2xl p-6 border-2 border-blue-200 group-hover:shadow-xl transition-shadow"
                style={{ backfaceVisibility: 'hidden' }}
              >
                <div className="text-center mb-4">
                  <div className="text-5xl mb-2">⏱️</div>
                  <div className="text-4xl font-bold text-gray-800">{formatTime(safeStudyTimeToday)}</div>
                  <div className="text-sm text-gray-600 mt-1">Bugün Çalışma Süresi</div>
                </div>

                <div className="w-full bg-white/50 rounded-full h-3 overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-blue-400 to-blue-600 transition-all duration-500"
                    style={{ width: `${Math.min((safeStudyTimeToday / 180) * 100, 100)}%` }}
                  />
                </div>

                <div className="text-center mt-4 text-xs text-gray-500">
                  {safeStudyTimeToday < 60 ? '⚡ Daha fazla çalışabilirsin!' : '🔥 Harika gidiyorsun!'}
                </div>
              </div>

              {/* Arka Yüz */}
              <div
                className="absolute w-full h-full bg-gradient-to-br from-blue-100 to-blue-200 rounded-2xl p-6 border-2 border-blue-300"
                style={{
                  backfaceVisibility: 'hidden',
                  transform: 'rotateY(180deg)',
                }}
              >
                <div className="text-center mb-3">
                  <div className="text-3xl mb-2">⏳</div>
                  <div className="text-lg font-bold text-gray-800">Zaman Dağılımı</div>
                </div>

                <div className="space-y-2 text-sm">
                  <div className="bg-white rounded-lg p-2 flex justify-between items-center">
                    <span className="flex items-center gap-2">
                      <span>📝</span>
                      <span>Test</span>
                    </span>
                    <span className="font-bold">{formatTime(testTime)}</span>
                  </div>

                  <div className="bg-white rounded-lg p-2 flex justify-between items-center">
                    <span className="flex items-center gap-2">
                      <span>📚</span>
                      <span>Çalışma</span>
                    </span>
                    <span className="font-bold">{formatTime(studyTime)}</span>
                  </div>
                </div>

                <div className="mt-3 bg-blue-100 rounded-lg p-2 text-center">
                  <div className="text-xs text-blue-700 font-semibold">
                    {testTime > studyTime ? '📝 Test odaklı gidiyorsun!' : '📚 Çalışma odaklı gidiyorsun!'}
                  </div>
                </div>
              </div>
            </div>
          </div>
          {/* /KART 3 */}
        </div>
      </div>
    </div>
  );
}

export default React.memo(HeroStats);
