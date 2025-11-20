'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';

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

export default function Reports() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<ReportsData | null>(null);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState<'subjects' | 'topics' | 'recent'>('subjects');

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const userStr = localStorage.getItem('user');
        if (!userStr) {
          router.push('/');
          return;
        }

        const user = JSON.parse(userStr);
        const accessToken = localStorage.getItem('access_token');

        // Student ID al
        const studentResponse = await fetch(`http://localhost:8000/api/user/${user.id}/student`, {
          headers: { 'Authorization': `Bearer ${accessToken}` }
        });

        if (!studentResponse.ok) throw new Error('Öğrenci bilgisi bulunamadı');

          const studentData = await studentResponse.json();
          const studentId = studentData.id;  // ← DOĞRU

        // Reports verilerini al
        const reportsResponse = await fetch(`http://localhost:8000/api/students/${studentId}/reports`, {
          headers: { 'Authorization': `Bearer ${accessToken}` }
        });

        if (!reportsResponse.ok) throw new Error('Raporlar yüklenemedi');

        const reportsData = await reportsResponse.json();
        setData(reportsData);

      } catch (err: any) {
        console.error('Reports hatası:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchReports();
  }, [router]);

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
    if (score >= 9) return 'bg-green-50 border-green-200';
    if (score >= 7) return 'bg-yellow-50 border-yellow-200';
    return 'bg-red-50 border-red-200';
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
        <div className="text-center">
          <p className="text-red-600 mb-4">{error || 'Veri yüklenemedi'}</p>
          <button
            onClick={() => router.push('/dashboard')}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Dashboard'a Dön
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => router.push('/dashboard')}>
            <Image src="/logo.png" alt="End.STP" width={40} height={40} />
            <span className="text-2xl font-bold text-gray-800">End.STP</span>
          </div>
          
          <button 
            onClick={() => router.push('/dashboard')}
            className="px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-lg transition"
          >
            ← Dashboard
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-8">📊 Detaylı Performans Raporları</h1>

        {/* Genel İstatistikler */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white p-6 rounded-xl shadow-md">
            <p className="text-gray-600 text-sm mb-1">Toplam Test</p>
            <p className="text-3xl font-bold text-blue-600">{data.overall_stats.total_tests}</p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-md">
            <p className="text-gray-600 text-sm mb-1">Ortalama Net</p>
            <p className="text-3xl font-bold text-green-600">{data.overall_stats.avg_net}</p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-md">
            <p className="text-gray-600 text-sm mb-1">Toplam Doğru</p>
            <p className="text-3xl font-bold text-purple-600">{data.overall_stats.total_correct}</p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-md">
            <p className="text-gray-600 text-sm mb-1">Başarı Oranı</p>
            <p className="text-3xl font-bold text-orange-600">{data.overall_stats.success_rate}%</p>
          </div>
        </div>

        {/* Güçlü ve Zayıf Konular */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {/* Güçlü Konular */}
          <div className="bg-white rounded-xl shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
              💪 Güçlü Konularınız
            </h2>
            {data.strong_topics.length > 0 ? (
              <div className="space-y-3">
                {data.strong_topics.map((topic, index) => (
                  <div key={index} className="border border-green-200 bg-green-50 rounded-lg p-3">
                    <div className="flex justify-between items-center">
                      <div>
                        <p className="font-semibold text-gray-800">{topic.topic}</p>
                        <p className="text-sm text-gray-600">{topic.subject}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-2xl font-bold text-green-600">{topic.avg_net}</p>
                        <p className="text-xs text-gray-500">{topic.test_count} test</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-8">Henüz güçlü konu belirlenemedi</p>
            )}
          </div>

          {/* Zayıf Konular */}
          <div className="bg-white rounded-xl shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
              📚 Çalışmanız Gereken Konular
            </h2>
            {data.weak_topics.length > 0 ? (
              <div className="space-y-3">
                {data.weak_topics.map((topic, index) => (
                  <div key={index} className="border border-red-200 bg-red-50 rounded-lg p-3">
                    <div className="flex justify-between items-center">
                      <div>
                        <p className="font-semibold text-gray-800">{topic.topic}</p>
                        <p className="text-sm text-gray-600">{topic.subject}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-2xl font-bold text-red-600">{topic.avg_net}</p>
                        <p className="text-xs text-gray-500">{topic.test_count} test</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-8">Tüm konularınız iyi durumda! 🎉</p>
            )}
          </div>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-xl shadow-md p-6">
          <div className="border-b border-gray-200 mb-6">
            <div className="flex gap-4">
              <button
                onClick={() => setActiveTab('subjects')}
                className={`pb-3 px-2 font-semibold transition ${
                  activeTab === 'subjects'
                    ? 'border-b-2 border-blue-600 text-blue-600'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                📚 Ders Bazlı
              </button>
              <button
                onClick={() => setActiveTab('topics')}
                className={`pb-3 px-2 font-semibold transition ${
                  activeTab === 'topics'
                    ? 'border-b-2 border-blue-600 text-blue-600'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                📖 Konu Bazlı
              </button>
              <button
                onClick={() => setActiveTab('recent')}
                className={`pb-3 px-2 font-semibold transition ${
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
                <div key={index} className={`border-2 rounded-lg p-4 ${getScoreBg(subject.avg_net)}`}>
                  <div className="flex justify-between items-center mb-3">
                    <h3 className="text-xl font-bold text-gray-800">{subject.subject}</h3>
                    <span className={`text-3xl font-bold ${getScoreColor(subject.avg_net)}`}>
                      {subject.avg_net}
                    </span>
                  </div>
                  
                  <div className="grid grid-cols-5 gap-4 text-sm">
                    <div>
                      <p className="text-gray-600">Test Sayısı</p>
                      <p className="font-semibold text-gray-800">{subject.test_count}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Doğru</p>
                      <p className="font-semibold text-green-600">{subject.total_correct}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Yanlış</p>
                      <p className="font-semibold text-red-600">{subject.total_wrong}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Boş</p>
                      <p className="font-semibold text-gray-600">{subject.total_empty}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Başarı</p>
                      <p className="font-semibold text-blue-600">{subject.success_rate}%</p>
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
                <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition">
                  <div className="flex justify-between items-center">
                    <div>
                      <p className="font-semibold text-gray-800">{topic.topic}</p>
                      <p className="text-sm text-gray-500">{topic.subject} • {topic.test_count} test</p>
                    </div>
                    <div className="text-right">
                      <p className={`text-2xl font-bold ${getScoreColor(topic.avg_net)}`}>
                        {topic.avg_net}
                      </p>
                      {topic.trend !== 0 && (
                        <p className={`text-sm ${topic.trend > 0 ? 'text-green-600' : 'text-red-600'}`}>
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
                <div key={test.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition">
                  <div className="flex justify-between items-center mb-2">
                    <div>
                      <p className="font-semibold text-gray-800">{test.topic}</p>
                      <p className="text-sm text-gray-500">{test.subject}</p>
                    </div>
                    <p className={`text-3xl font-bold ${getScoreColor(test.net)}`}>
                      {test.net.toFixed(2)}
                    </p>
                  </div>
                  
                  <div className="flex justify-between items-center text-sm">
                    <div className="flex gap-4">
                      <span className="text-green-600">✅ {test.correct}</span>
                      <span className="text-red-600">❌ {test.wrong}</span>
                      <span className="text-gray-600">⭕ {test.empty}</span>
                    </div>
                    <span className="text-gray-500">{formatDate(test.date)}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}