'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';

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

export default function ExamManagement() {
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
  
  // Yeni sınav ekleme
  const [showAddExam, setShowAddExam] = useState(false);
  const [newExam, setNewExam] = useState({
    exam_system_id: '',
    year: new Date().getFullYear(),
    exam_type: 'TYT',
    total_questions: 40
  });
  
  // Konu soru sayısı ekleme
  const [showAddTopicData, setShowAddTopicData] = useState(false);
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
    const fetchData = async () => {
      try {
        const accessToken = localStorage.getItem('access_token');

        // Exam systems
        const examsRes = await fetch('http://localhost:8000/api/admin/subjects', {
          headers: { 'Authorization': `Bearer ${accessToken}` }
        });
        
        // Subjects
        const subjectsRes = await fetch('http://localhost:8000/api/admin/subjects', {
          headers: { 'Authorization': `Bearer ${accessToken}` }
        });
        if (subjectsRes.ok) {
          const data = await subjectsRes.json();
          setSubjects(data.subjects);
        }

        // Topics
        const topicsRes = await fetch('http://localhost:8000/api/admin/topics', {
          headers: { 'Authorization': `Bearer ${accessToken}` }
        });
        if (topicsRes.ok) {
          const data = await topicsRes.json();
          setTopics(data.topics);
        }

        // Exam systems (mock - gerçekte API'den gelecek)
        setExamSystems([
          { id: '550e8400-e29b-41d4-a716-446655440009', code: 'YKS', name_tr: 'YKS (TYT/AYT)' }
        ]);

      } catch (err) {
        console.error('Data fetch hatası:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

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
        `http://localhost:8000/api/admin/topics/${selectedTopic}/yearly-stats?exam_system_id=${selectedExamSystem}`,
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

      // Önce exam_history var mı kontrol et, yoksa oluştur
      // Basitleştirme için direkt topic_yearly_stats'a ekle
      
      const response = await fetch('http://localhost:8000/api/admin/topic-yearly-data', {
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
        alert('Sınav verisi eklendi!');
        setShowAddTopicData(false);
        fetchYearlyStats(); // Yenile
        
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
        alert('Hata oluştu!');
      }
    } catch (err) {
      console.error('Add topic data hatası:', err);
      alert('Bir hata oluştu!');
    }
  };

  const filteredTopics = selectedSubject 
    ? topics.filter(t => t.subject_name === subjects.find(s => s.id === selectedSubject)?.name_tr)
    : topics;

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-800 mx-auto"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <header className="bg-gray-900 text-white shadow-lg border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <Image src="/logo.png" alt="End.STP" width={40} height={40} />
            <div>
              <h1 className="text-2xl font-bold">Sınav Yönetimi</h1>
              <p className="text-sm text-gray-400">Yıllık sınav verilerini güncelleyin</p>
            </div>
          </div>
          
          <button 
            onClick={() => router.push('/admin')}
            className="px-4 py-2 text-sm bg-gray-700 hover:bg-gray-600 rounded-lg transition"
          >
            ← Admin Panel
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Filtreler */}
        <div className="bg-white rounded-xl shadow-md p-6 mb-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">📊 Konu Seçimi</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Sınav Sistemi</label>
              <select
                value={selectedExamSystem}
                onChange={(e) => setSelectedExamSystem(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 outline-none text-gray-900"
              >
                <option value="">Sınav Seçin</option>
                {examSystems.map(exam => (
                  <option key={exam.id} value={exam.id}>{exam.name_tr}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Ders</label>
              <select
                value={selectedSubject}
                onChange={(e) => {
                  setSelectedSubject(e.target.value);
                  setSelectedTopic('');
                }}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 outline-none text-gray-900"
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
              <label className="block text-sm font-medium text-gray-700 mb-2">Konu</label>
              <select
                value={selectedTopic}
                onChange={(e) => setSelectedTopic(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 outline-none text-gray-900"
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
          <div className="bg-white rounded-xl shadow-md p-6">
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
                  setShowAddTopicData(true);
                }}
                className="px-6 py-3 bg-gray-900 text-white rounded-lg hover:bg-gray-800 transition font-semibold"
              >
                + Yeni Yıl Ekle
              </button>
            </div>

            {loadingStats ? (
              <div className="text-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-800 mx-auto"></div>
              </div>
            ) : yearlyStats.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-900 text-white">
                    <tr>
                      <th className="px-6 py-4 text-left">Yıl</th>
                      <th className="px-6 py-4 text-center">Ana Konu</th>
                      <th className="px-6 py-4 text-center">Tali Konu</th>
                      <th className="px-6 py-4 text-center">Toplam</th>
                      <th className="px-6 py-4 text-left">Soru Numaraları</th>
                      <th className="px-6 py-4 text-left">Notlar</th>
                    </tr>
                  </thead>
                  <tbody>
                    {yearlyStats.map((stat, index) => (
                      <tr key={stat.year} className={index % 2 === 0 ? 'bg-gray-50' : 'bg-white'}>
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
            ) : (
              <div className="text-center py-12 text-gray-500">
                <div className="text-6xl mb-4">📊</div>
                <p className="text-lg font-semibold mb-2">Henüz veri yok</p>
                <p className="text-sm">Bu konu için yıllık sınav verisi ekleyin</p>
              </div>
            )}

            {/* Özet İstatistik */}
            {yearlyStats.length > 0 && (
              <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                <h3 className="font-semibold text-gray-800 mb-2">📈 Özet</h3>
                <div className="grid grid-cols-4 gap-4 text-sm">
                  <div>
                    <p className="text-gray-600">Toplam Yıl</p>
                    <p className="font-bold text-gray-900">{yearlyStats.length}</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Toplam Soru (Ana)</p>
                    <p className="font-bold text-blue-600">
                      {yearlyStats.reduce((sum, s) => sum + s.primary_questions, 0)}
                    </p>
                  </div>
                  <div>
                    <p className="text-gray-600">Toplam Soru (Tali)</p>
                    <p className="font-bold text-purple-600">
                      {yearlyStats.reduce((sum, s) => sum + s.secondary_questions, 0)}
                    </p>
                  </div>
                  <div>
                    <p className="text-gray-600">Ortalama (Yıllık)</p>
                    <p className="font-bold text-green-600">
                      {(yearlyStats.reduce((sum, s) => sum + s.total_questions, 0) / yearlyStats.length).toFixed(1)}
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </main>

      {/* Add Topic Data Modal */}
      {showAddTopicData && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl shadow-2xl p-8 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
            <h3 className="text-2xl font-bold text-gray-800 mb-6">
              📝 Yeni Sınav Verisi Ekle
            </h3>
            
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Yıl</label>
                  <input
                    type="number"
                    value={topicData.year}
                    onChange={(e) => setTopicData({...topicData, year: parseInt(e.target.value)})}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 outline-none text-gray-900"
                    min="2000"
                    max={new Date().getFullYear()}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Ana/Tali Konu</label>
                  <select
                    value={topicData.is_primary ? 'primary' : 'secondary'}
                    onChange={(e) => setTopicData({...topicData, is_primary: e.target.value === 'primary'})}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 outline-none text-gray-900"
                  >
                    <option value="primary">Ana Konu</option>
                    <option value="secondary">Tali Konu</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Ana Konu Soru Sayısı
                  </label>
                  <input
                    type="number"
                    value={topicData.primary_questions}
                    onChange={(e) => setTopicData({...topicData, primary_questions: parseInt(e.target.value) || 0})}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 outline-none text-gray-900"
                    min="0"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Tali Konu Soru Sayısı
                  </label>
                  <input
                    type="number"
                    value={topicData.secondary_questions}
                    onChange={(e) => setTopicData({...topicData, secondary_questions: parseInt(e.target.value) || 0})}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 outline-none text-gray-900"
                    min="0"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Soru Numaraları (virgülle ayırın)
                </label>
                <input
                  type="text"
                  value={topicData.question_numbers}
                  onChange={(e) => setTopicData({...topicData, question_numbers: e.target.value})}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 outline-none text-gray-900"
                  placeholder="Örn: 23, 35, 47, 51"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Opsiyonel: Hangi sorularda çıktı?
                </p>
              </div>

              <div className="bg-blue-50 p-4 rounded-lg">
                <p className="text-sm font-semibold text-gray-800 mb-1">Özet:</p>
                <p className="text-sm text-gray-700">
                  {topicData.year} yılında <span className="font-bold">{topicData.primary_questions + topicData.secondary_questions}</span> soru 
                  ({topicData.primary_questions} ana + {topicData.secondary_questions} tali)
                </p>
              </div>
            </div>

            <div className="flex gap-4 mt-6">
              <button
                onClick={() => setShowAddTopicData(false)}
                className="flex-1 px-6 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition font-semibold"
              >
                İptal
              </button>
              <button
                onClick={handleAddTopicData}
                className="flex-1 px-6 py-3 bg-gray-900 text-white rounded-lg hover:bg-gray-800 transition font-semibold"
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