'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface ExamSystem {
  id: string;
  code: string;
  name_tr: string;
}

interface Subject {
  id: string;
  name_tr: string;
  icon: string;
}

interface Topic {
  id: string;
  name_tr: string;
  subject_name: string;
  subject_icon: string;
}

interface YearlyStats {
  year: number;
  primary_questions: number;
  secondary_questions: number;
  total_questions: number;
  question_numbers: string[];
  notes: string;
}

export default function AdminExamsPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [examSystems, setExamSystems] = useState<ExamSystem[]>([]);
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [topics, setTopics] = useState<Topic[]>([]);
  
  // Seçimler
  const [selectedExamSystem, setSelectedExamSystem] = useState('');
  const [selectedSubject, setSelectedSubject] = useState('');
  const [selectedTopic, setSelectedTopic] = useState('');
  
  // Yıllık istatistikler
  const [yearlyStats, setYearlyStats] = useState<YearlyStats[]>([]);
  const [loadingStats, setLoadingStats] = useState(false);
  
  // Yeni sınav verisi ekleme
  const [showAddData, setShowAddData] = useState(false);
  const [topicData, setTopicData] = useState({
    topic_id: '',
    year: new Date().getFullYear(),
    exam_system_id: '',
    primary_questions: 0,
    secondary_questions: 0,
    question_numbers: '',
    is_primary: true
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const accessToken = localStorage.getItem('access_token');

      // Subjects
      const subjectsRes = await fetch('http://localhost:8000/api/v1/subjects', {
        headers: { 'Authorization': `Bearer ${accessToken}` }
      });
      if (subjectsRes.ok) {
        const data = await subjectsRes.json();
        setSubjects(data);
      }

      // Topics
      const topicsRes = await fetch('http://localhost:8000/api/v1/admin/topics', {
        headers: { 'Authorization': `Bearer ${accessToken}` }
      });
      if (topicsRes.ok) {
        const data = await topicsRes.json();
        setTopics(data.topics || []);
      }

      // Mock exam systems (gerçekte API'den gelecek)
      setExamSystems([
        { id: '1', code: 'YKS', name_tr: 'YKS (TYT/AYT)' }
      ]);

    } catch (err) {
      console.error('Data fetch hatası:', err);
    } finally {
      setLoading(false);
    }
  };

  // Konu seçildiğinde yıllık istatistikleri getir
  useEffect(() => {
    if (selectedTopic && selectedExamSystem) {
      fetchYearlyStats();
    }
  }, [selectedTopic, selectedExamSystem]);

  const fetchYearlyStats = async () => {
    setLoadingStats(true);
    try {
      const accessToken = localStorage.getItem('access_token');
      const res = await fetch(
        `http://localhost:8000/api/v1/admin/topics/${selectedTopic}/yearly-stats?exam_system_id=${selectedExamSystem}`,
        { headers: { 'Authorization': `Bearer ${accessToken}` } }
      );

      if (res.ok) {
        const data = await res.json();
        setYearlyStats(data.stats || []);
      }
    } catch (err) {
      console.error('Yearly stats hatası:', err);
    } finally {
      setLoadingStats(false);
    }
  };

  const handleAddTopicData = async () => {
    try {
      const accessToken = localStorage.getItem('access_token');
      
      const response = await fetch('http://localhost:8000/api/v1/admin/topic-yearly-data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify({
          topic_id: topicData.topic_id,
          exam_system_id: topicData.exam_system_id,
          year: topicData.year,
          primary_questions: topicData.primary_questions,
          secondary_questions: topicData.secondary_questions,
          question_numbers: topicData.question_numbers.split(',').map(n => n.trim()).filter(n => n)
        })
      });

      if (response.ok) {
        alert('✅ Sınav verisi eklendi!');
        setShowAddData(false);
        fetchYearlyStats();
        
        // Formu sıfırla
        setTopicData({
          topic_id: '',
          year: new Date().getFullYear(),
          exam_system_id: '',
          primary_questions: 0,
          secondary_questions: 0,
          question_numbers: '',
          is_primary: true
        });
      } else {
        alert('❌ Hata oluştu!');
      }
    } catch (err) {
      console.error('Add topic data hatası:', err);
      alert('Bir hata oluştu!');
    }
  };

  const filteredTopics = selectedSubject 
    ? topics.filter(t => t.subject_name === subjects.find(s => s.id === selectedSubject)?.name_tr)
    : topics;

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    document.cookie = 'access_token=; path=/; max-age=0';
    router.push('/login');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-blue-50">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">📊 Sınav Yönetimi</h1>
            <p className="text-sm text-gray-500">Yıllık sınav verilerini güncelleyin</p>
          </div>
          
          <div className="flex items-center gap-4">
            <button 
              onClick={() => router.push('/admin')}
              className="px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-lg transition"
            >
              ← Admin Panel
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
        {/* Filtreler */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">🎯 Konu Seçimi</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Sınav Sistemi</label>
              <select
                value={selectedExamSystem}
                onChange={(e) => setSelectedExamSystem(e.target.value)}
                className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Sınav Seçin</option>
                {examSystems.map(exam => (
                  <option key={exam.id} value={exam.id}>{exam.name_tr}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Ders</label>
              <select
                value={selectedSubject}
                onChange={(e) => {
                  setSelectedSubject(e.target.value);
                  setSelectedTopic('');
                }}
                className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Ders Seçin</option>
                {subjects.map(subject => (
                  <option key={subject.id} value={subject.id}>
                    {subject.icon} {subject.name_tr}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Konu</label>
              <select
                value={selectedTopic}
                onChange={(e) => setSelectedTopic(e.target.value)}
                className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                disabled={!selectedSubject}
              >
                <option value="">Konu Seçin</option>
                {filteredTopics.map(topic => (
                  <option key={topic.id} value={topic.id}>
                    {topic.name_tr}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Yıllık İstatistikler */}
        {selectedTopic && selectedExamSystem && (
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold text-gray-800">
                📅 Yıllık Soru Dağılımı
              </h2>
              <button
                onClick={() => {
                  setTopicData({
                    ...topicData,
                    topic_id: selectedTopic,
                    exam_system_id: selectedExamSystem
                  });
                  setShowAddData(true);
                }}
                className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg hover:scale-105 transition font-semibold shadow-lg"
              >
                ➕ Yeni Yıl Ekle
              </button>
            </div>

            {loadingStats ? (
              <div className="text-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
              </div>
            ) : yearlyStats.length > 0 ? (
              <>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="bg-gradient-to-r from-purple-600 to-blue-600 text-white">
                      <tr>
                        <th className="px-6 py-4 text-left font-semibold">Yıl</th>
                        <th className="px-6 py-4 text-center font-semibold">Ana Konu</th>
                        <th className="px-6 py-4 text-center font-semibold">Tali Konu</th>
                        <th className="px-6 py-4 text-center font-semibold">Toplam</th>
                        <th className="px-6 py-4 text-left font-semibold">Soru Numaraları</th>
                        <th className="px-6 py-4 text-left font-semibold">Notlar</th>
                      </tr>
                    </thead>
                    <tbody>
                      {yearlyStats.map((stat, index) => (
                        <tr key={stat.year} className={`border-b ${index % 2 === 0 ? 'bg-gray-50' : 'bg-white'} hover:bg-blue-50 transition`}>
                          <td className="px-6 py-4 font-bold text-gray-900">{stat.year}</td>
                          <td className="px-6 py-4 text-center">
                            <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full font-semibold">
                              {stat.primary_questions}
                            </span>
                          </td>
                          <td className="px-6 py-4 text-center">
                            <span className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full font-semibold">
                              {stat.secondary_questions}
                            </span>
                          </td>
                          <td className="px-6 py-4 text-center">
                            <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full font-semibold">
                              {stat.total_questions}
                            </span>
                          </td>
                          <td className="px-6 py-4 text-gray-600">
                            {stat.question_numbers?.join(', ') || '-'}
                          </td>
                          <td className="px-6 py-4 text-gray-600 text-sm">
                            {stat.notes || '-'}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                {/* Özet */}
                <div className="mt-6 p-6 bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl">
                  <h3 className="font-semibold text-gray-800 mb-3">📈 Özet İstatistikler</h3>
                  <div className="grid grid-cols-4 gap-4">
                    <div className="bg-white rounded-lg p-4">
                      <p className="text-gray-600 text-sm mb-1">Toplam Yıl</p>
                      <p className="font-bold text-gray-900 text-2xl">{yearlyStats.length}</p>
                    </div>
                    <div className="bg-white rounded-lg p-4">
                      <p className="text-gray-600 text-sm mb-1">Toplam Soru (Ana)</p>
                      <p className="font-bold text-blue-600 text-2xl">
                        {yearlyStats.reduce((sum, s) => sum + s.primary_questions, 0)}
                      </p>
                    </div>
                    <div className="bg-white rounded-lg p-4">
                      <p className="text-gray-600 text-sm mb-1">Toplam Soru (Tali)</p>
                      <p className="font-bold text-purple-600 text-2xl">
                        {yearlyStats.reduce((sum, s) => sum + s.secondary_questions, 0)}
                      </p>
                    </div>
                    <div className="bg-white rounded-lg p-4">
                      <p className="text-gray-600 text-sm mb-1">Ortalama (Yıllık)</p>
                      <p className="font-bold text-green-600 text-2xl">
                        {(yearlyStats.reduce((sum, s) => sum + s.total_questions, 0) / yearlyStats.length).toFixed(1)}
                      </p>
                    </div>
                  </div>
                </div>
              </>
            ) : (
              <div className="text-center py-12 text-gray-500">
                <div className="text-8xl mb-4">📊</div>
                <p className="text-xl font-semibold mb-2">Henüz veri yok</p>
                <p className="text-sm">Bu konu için yıllık sınav verisi ekleyin</p>
              </div>
            )}
          </div>
        )}
      </main>

      {/* Add Data Modal */}
      {showAddData && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <h3 className="text-2xl font-bold text-gray-800 mb-6">
              📝 Yeni Sınav Verisi Ekle
            </h3>
            
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Yıl</label>
                  <input
                    type="number"
                    value={topicData.year}
                    onChange={(e) => setTopicData({...topicData, year: parseInt(e.target.value)})}
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    min="2000"
                    max={new Date().getFullYear()}
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Ana/Tali Konu</label>
                  <select
                    value={topicData.is_primary ? 'primary' : 'secondary'}
                    onChange={(e) => setTopicData({...topicData, is_primary: e.target.value === 'primary'})}
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="primary">Ana Konu</option>
                    <option value="secondary">Tali Konu</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Ana Konu Soru Sayısı
                  </label>
                  <input
                    type="number"
                    value={topicData.primary_questions}
                    onChange={(e) => setTopicData({...topicData, primary_questions: parseInt(e.target.value) || 0})}
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    min="0"
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Tali Konu Soru Sayısı
                  </label>
                  <input
                    type="number"
                    value={topicData.secondary_questions}
                    onChange={(e) => setTopicData({...topicData, secondary_questions: parseInt(e.target.value) || 0})}
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    min="0"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Soru Numaraları (virgülle ayırın)
                </label>
                <input
                  type="text"
                  value={topicData.question_numbers}
                  onChange={(e) => setTopicData({...topicData, question_numbers: e.target.value})}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="Örn: 23, 35, 47, 51"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Opsiyonel: Hangi sorularda çıktı?
                </p>
              </div>

              <div className="bg-blue-50 p-4 rounded-xl">
                <p className="text-sm font-semibold text-gray-800 mb-1">📊 Özet:</p>
                <p className="text-sm text-gray-700">
                  {topicData.year} yılında <span className="font-bold">{topicData.primary_questions + topicData.secondary_questions}</span> soru 
                  ({topicData.primary_questions} ana + {topicData.secondary_questions} tali)
                </p>
              </div>
            </div>

            <div className="flex gap-4 mt-6">
              <button
                onClick={() => setShowAddData(false)}
                className="flex-1 px-6 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 font-semibold"
              >
                İptal
              </button>
              <button
                onClick={handleAddTopicData}
                className="flex-1 px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg hover:scale-105 transition font-semibold"
                disabled={!topicData.topic_id || !topicData.exam_system_id}
              >
                Kaydet
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
