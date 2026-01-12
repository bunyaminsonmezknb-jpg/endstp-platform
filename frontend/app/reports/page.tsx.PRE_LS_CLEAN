'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface OverallStats {
  total_tests: number;
  avg_net: number;
  total_correct: number;
  total_wrong: number;
  total_empty: number;
  success_rate: number;
}

interface SubjectPerformance {
  subject: string;
  test_count: number;
  avg_net: number;
  total_correct: number;
  total_wrong: number;
  total_empty: number;
  success_rate: number;
}

interface TopicPerformance {
  subject: string;
  topic: string;
  test_count: number;
  avg_net: number;
  trend: number;
  last_net: number;
}

interface RecentTest {
  id: string;
  subject: string;
  topic: string;
  net: number;
  correct: number;
  wrong: number;
  empty: number;
  success_rate: number;
  date: string;
}

interface ReportsData {
  overall_stats: OverallStats;
  subject_performance: SubjectPerformance[];
  topic_performance: TopicPerformance[];
  strong_topics: TopicPerformance[];
  weak_topics: TopicPerformance[];
  recent_tests: RecentTest[];
}

export default function ReportsPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<ReportsData | null>(null);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState<'subjects' | 'topics' | 'recent'>('subjects');

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      const userStr = localStorage.getItem('user');
      if (!userStr) {
        router.push('/login');
        return;
      }

      const user = JSON.parse(userStr);
      const accessToken = localStorage.getItem('access_token');

      // Reports API'den veri çek
      const response = await fetch(`http://localhost:8000/api/v1/students/${user.id}/reports`, {
        headers: { 'Authorization': `Bearer ${accessToken}` }
      });

      if (response.status === 404) {
        // Veri yok
        setError('');
        setData({
          overall_stats: {
            total_tests: 0,
            avg_net: 0,
            total_correct: 0,
            total_wrong: 0,
            total_empty: 0,
            success_rate: 0
          },
          subject_performance: [],
          topic_performance: [],
          strong_topics: [],
          weak_topics: [],
          recent_tests: []
        });
        return;
      }

      if (!response.ok) throw new Error('Raporlar yüklenemedi');

      const reportsData = await response.json();
      setData(reportsData);

    } catch (err: any) {
      console.error('Reports hatası:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('tr-TR', { 
      day: '2-digit', 
      month: '2-digit', 
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getScoreColor = (score: number) => {
    if (score >= 9) return 'text-green-600';
    if (score >= 7) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBg = (score: number) => {
    if (score >= 9) return 'bg-green-50 border-green-300';
    if (score >= 7) return 'bg-yellow-50 border-yellow-300';
    return 'bg-red-50 border-red-300';
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    document.cookie = 'access_token=; path=/; max-age=0';
    router.push('/login');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-purple-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Raporlar yükleniyor...</p>
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-purple-50">
        <div className="text-center bg-white p-8 rounded-2xl shadow-lg">
          <div className="text-6xl mb-4">❌</div>
          <p className="text-red-600 mb-4 font-semibold">{error || 'Veri yüklenemedi'}</p>
          <button
            onClick={() => router.push('/student/dashboard')}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            Dashboard'a Dön
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => router.push('/student/dashboard')}>
            <span className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              End.STP
            </span>
          </div>
          
          <div className="flex items-center gap-4">
            <button 
              onClick={() => router.push('/student/dashboard')}
              className="px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-lg transition"
            >
              ← Dashboard
            </button>
            <button 
              onClick={handleLogout}
              className="px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded-lg transition"
            >
              Çıkış
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-8">📊 Detaylı Performans Raporları</h1>

        {/* Veri yok durumu */}
        {data.overall_stats.total_tests === 0 ? (
          <div className="bg-white rounded-2xl shadow-lg p-12 text-center">
            <div className="text-8xl mb-6">📊</div>
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Henüz Test Girilmemiş</h2>
            <p className="text-gray-600 mb-8">
              Performans raporlarınızı görebilmek için önce test sonuçlarınızı girin.
            </p>
            <button
              onClick={() => router.push('/test-entry')}
              className="px-8 py-4 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg hover:scale-105 transition font-semibold"
            >
              ➕ İlk Testimi Gir
            </button>
          </div>
        ) : (
          <>
            {/* Genel İstatistikler */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white p-6 rounded-xl shadow-md border-l-4 border-blue-500">
            <p className="text-gray-600 text-sm mb-1">Toplam Test</p>
            <p className="text-4xl font-bold text-blue-600">{data.overall_stats.total_tests}</p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-md border-l-4 border-green-500">
            <p className="text-gray-600 text-sm mb-1">Ortalama Net</p>
            <p className="text-4xl font-bold text-green-600">{data.overall_stats.avg_net.toFixed(1)}</p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-md border-l-4 border-purple-500">
            <p className="text-gray-600 text-sm mb-1">Toplam Doğru</p>
            <p className="text-4xl font-bold text-purple-600">{data.overall_stats.total_correct}</p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-md border-l-4 border-orange-500">
            <p className="text-gray-600 text-sm mb-1">Başarı Oranı</p>
            <p className="text-4xl font-bold text-orange-600">{data.overall_stats.success_rate.toFixed(0)}%</p>
          </div>
        </div>

        {/* Güçlü ve Zayıf Konular */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {/* Güçlü Konular */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
              <span className="text-2xl">💪</span> Güçlü Konularınız
            </h2>
            {data.strong_topics.length > 0 ? (
              <div className="space-y-3">
                {data.strong_topics.map((topic, index) => (
                  <div key={index} className="border-2 border-green-200 bg-green-50 rounded-lg p-4 hover:shadow-md transition">
                    <div className="flex justify-between items-center">
                      <div>
                        <p className="font-semibold text-gray-800">{topic.topic}</p>
                        <p className="text-sm text-gray-600">{topic.subject}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-3xl font-bold text-green-600">{topic.avg_net.toFixed(1)}</p>
                        <p className="text-xs text-gray-500">{topic.test_count} test</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <div className="text-4xl mb-2">🎯</div>
                <p>Henüz güçlü konu belirlenemedi</p>
              </div>
            )}
          </div>

          {/* Zayıf Konular */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
              <span className="text-2xl">📚</span> Çalışmanız Gereken Konular
            </h2>
            {data.weak_topics.length > 0 ? (
              <div className="space-y-3">
                {data.weak_topics.map((topic, index) => (
                  <div key={index} className="border-2 border-red-200 bg-red-50 rounded-lg p-4 hover:shadow-md transition">
                    <div className="flex justify-between items-center">
                      <div>
                        <p className="font-semibold text-gray-800">{topic.topic}</p>
                        <p className="text-sm text-gray-600">{topic.subject}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-3xl font-bold text-red-600">{topic.avg_net.toFixed(1)}</p>
                        <p className="text-xs text-gray-500">{topic.test_count} test</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <div className="text-4xl mb-2">🎉</div>
                <p>Tüm konularınız iyi durumda!</p>
              </div>
            )}
          </div>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="border-b border-gray-200 mb-6">
            <div className="flex gap-4">
              <button
                onClick={() => setActiveTab('subjects')}
                className={`pb-3 px-4 font-semibold transition ${
                  activeTab === 'subjects'
                    ? 'border-b-2 border-blue-600 text-blue-600'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                📚 Ders Bazlı
              </button>
              <button
                onClick={() => setActiveTab('topics')}
                className={`pb-3 px-4 font-semibold transition ${
                  activeTab === 'topics'
                    ? 'border-b-2 border-blue-600 text-blue-600'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                📖 Konu Bazlı
              </button>
              <button
                onClick={() => setActiveTab('recent')}
                className={`pb-3 px-4 font-semibold transition ${
                  activeTab === 'recent'
                    ? 'border-b-2 border-blue-600 text-blue-600'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                🕐 Son Testler
              </button>
            </div>
          </div>

          {/* Ders Bazlı */}
          {activeTab === 'subjects' && (
            <div className="space-y-4">
              {data.subject_performance.map((subject, index) => (
                <div key={index} className={`border-2 rounded-xl p-5 ${getScoreBg(subject.avg_net)} hover:shadow-lg transition`}>
                  <div className="flex justify-between items-center mb-4">
                    <h3 className="text-xl font-bold text-gray-800">{subject.subject}</h3>
                    <span className={`text-4xl font-bold ${getScoreColor(subject.avg_net)}`}>
                      {subject.avg_net.toFixed(1)}
                    </span>
                  </div>
                  
                  <div className="grid grid-cols-5 gap-4 text-sm">
                    <div className="bg-white rounded-lg p-3 text-center">
                      <p className="text-gray-600 mb-1">Test Sayısı</p>
                      <p className="font-bold text-gray-800 text-lg">{subject.test_count}</p>
                    </div>
                    <div className="bg-white rounded-lg p-3 text-center">
                      <p className="text-gray-600 mb-1">Doğru</p>
                      <p className="font-bold text-green-600 text-lg">{subject.total_correct}</p>
                    </div>
                    <div className="bg-white rounded-lg p-3 text-center">
                      <p className="text-gray-600 mb-1">Yanlış</p>
                      <p className="font-bold text-red-600 text-lg">{subject.total_wrong}</p>
                    </div>
                    <div className="bg-white rounded-lg p-3 text-center">
                      <p className="text-gray-600 mb-1">Boş</p>
                      <p className="font-bold text-gray-600 text-lg">{subject.total_empty}</p>
                    </div>
                    <div className="bg-white rounded-lg p-3 text-center">
                      <p className="text-gray-600 mb-1">Başarı</p>
                      <p className="font-bold text-blue-600 text-lg">{subject.success_rate.toFixed(0)}%</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Konu Bazlı */}
          {activeTab === 'topics' && (
            <div className="space-y-3">
              {data.topic_performance.map((topic, index) => (
                <div key={index} className="border-2 border-gray-200 rounded-lg p-4 hover:shadow-md hover:border-blue-300 transition">
                  <div className="flex justify-between items-center">
                    <div>
                      <p className="font-semibold text-gray-800">{topic.topic}</p>
                      <p className="text-sm text-gray-500">{topic.subject} • {topic.test_count} test</p>
                    </div>
                    <div className="text-right">
                      <p className={`text-3xl font-bold ${getScoreColor(topic.avg_net)}`}>
                        {topic.avg_net.toFixed(1)}
                      </p>
                      {topic.trend !== 0 && (
                        <p className={`text-sm font-semibold ${topic.trend > 0 ? 'text-green-600' : 'text-red-600'}`}>
                          {topic.trend > 0 ? '↗' : '↘'} {Math.abs(topic.trend).toFixed(1)}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Son Testler */}
          {activeTab === 'recent' && (
            <div className="space-y-3">
              {data.recent_tests.map((test) => (
                <div key={test.id} className="border-2 border-gray-200 rounded-lg p-4 hover:shadow-md hover:border-blue-300 transition">
                  <div className="flex justify-between items-center mb-3">
                    <div>
                      <p className="font-semibold text-gray-800">{test.topic}</p>
                      <p className="text-sm text-gray-500">{test.subject}</p>
                    </div>
                    <p className={`text-4xl font-bold ${getScoreColor(test.net)}`}>
                      {test.net.toFixed(2)}
                    </p>
                  </div>
                  
                  <div className="flex justify-between items-center text-sm">
                    <div className="flex gap-4">
                      <span className="text-green-600 font-semibold">✅ {test.correct}</span>
                      <span className="text-red-600 font-semibold">❌ {test.wrong}</span>
                      <span className="text-gray-600 font-semibold">⭕ {test.empty}</span>
                    </div>
                    <span className="text-gray-500">{formatDate(test.date)}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
        </>
        )}
      </main>
    </div>
  );
}
