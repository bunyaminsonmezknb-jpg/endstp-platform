'use client';

import { useState, useEffect } from 'react';

interface MotorTopic {
  topic_name: string;
  subject_name: string;
  urgency_score?: number;
  difficulty_score?: number;
  priority_score?: number;
  remembering_rate?: number;
  recommendation: string;
  priority_level?: string;
  next_review_urgency?: string;
  average_interval_days?: number;
  average_success?: number;
  total_tests?: number;
}

interface MotorAnalysisData {
  status: string;
  analyzed_topics: number;
  bs_model: {
    name: string;
    description: string;
    urgent_topics: MotorTopic[];
  };
  difficulty_engine: {
    name: string;
    description: string;
    struggling_topics: MotorTopic[];
  };
  time_analyzer: {
    name: string;
    description: string;
    slow_topics: MotorTopic[];
  };
  priority_engine: {
    name: string;
    description: string;
    this_week_topics: MotorTopic[];
  };
}

export default function MotorAnalysisPanel() {
  const [analysisData, setAnalysisData] = useState<MotorAnalysisData | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedMotor, setSelectedMotor] = useState<'all' | 'bs' | 'difficulty' | 'time' | 'priority'>('all');

  // Sayfa yüklendiğinde otomatik analiz yap
  useEffect(() => {
    runAnalysis();
  }, []);

  const runAnalysis = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const userStr = localStorage.getItem('user');
      const accessToken = localStorage.getItem('access_token');

      if (!userStr || !accessToken) {
        throw new Error('Lütfen giriş yapın');
      }

      const user = JSON.parse(userStr);

      const response = await fetch('http://localhost:8000/api/v1/student/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`,
        },
        body: JSON.stringify({
          student_id: user.id,
        }),
      });

      if (!response.ok) {
        throw new Error('Analiz başarısız');
      }

      const data = await response.json();
      setAnalysisData(data);
    } catch (err: any) {
      console.error('Motor analiz hatası:', err);
      setError(err.message || 'Analiz sırasında hata oluştu');
    } finally {
      setIsLoading(false);
    }
  };

  const getUrgencyColor = (urgency?: string) => {
    if (!urgency) return 'bg-gray-100 text-gray-700';
    switch (urgency) {
      case 'HEMEN': return 'bg-red-500 text-white';
      case 'ACİL': return 'bg-orange-500 text-white';
      case 'YAKIN': return 'bg-yellow-500 text-white';
      default: return 'bg-blue-500 text-white';
    }
  };

  const getPriorityColor = (level?: string) => {
    if (!level) return 'bg-gray-100 text-gray-700';
    switch (level) {
      case 'CRITICAL': return 'bg-red-500 text-white';
      case 'HIGH': return 'bg-orange-500 text-white';
      case 'MEDIUM': return 'bg-yellow-500 text-white';
      default: return 'bg-blue-500 text-white';
    }
  };
