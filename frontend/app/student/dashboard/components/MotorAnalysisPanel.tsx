'use client';

import { useState, useEffect } from 'react';
import { getMotorAnalysis, type TopicAnalysisOutput } from '@/lib/api-client';

/**
 * 4 MOTOR ANALİZ PANELİ - v3
 * 
 * Güncellemeler:
 * - Tüm terimler Türkçeleştirildi
 * - Durum etiketlerine açıklama eklendi
 * - CRITICAL → KRİTİK
 * - Ease Factor → Kolaylık Faktörü
 * - Pace Ratio → Tempo Oranı
 */

export default function MotorAnalysisPanel() {
  const [analysisData, setAnalysisData] = useState<TopicAnalysisOutput[] | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedMotor, setSelectedMotor] = useState<'all' | 'priority' | 'difficulty' | 'time' | 'bs'>('all');

  const runDemoAnalysis = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const result = await getMotorAnalysis([
        {
          topic_id: 1,
          topic_name: "Türev",
          correct: 5,
          incorrect: 3,
          blank: 2,
          total_questions: 10,
          duration_minutes: 15,
          repetitions: 2,
          difficulty_baseline: 4
        },
        {
          topic_id: 2,
          topic_name: "İntegral",
          correct: 7,
          incorrect: 2,
          blank: 1,
          total_questions: 10,
          duration_minutes: 12,
          repetitions: 3,
          difficulty_baseline: 3
        },
        {
          topic_id: 3,
          topic_name: "Limit",
          correct: 3,
          incorrect: 5,
          blank: 2,
          total_questions: 10,
          duration_minutes: 18,
          repetitions: 1,
          difficulty_baseline: 5
        }
      ]);

      if (result.error) {
        setError(result.error);
        return;
      }

      if (result.data) {
        setAnalysisData(result.data.topics);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Bilinmeyen hata');
    } finally {
      setIsLoading(false);
    }
  };

  // Öncelik seviyesi Türkçe çevirisi
  const getPriorityText = (level: string) => {
    const map: Record<string, string> = {
      'CRITICAL': 'KRİTİK',
      'HIGH': 'YÜKSEK',
      'MEDIUM': 'ORTA',
      'LOW': 'DÜŞÜK'
    };
    return map[level] || level;
  };

  // Öncelik seviyesi açıklaması
  const getPriorityDescription = (level: string) => {
    const map: Record<string, string> = {
      'CRITICAL': 'Hemen çalış',
      'HIGH': 'Bu hafta çalış',
      'MEDIUM': '2 hafta içinde',
      'LOW': 'Rahat ol'
    };
    return map[level] || '';
  };

  const getPriorityColor = (level: string) => {
    switch (level) {
      case 'CRITICAL': return 'bg-red-500 text-white';
      case 'HIGH': return 'bg-orange-500 text-white';
      case 'MEDIUM': return 'bg-yellow-500 text-gray-900';
      case 'LOW': return 'bg-green-500 text-white';
      default: return 'bg-gray-500 text-white';
    }
  };

  const getDifficultyColor = (percentage: number) => {
    if (percentage >= 80) return 'text-red-600';
    if (percentage >= 60) return 'text-orange-600';
    if (percentage >= 40) return 'text-yellow-600';
    return 'text-green-600';
  };

  const getSpeedColor = (ratio: number) => {
    if (ratio > 1.3) return 'text-red-600';
    if (ratio > 1.1) return 'text-orange-600';
    if (ratio >= 0.9) return 'text-green-600';
    return 'text-blue-600';
  };

  // Durum metni ve açıklaması
  const getStatusInfo = (status: string) => {
    const statusMap: Record<string, { text: string; description: string }> = {
      'RESET': { text: 'YENİLE', description: 'Konuyu yeni öğreniyorsun' },
      'NORMAL': { text: 'NORMAL', description: 'Düzenli tekrar ediyorsun' },
      'HARD': { text: 'ZOR', description: 'Bu konu zor gidiyor' },
      'EASY': { text: 'KOLAY', description: 'Bu konu kolay geliyor' }
    };
    return statusMap[status.toUpperCase()] || { text: status, description: '' };
  };

  const filteredTopics = analysisData?.filter(topic => {
    if (selectedMotor === 'all') return true;
    if (selectedMotor === 'priority') return topic.priority_level === 'CRITICAL' || topic.priority_level === 'HIGH';
    if (selectedMotor === 'difficulty') return topic.difficulty_percentage >= 60;
    if (selectedMotor === 'time') return topic.pace_ratio > 1.2 || topic.pace_ratio < 0.8;
    if (selectedMotor === 'bs') return topic.next_interval <= 2;
    return true;
  });

  return (
    <div className="space-y-6">
      {/* Header with Demo Button */}
      <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-2xl p-6 shadow-xl">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-3xl font-bold mb-2">🚀 4 Motor Analiz Sistemi</h2>
            <p className="text-sm opacity-90">Akıllı Tekrar Planlayıcı • Zorluk Motoru • Hız Analizi • Öncelik Motoru</p>
          </div>
          <button
            onClick={runDemoAnalysis}
            disabled={isLoading}
            className="bg-white text-purple-600 px-6 py-3 rounded-xl font-bold hover:scale-105 transition-transform disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? '⏳ Analiz ediliyor...' : '🎯 Demo Analiz Çalıştır'}
          </button>
        </div>
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="bg-white rounded-2xl p-12 text-center shadow-lg">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-purple-600 mx-auto mb-4"></div>
          <p className="text-gray-600 text-lg">4 Motor çalışıyor...</p>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="bg-red-50 border-2 border-red-200 rounded-2xl p-6">
          <div className="flex items-center gap-3 text-red-600">
            <span className="text-3xl">⚠️</span>
            <div>
              <div className="font-bold text-lg">Hata Oluştu</div>
              <div className="text-sm">{error}</div>
            </div>
          </div>
        </div>
      )}

      {/* Analysis Results */}
      {analysisData && !isLoading && (
        <>
          {/* Motor Filter */}
          <div className="bg-white rounded-2xl p-6 shadow-lg">
            <h3 className="text-lg font-bold text-gray-800 mb-4">🔍 Motor Filtresi</h3>
            <div className="flex flex-wrap gap-3">
              <button
                onClick={() => setSelectedMotor('all')}
                className={`px-4 py-2 rounded-lg font-semibold transition-all ${
                  selectedMotor === 'all'
                    ? 'bg-purple-600 text-white shadow-lg'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                🌐 Tümü ({analysisData.length})
              </button>
              <button
                onClick={() => setSelectedMotor('priority')}
                className={`px-4 py-2 rounded-lg font-semibold transition-all ${
                  selectedMotor === 'priority'
                    ? 'bg-red-600 text-white shadow-lg'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                🎯 Öncelik (Kritik/Yüksek)
              </button>
              <button
                onClick={() => setSelectedMotor('difficulty')}
                className={`px-4 py-2 rounded-lg font-semibold transition-all ${
                  selectedMotor === 'difficulty'
                    ? 'bg-orange-600 text-white shadow-lg'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                📊 Zorluk (>%60)
              </button>
              <button
                onClick={() => setSelectedMotor('time')}
                className={`px-4 py-2 rounded-lg font-semibold transition-all ${
                  selectedMotor === 'time'
                    ? 'bg-blue-600 text-white shadow-lg'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                ⏱️ Hız Sorunu
              </button>
              <button
                onClick={() => setSelectedMotor('bs')}
                className={`px-4 py-2 rounded-lg font-semibold transition-all ${
                  selectedMotor === 'bs'
                    ? 'bg-green-600 text-white shadow-lg'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                🔄 Acil Tekrar (≤2 gün)
              </button>
            </div>
          </div>

          {/* Topics List */}
          <div className="space-y-4">
            {filteredTopics && filteredTopics.length > 0 ? (
              filteredTopics.map((topic) => {
                const statusInfo = getStatusInfo(topic.status);
                
                return (
                  <div key={topic.topic_id} className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-shadow">
                    {/* Header */}
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center gap-3">
                        <div className="text-3xl">📚</div>
                        <div>
                          <h3 className="text-xl font-bold text-gray-800">{topic.topic_name}</h3>
                          <div className="flex items-center gap-2 mt-1">
                            <div className="flex flex-col">
                              <span className={`px-3 py-1 rounded-full text-xs font-bold ${getPriorityColor(topic.priority_level)}`}>
                                {getPriorityText(topic.priority_level)}
                              </span>
                              <span className="text-xs text-gray-500 italic mt-1">
                                {getPriorityDescription(topic.priority_level)}
                              </span>
                            </div>
                            <span className="text-xs text-gray-500">Öncelik Skoru: {topic.priority_score.toFixed(2)}</span>
                          </div>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-bold text-purple-600">{statusInfo.text}</div>
                        <div className="text-xs text-gray-500 italic">{statusInfo.description}</div>
                      </div>
                    </div>

                    {/* 4 Motor Sonuçları */}
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                      {/* Akıllı Tekrar Planlayıcı Motor */}
                      <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-xl p-4 border-2 border-green-200">
                        <div className="text-sm font-bold text-green-700 mb-2">🔄 Akıllı Tekrar Planlayıcı</div>
                        <div className="text-xs text-gray-600 mb-3 italic">
                          Unutma Eğrisi Motoruna göre en uygun tekrar zamanını hesaplar
                        </div>
                        <div className="space-y-1 text-sm">
                          <div className="flex justify-between">
                            <span className="text-gray-600">Sonraki Tekrar:</span>
                            <span className="font-semibold">{topic.next_interval} gün</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-600">Tarih:</span>
                            <span className="font-semibold text-xs">{new Date(topic.next_review_date).toLocaleDateString('tr-TR')}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-600">Kolaylık Faktörü:</span>
                            <span className="font-semibold">{topic.next_ease_factor.toFixed(2)}</span>
                          </div>
                        </div>
                      </div>

                      {/* Zorluk Motoru */}
                      <div className="bg-gradient-to-br from-orange-50 to-orange-100 rounded-xl p-4 border-2 border-orange-200">
                        <div className="text-sm font-bold text-orange-700 mb-2">📊 Zorluk Motoru</div>
                        <div className="text-xs text-gray-600 mb-3 italic">
                          Konunun sizin için ne kadar zor olduğunu analiz eder
                        </div>
                        <div className="space-y-1 text-sm">
                          <div className="flex justify-between">
                            <span className="text-gray-600">Seviye:</span>
                            <span className="font-semibold">{topic.difficulty_level}/5</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-600">Yüzde:</span>
                            <span className={`font-bold ${getDifficultyColor(topic.difficulty_percentage)}`}>
                              %{topic.difficulty_percentage.toFixed(1)}
                            </span>
                          </div>
                          <div className="w-full bg-white rounded-full h-2 mt-2">
                            <div
                              className="bg-orange-500 h-2 rounded-full transition-all"
                              style={{ width: `${Math.min(topic.difficulty_percentage, 100)}%` }}
                            />
                          </div>
                        </div>
                      </div>

                      {/* Hız Analizi Motoru */}
                      <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-4 border-2 border-blue-200">
                        <div className="text-sm font-bold text-blue-700 mb-2">⏱️ Hız Analizi</div>
                        <div className="text-xs text-gray-600 mb-3 italic">
                          Soru çözme hızınızı ve temponuzu ölçer
                        </div>
                        <div className="space-y-1 text-sm">
                          <div className="flex justify-between">
                            <span className="text-gray-600">Tempo Oranı:</span>
                            <span className={`font-bold ${getSpeedColor(topic.pace_ratio)}`}>
                              {topic.pace_ratio.toFixed(2)}x
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-600">Çarpan:</span>
                            <span className="font-semibold">{topic.time_modifier.toFixed(2)}</span>
                          </div>
                          <div className="text-xs text-gray-600 mt-2">
                            {topic.speed_note}
                          </div>
                        </div>
                      </div>

                      {/* Öncelik Motoru */}
                      <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl p-4 border-2 border-purple-200">
                        <div className="text-sm font-bold text-purple-700 mb-2">🎯 Öncelik Motoru</div>
                        <div className="text-xs text-gray-600 mb-3 italic">
                          Hangi konuya öncelik vereceğinizi belirler
                        </div>
                        <div className="space-y-1 text-sm">
                          <div className="flex justify-between">
                            <span className="text-gray-600">Skor:</span>
                            <span className="font-bold text-purple-600">{topic.priority_score.toFixed(2)}</span>
                          </div>
                          <div className="text-xs text-gray-600 mt-2">
                            {topic.suggestion}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })
            ) : (
              <div className="bg-gray-50 rounded-2xl p-12 text-center">
                <div className="text-4xl mb-3">🔍</div>
                <p className="text-gray-600">Bu filtrede konu bulunamadı</p>
              </div>
            )}
          </div>
        </>
      )}

      {/* Empty State */}
      {!analysisData && !isLoading && !error && (
        <div className="bg-white rounded-2xl p-12 text-center shadow-lg">
          <div className="text-6xl mb-4">🎯</div>
          <h3 className="text-2xl font-bold text-gray-800 mb-2">4 Motor Analizi Hazır</h3>
          <p className="text-gray-600 mb-6">
            Yukarıdaki butona tıklayarak demo analiz çalıştırabilirsiniz.
          </p>
          <div className="text-sm text-gray-500 space-y-1 max-w-2xl mx-auto">
            <p>✓ <strong>Akıllı Tekrar Planlayıcı:</strong> Unutma eğrisi ve sonraki tekrar tarihi</p>
            <p>✓ <strong>Zorluk Motoru:</strong> Konu zorluğu analizi</p>
            <p>✓ <strong>Hız Analizi:</strong> Hız ve tempo analizi</p>
            <p>✓ <strong>Öncelik Motoru:</strong> Akıllı önceliklendirme</p>
          </div>
        </div>
      )}
    </div>
  );
}
