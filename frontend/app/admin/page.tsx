'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';

interface AdminStats {
  total_students: number;
  total_tests: number;
  total_topics: number;
  total_subjects: number;
  recent_tests: number;
}

interface Student {
  id: string;
  name: string;
  class: string;
  email: string;
  test_count: number;
  last_test: string | null;
  created_at: string;
}

interface Topic {
  id: string;
  code: string;
  name_tr: string;
  name_en: string;
  subject_name: string;
  subject_icon: string;
  difficulty_level: number;
  exam_weight: number;
  test_count: number;
  is_active: boolean;
  created_at: string;
}

interface Subject {
  id: string;
  code: string;
  name_tr: string;
  icon: string;
  color: string;
  total_questions: number;
  topic_count: number;
  is_active: boolean;
}

export default function AdminPanel() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [students, setStudents] = useState<Student[]>([]);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [error, setError] = useState('');
  
  const [activeTab, setActiveTab] = useState<'overview' | 'students' | 'topics' | 'subjects'>('overview');
  
  // Yeni konu ekleme modal
  const [showAddTopic, setShowAddTopic] = useState(false);
  const [newTopic, setNewTopic] = useState({
    subject_id: '',
    name_tr: '',
    difficulty_level: 3,
    exam_weight: 0
  });

  useEffect(() => {
    const fetchAdminData = async () => {
      try {
        const userStr = localStorage.getItem('user');
        if (!userStr) {
          router.push('/');
          return;
        }

        const accessToken = localStorage.getItem('access_token');

        // Stats
        const statsRes = await fetch('http://localhost:8000/api/admin/stats', {
          headers: { 'Authorization': `Bearer ${accessToken}` }
        });
        if (statsRes.ok) {
          const statsData = await statsRes.json();
          setStats(statsData);
        }

        // Students
        const studentsRes = await fetch('http://localhost:8000/api/admin/students', {
          headers: { 'Authorization': `Bearer ${accessToken}` }
        });
        if (studentsRes.ok) {
          const studentsData = await studentsRes.json();
          setStudents(studentsData.students);
        }

        // Topics
        const topicsRes = await fetch('http://localhost:8000/api/admin/topics', {
          headers: { 'Authorization': `Bearer ${accessToken}` }
        });
        if (topicsRes.ok) {
          const topicsData = await topicsRes.json();
          setTopics(topicsData.topics);
        }

        // Subjects
        const subjectsRes = await fetch('http://localhost:8000/api/admin/subjects', {
          headers: { 'Authorization': `Bearer ${accessToken}` }
        });
        if (subjectsRes.ok) {
          const subjectsData = await subjectsRes.json();
          setSubjects(subjectsData.subjects);
        }

      } catch (err: any) {
        console.error('Admin data hatası:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchAdminData();
  }, [router]);

  const handleAddTopic = async () => {
    try {
      const accessToken = localStorage.getItem('access_token');
      
      const response = await fetch('http://localhost:8000/api/admin/topics', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify(newTopic)
      });

      if (response.ok) {
        // Başarılı - sayfayı yenile
        window.location.reload();
      } else {
        alert('Konu eklenemedi!');
      }
    } catch (err) {
      console.error('Add topic hatası:', err);
      alert('Bir hata oluştu!');
    }
  };

  const handleDeleteTopic = async (topicId: string) => {
    if (!confirm('Bu konuyu deaktif etmek istediğinizden emin misiniz?')) return;

    try {
      const accessToken = localStorage.getItem('access_token');
      
      const response = await fetch(`http://localhost:8000/api/admin/topics/${topicId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${accessToken}` }
      });

      if (response.ok) {
        window.location.reload();
      } else {
        alert('Konu silinemedi!');
      }
    } catch (err) {
      console.error('Delete topic hatası:', err);
    }
  };

  const formatDate = (dateStr: string) => {
    if (!dateStr) return '-';
    const date = new Date(dateStr);
    return date.toLocaleDateString('tr-TR', { 
      day: '2-digit', 
      month: '2-digit', 
      year: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-800 mx-auto mb-4"></div>
          <p className="text-gray-600">Admin panel yükleniyor...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error}</p>
          <button
            onClick={() => router.push('/dashboard')}
            className="px-6 py-3 bg-gray-800 text-white rounded-lg hover:bg-gray-900"
          >
            Dashboard'a Dön
          </button>
        </div>
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
              <h1 className="text-2xl font-bold">End.STP Admin</h1>
              <p className="text-sm text-gray-400">Yönetim Paneli</p>
            </div>
          </div>
          
          <button 
            onClick={() => router.push('/dashboard')}
            className="px-4 py-2 text-sm bg-gray-700 hover:bg-gray-600 rounded-lg transition"
          >
            ← Kullanıcı Paneli
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Tabs */}
        <div className="bg-white rounded-xl shadow-md mb-6">
          <div className="border-b border-gray-200">
            <div className="flex gap-2 p-2">
              <button
                onClick={() => setActiveTab('overview')}
                className={`px-6 py-3 rounded-lg font-semibold transition ${
                  activeTab === 'overview'
                    ? 'bg-gray-900 text-white'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                📊 Genel Bakış
              </button>
              <button
                onClick={() => setActiveTab('students')}
                className={`px-6 py-3 rounded-lg font-semibold transition ${
                  activeTab === 'students'
                    ? 'bg-gray-900 text-white'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                👥 Öğrenciler ({students.length})
              </button>
              <button
                onClick={() => setActiveTab('topics')}
                className={`px-6 py-3 rounded-lg font-semibold transition ${
                  activeTab === 'topics'
                    ? 'bg-gray-900 text-white'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                📖 Konular ({topics.length})
              </button>
              <button
                onClick={() => setActiveTab('subjects')}
                className={`px-6 py-3 rounded-lg font-semibold transition ${
                  activeTab === 'subjects'
                    ? 'bg-gray-900 text-white'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                📚 Dersler ({subjects.length})
              </button>
            </div>
          </div>
        </div>

        {/* Overview Tab */}
        {activeTab === 'overview' && stats && (
          <div>
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Genel İstatistikler</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-5 gap-6 mb-8">
              <div className="bg-white p-6 rounded-xl shadow-md border-l-4 border-blue-500">
                <p className="text-gray-600 text-sm mb-1">Toplam Öğrenci</p>
                <p className="text-4xl font-bold text-gray-900">{stats.total_students}</p>
              </div>

              <div className="bg-white p-6 rounded-xl shadow-md border-l-4 border-green-500">
                <p className="text-gray-600 text-sm mb-1">Toplam Test</p>
                <p className="text-4xl font-bold text-gray-900">{stats.total_tests}</p>
              </div>

              <div className="bg-white p-6 rounded-xl shadow-md border-l-4 border-purple-500">
                <p className="text-gray-600 text-sm mb-1">Aktif Konu</p>
                <p className="text-4xl font-bold text-gray-900">{stats.total_topics}</p>
              </div>

              <div className="bg-white p-6 rounded-xl shadow-md border-l-4 border-orange-500">
                <p className="text-gray-600 text-sm mb-1">Aktif Ders</p>
                <p className="text-4xl font-bold text-gray-900">{stats.total_subjects}</p>
              </div>

              <div className="bg-white p-6 rounded-xl shadow-md border-l-4 border-red-500">
                <p className="text-gray-600 text-sm mb-1">Son 7 Gün Test</p>
                <p className="text-4xl font-bold text-gray-900">{stats.recent_tests}</p>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-md p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-4">Hızlı İşlemler</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <button
                  onClick={() => setActiveTab('topics')}
                  className="p-6 border-2 border-gray-200 rounded-lg hover:border-gray-900 hover:shadow-lg transition"
                >
                  <div className="text-4xl mb-2">➕</div>
                  <p className="font-semibold text-gray-800">Yeni Konu Ekle</p>
                </button>

                <button
                  onClick={() => setActiveTab('students')}
                  className="p-6 border-2 border-gray-200 rounded-lg hover:border-gray-900 hover:shadow-lg transition"
                >
                  <div className="text-4xl mb-2">👥</div>
                  <p className="font-semibold text-gray-800">Öğrencileri Görüntüle</p>
                </button>

                <button
                  onClick={() => setActiveTab('subjects')}
                  className="p-6 border-2 border-gray-200 rounded-lg hover:border-gray-900 hover:shadow-lg transition"
                >
                  <div className="text-4xl mb-2">📚</div>
                  <p className="font-semibold text-gray-800">Dersleri Görüntüle</p>
                </button>
               <button
                onClick={() => router.push('/admin/exams')}
                className="p-6 border-2 border-gray-200 rounded-lg hover:border-gray-900 hover:shadow-lg transition"
            >
                <div className="text-4xl mb-2">📊</div>
                <p className="font-semibold text-gray-800">Sınav Verilerini Güncelle</p>
                </button>
                <button
                onClick={() => router.push('/admin/osym')}
                className="p-6 border-2 border-gray-200 rounded-lg hover:border-gray-900 hover:shadow-lg transition"
                >
                <div className="text-4xl mb-2">🔗</div>
                <p className="font-semibold text-gray-800">ÖSYM Konu Eşleştirme</p>
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Students Tab */}
        {activeTab === 'students' && (
          <div>
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-800">Öğrenci Listesi</h2>
              <p className="text-gray-600">Toplam: {students.length} öğrenci</p>
            </div>

            <div className="bg-white rounded-xl shadow-md overflow-hidden">
              <table className="w-full">
                <thead className="bg-gray-900 text-white">
                  <tr>
                    <th className="px-6 py-4 text-left">Öğrenci Adı</th>
                    <th className="px-6 py-4 text-left">Email</th>
                    <th className="px-6 py-4 text-left">Sınıf</th>
                    <th className="px-6 py-4 text-center">Test Sayısı</th>
                    <th className="px-6 py-4 text-left">Son Test</th>
                    <th className="px-6 py-4 text-left">Kayıt Tarihi</th>
                  </tr>
                </thead>
                <tbody>
                  {students.map((student, index) => (
                    <tr key={student.id} className={index % 2 === 0 ? 'bg-gray-50' : 'bg-white'}>
                      <td className="px-6 py-4 font-semibold text-gray-800">{student.name}</td>
                      <td className="px-6 py-4 text-gray-600">{student.email}</td>
                      <td className="px-6 py-4 text-gray-600">{student.class}</td>
                      <td className="px-6 py-4 text-center">
                        <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full font-semibold">
                          {student.test_count}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-gray-600">{formatDate(student.last_test || '')}</td>
                      <td className="px-6 py-4 text-gray-600">{formatDate(student.created_at)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Topics Tab */}
        {activeTab === 'topics' && (
          <div>
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-800">Konu Yönetimi</h2>
              <button
                onClick={() => setShowAddTopic(true)}
                className="px-6 py-3 bg-gray-900 text-white rounded-lg hover:bg-gray-800 transition font-semibold"
              >
                + Yeni Konu Ekle
              </button>
            </div>

            <div className="bg-white rounded-xl shadow-md overflow-hidden">
              <table className="w-full">
                <thead className="bg-gray-900 text-white">
                  <tr>
                    <th className="px-6 py-4 text-left">Konu Adı</th>
                    <th className="px-6 py-4 text-left">Ders</th>
                    <th className="px-6 py-4 text-center">Zorluk</th>
                    <th className="px-6 py-4 text-center">Test Sayısı</th>
                    <th className="px-6 py-4 text-center">Durum</th>
                    <th className="px-6 py-4 text-center">İşlemler</th>
                  </tr>
                </thead>
                <tbody>
                  {topics.map((topic, index) => (
                    <tr key={topic.id} className={index % 2 === 0 ? 'bg-gray-50' : 'bg-white'}>
                      <td className="px-6 py-4 font-semibold text-gray-800">{topic.name_tr}</td>
                      <td className="px-6 py-4 text-gray-600">
                        {topic.subject_icon} {topic.subject_name}
                      </td>
                      <td className="px-6 py-4 text-center">
                        {'⭐'.repeat(topic.difficulty_level)}
                      </td>
                      <td className="px-6 py-4 text-center">
                        <span className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full font-semibold">
                          {topic.test_count}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-center">
                        <span className={`px-3 py-1 rounded-full font-semibold ${
                          topic.is_active 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {topic.is_active ? 'Aktif' : 'Pasif'}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-center">
                        <button
                          onClick={() => handleDeleteTopic(topic.id)}
                          className="text-red-600 hover:text-red-800 font-semibold"
                        >
                          🗑️ Sil
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Subjects Tab */}
        {activeTab === 'subjects' && (
          <div>
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Ders Listesi</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {subjects.map((subject) => (
                <div key={subject.id} className="bg-white rounded-xl shadow-md p-6 border-l-4" style={{borderColor: subject.color}}>
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <span className="text-4xl">{subject.icon}</span>
                      <div>
                        <h3 className="text-xl font-bold text-gray-800">{subject.name_tr}</h3>
                        <p className="text-sm text-gray-500">{subject.code}</p>
                      </div>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                      subject.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                    }`}>
                      {subject.is_active ? 'Aktif' : 'Pasif'}
                    </span>
                  </div>

                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <p className="text-gray-600">Konu Sayısı</p>
                      <p className="font-bold text-gray-900">{subject.topic_count}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Soru Sayısı</p>
                      <p className="font-bold text-gray-900">{subject.total_questions || 12}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>

      {/* Add Topic Modal */}
      {showAddTopic && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl shadow-2xl p-8 max-w-md w-full mx-4">
            <h3 className="text-2xl font-bold text-gray-800 mb-6">Yeni Konu Ekle</h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Ders</label>
                <select
                  value={newTopic.subject_id}
                  onChange={(e) => setNewTopic({...newTopic, subject_id: e.target.value})}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 outline-none text-gray-900"
                  required
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
                <label className="block text-sm font-medium text-gray-700 mb-2">Konu Adı (Türkçe)</label>
                <input
                  type="text"
                  value={newTopic.name_tr}
                  onChange={(e) => setNewTopic({...newTopic, name_tr: e.target.value})}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 outline-none text-gray-900"
                  placeholder="Örn: Limit"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Zorluk Seviyesi: {newTopic.difficulty_level} ⭐
                </label>
                <input
                  type="range"
                  min="1"
                  max="5"
                  value={newTopic.difficulty_level}
                  onChange={(e) => setNewTopic({...newTopic, difficulty_level: parseInt(e.target.value)})}
                  className="w-full"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Sınav Ağırlığı (%)</label>
                <input
                  type="number"
                  step="0.1"
                  value={newTopic.exam_weight}
                  onChange={(e) => setNewTopic({...newTopic, exam_weight: parseFloat(e.target.value)})}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-900 outline-none text-gray-900"
                  placeholder="8.5"
                />
              </div>
            </div>

            <div className="flex gap-4 mt-6">
              <button
                onClick={() => setShowAddTopic(false)}
                className="flex-1 px-6 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition font-semibold"
              >
                İptal
              </button>
              <button
                onClick={handleAddTopic}
                className="flex-1 px-6 py-3 bg-gray-900 text-white rounded-lg hover:bg-gray-800 transition font-semibold"
                disabled={!newTopic.subject_id || !newTopic.name_tr}
              >
                Ekle
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}