const getPriorityText = (level?: string) => {
  if (!level) return 'BELİRSİZ';
  switch (level) {
    case 'CRITICAL': return 'KRİTİK';
    case 'HIGH': return 'YÜKSEK';
    case 'MEDIUM': return 'ORTA';
    case 'LOW': return 'DÜŞÜK';
    default: return level;
  }
};
  if (isLoading) {
    return (
      <div className="bg-white rounded-2xl p-8 shadow-lg">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-purple-600 mx-auto mb-4"></div>
          <p className="text-gray-600">4 Motor analizi yapılıyor...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border-2 border-red-300 rounded-2xl p-6">
        <div className="text-center">
          <div className="text-4xl mb-2">⚠️</div>
          <div className="text-red-700 font-bold mb-2">Analiz Hatası</div>
          <div className="text-sm text-red-600 mb-4">{error}</div>
          <button
            onClick={runAnalysis}
            className="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700"
          >
            Tekrar Dene
          </button>
        </div>
      </div>
    );
  }

  if (!analysisData || analysisData.status === 'no_data') {
    return (
      <div className="bg-yellow-50 border-2 border-yellow-300 rounded-2xl p-8 text-center">
        <div className="text-6xl mb-4">📊</div>
        <h3 className="text-xl font-bold text-gray-800 mb-2">Henüz Analiz Verisi Yok</h3>
        <p className="text-gray-600 mb-4">
          4 motor analizini yapabilmek için önce test sonuçları girmelisiniz.
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

  const { bs_model, difficulty_engine, time_analyzer, priority_engine } = analysisData;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-2xl p-6 shadow-xl">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold mb-2">🚀 4 Motor Analiz Sistemi</h2>
            <p className="text-sm opacity-90">
              {analysisData.analyzed_topics} konu analiz edildi
            </p>
          </div>
          <button
            onClick={runAnalysis}
            className="bg-white text-purple-600 px-4 py-2 rounded-lg font-semibold hover:bg-purple-50"
          >
            🔄 Yenile
          </button>
        </div>
      </div>

      {/* Motor Seçimi */}
      <div className="bg-white rounded-2xl p-4 shadow-lg">
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setSelectedMotor('all')}
            className={`px-4 py-2 rounded-lg font-semibold transition ${
              selectedMotor === 'all'
                ? 'bg-purple-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            🌟 Tümü
          </button>
          <button
            onClick={() => setSelectedMotor('bs')}
            className={`px-4 py-2 rounded-lg font-semibold transition ${
              selectedMotor === 'bs'
                ? 'bg-purple-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            ⏰ Akıllı Tekrar ({bs_model.urgent_topics.length})
          </button>
          <button
            onClick={() => setSelectedMotor('difficulty')}
            className={`px-4 py-2 rounded-lg font-semibold transition ${
              selectedMotor === 'difficulty'
                ? 'bg-purple-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            😰 Zorluk ({difficulty_engine.struggling_topics.length})
          </button>
          <button
            onClick={() => setSelectedMotor('time')}
            className={`px-4 py-2 rounded-lg font-semibold transition ${
              selectedMotor === 'time'
                ? 'bg-purple-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            ⏱️ Hız ({time_analyzer.slow_topics.length})
          </button>
          <button
            onClick={() => setSelectedMotor('priority')}
            className={`px-4 py-2 rounded-lg font-semibold transition ${
              selectedMotor === 'priority'
                ? 'bg-purple-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            🎯 Öncelik ({priority_engine.this_week_topics.length})
          </button>
        </div>
      </div>

      {/* BS-Model */}
      {(selectedMotor === 'all' || selectedMotor === 'bs') && (
        <div className="bg-white rounded-2xl p-6 shadow-lg">
          <h3 className="text-xl font-bold text-gray-800 mb-2">⏰ {bs_model.name}</h3>
          <p className="text-sm text-gray-600 mb-4">{bs_model.description}</p>
          {bs_model.urgent_topics.length > 0 ? (
            <div className="space-y-3">
              {bs_model.urgent_topics.map((topic, index) => (
                <div key={index} className="border-2 border-orange-200 rounded-lg p-4 hover:bg-orange-50 transition">
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex-1">
                      <div className="font-bold text-gray-800">{topic.topic_name}</div>
                      <div className="text-sm text-gray-600">{topic.subject_name}</div>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-xs font-bold ${getUrgencyColor(topic.next_review_urgency)}`}>
                      {topic.next_review_urgency}
                    </span>
                  </div>
                  <div className="text-sm text-gray-700 mb-2">{topic.recommendation}</div>
                  <div className="flex gap-4 text-xs text-gray-600">
                    <span>Hatırlama: %{topic.remembering_rate}</span>
                    <span>Son test: {topic.days_since_last_test} gün önce</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              Acil tekrar gereken konu yok 🎉
            </div>
          )}
        </div>
      )}

      {/* Difficulty Engine */}
      {(selectedMotor === 'all' || selectedMotor === 'difficulty') && (
        <div className="bg-white rounded-2xl p-6 shadow-lg">
          <h3 className="text-xl font-bold text-gray-800 mb-2">😰 {difficulty_engine.name}</h3>
          <p className="text-sm text-gray-600 mb-4">{difficulty_engine.description}</p>
          {difficulty_engine.struggling_topics.length > 0 ? (
            <div className="space-y-3">
              {difficulty_engine.struggling_topics.map((topic, index) => (
                <div key={index} className="border-2 border-red-200 rounded-lg p-4 hover:bg-red-50 transition">
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex-1">
                      <div className="font-bold text-gray-800">{topic.topic_name}</div>
                      <div className="text-sm text-gray-600">{topic.subject_name}</div>
                    </div>
                    <span className="px-3 py-1 rounded-full text-xs font-bold bg-red-500 text-white">
                      Zorluk: {topic.difficulty_score}
                    </span>
                  </div>
                  <div className="text-sm text-gray-700 mb-2">{topic.recommendation}</div>
                  <div className="flex gap-4 text-xs text-gray-600">
                    <span>Ortalama Başarı: %{topic.average_success}</span>
                    <span>Test Sayısı: {topic.total_tests}</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              Zorlanılan konu yok 🎉
            </div>
          )}
        </div>
      )}

      {/* Time Analyzer */}
      {(selectedMotor === 'all' || selectedMotor === 'time') && (
        <div className="bg-white rounded-2xl p-6 shadow-lg">
          <h3 className="text-xl font-bold text-gray-800 mb-2">⏱️ {time_analyzer.name}</h3>
          <p className="text-sm text-gray-600 mb-4">{time_analyzer.description}</p>
          {time_analyzer.slow_topics.length > 0 ? (
            <div className="space-y-3">
              {time_analyzer.slow_topics.map((topic, index) => (
                <div key={index} className="border-2 border-yellow-200 rounded-lg p-4 hover:bg-yellow-50 transition">
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex-1">
                      <div className="font-bold text-gray-800">{topic.topic_name}</div>
                      <div className="text-sm text-gray-600">{topic.subject_name}</div>
                    </div>
                    <span className="px-3 py-1 rounded-full text-xs font-bold bg-yellow-500 text-white">
                      {topic.average_interval_days} gün
                    </span>
                  </div>
                  <div className="text-sm text-gray-700">{topic.recommendation}</div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              Hız sorunu yok 🎉
            </div>
          )}
        </div>
      )}

      {/* Priority Engine */}
      {(selectedMotor === 'all' || selectedMotor === 'priority') && (
        <div className="bg-white rounded-2xl p-6 shadow-lg">
          <h3 className="text-xl font-bold text-gray-800 mb-2">🎯 {priority_engine.name}</h3>
          <p className="text-sm text-gray-600 mb-4">{priority_engine.description}</p>
          {priority_engine.this_week_topics.length > 0 ? (
            <div className="space-y-3">
              {priority_engine.this_week_topics.map((topic, index) => (
                <div key={index} className="border-2 border-purple-200 rounded-lg p-4 hover:bg-purple-50 transition">
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex-1">
                      <div className="font-bold text-gray-800">{topic.topic_name}</div>
                      <div className="text-sm text-gray-600">{topic.subject_name}</div>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-xs font-bold ${getPriorityColor(topic.priority_level)}`}>
                      {getPriorityText(topic.priority_level)}
                    </span>
                  </div>
                  <div className="text-sm text-gray-700 mb-2">{topic.recommendation}</div>
                  <div className="flex gap-4 text-xs text-gray-600">
                    <span>Öncelik Skoru: {topic.priority_score}</span>
                    <span>Hatırlama: %{topic.remembering_rate}</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              Bu hafta öncelikli konu yok 🎉
            </div>
          )}
        </div>
      )}
    </div>
  );
}