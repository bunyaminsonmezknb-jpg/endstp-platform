'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';

interface Subject {
  id: string;
  code: string;
  name_tr: string;
  icon: string;
  color: string;
}

interface Topic {
  id: string;
  code: string;
  name_tr: string;
  difficulty_level: number;
  exam_weight: number;
}

export default function TestEntry() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');

  // Form verileri
  const [testDateTime, setTestDateTime] = useState('');
  const [subjectId, setSubjectId] = useState('');
  const [topicId, setTopicId] = useState('');
  const [correctCount, setCorrectCount] = useState('');
  const [wrongCount, setWrongCount] = useState('');
  const [emptyCount, setEmptyCount] = useState('');
  const [net, setNet] = useState(0);

  // Dinamik veriler
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [loadingSubjects, setLoadingSubjects] = useState(true);
  const [loadingTopics, setLoadingTopics] = useState(false);

  // Max datetime (şu an)
  const getTurkeyDateTime = () => {
    const now = new Date();
    return now.toISOString().slice(0, 16);
  };

  // Dersleri yükle
  useEffect(() => {
    const fetchSubjects = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/subjects');
        const data = await response.json();
        setSubjects(data.subjects);
      } catch (err) {
        console.error('Dersler yüklenemedi:', err);
      } finally {
        setLoadingSubjects(false);
      }
    };

    fetchSubjects();
  }, []);

  // Ders değiştiğinde konuları yükle
  useEffect(() => {
    if (!subjectId) {
      setTopics([]);
      return;
    }

    const fetchTopics = async () => {
      setLoadingTopics(true);
      try {
        const response = await fetch(`http://localhost:8000/api/subjects/${subjectId}/topics`);
        const data = await response.json();
        setTopics(data.topics);
      } catch (err) {
        console.error('Konular yüklenemedi:', err);
      } finally {
        setLoadingTopics(false);
      }
    };

    fetchTopics();
  }, [subjectId]);

  // Net hesaplama
  useEffect(() => {
    const correct = parseFloat(correctCount) || 0;
    const wrong = parseFloat(wrongCount) || 0;
    const calculated = correct - (wrong / 4);
    setNet(Math.max(0, calculated));
  }, [correctCount, wrongCount]);

  // Form gönderme
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Gelecek tarih kontrolü
      const selectedDateTime = new Date(testDateTime);
      const now = new Date();
      
      if (selectedDateTime > now) {
        throw new Error('Gelecek tarih seçilemez! Test zaten çözülmüş olmalı.');
      }

      const userStr = localStorage.getItem('user');
      if (!userStr) {
        throw new Error('Lütfen giriş yapın');
      }

      const user = JSON.parse(userStr);
      const accessToken = localStorage.getItem('access_token');

      // Seçilen ders ve konu bilgilerini bul
      const selectedSubject = subjects.find(s => s.id === subjectId);
      const selectedTopic = topics.find(t => t.id === topicId);

      const testDateTimeISO = testDateTime + ':00';

      // Backend API'ye gönder
      const response = await fetch('http://localhost:8000/api/test-results', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify({
          user_id: user.id,
          test_datetime: testDateTimeISO,
          subject: selectedSubject?.name_tr || '',
          topic: selectedTopic?.name_tr || '',
          correct_count: parseInt(correctCount),
          wrong_count: parseInt(wrongCount),
          empty_count: parseInt(emptyCount),
          net: parseFloat(net.toFixed(2)),
          success_rate: parseFloat(((parseInt(correctCount) / 12) * 100).toFixed(2))
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Test sonucu kaydedilemedi');
      }

      setSuccess(true);
      
      setTimeout(() => {
        router.push('/dashboard');
      }, 2000);

    } catch (err: any) {
      setError(err.message || 'Bir hata oluştu');
      console.error('Hata detayı:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    router.push('/');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => router.push('/dashboard')}>
            <Image src="/logo.png" alt="End.STP" width={40} height={40} />
            <span className="text-2xl font-bold text-gray-800">End.STP</span>
          </div>
          
          <div className="flex items-center gap-4">
            <button 
              onClick={() => router.push('/dashboard')}
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

      <main className="max-w-2xl mx-auto px-4 py-8">
        <div className="bg-white rounded-xl shadow-md p-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">📝 Yeni Test Sonucu Ekle</h1>
          <p className="text-gray-600 mb-6">Çözdüğünüz test sonucunu girin</p>

          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
              {error}
            </div>
          )}

          {success && (
            <div className="mb-4 p-3 bg-green-50 border border-green-200 text-green-700 rounded-lg text-sm">
              Test sonucu kaydedildi! Dashboard'a yönlendiriliyorsunuz...
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Tarih ve Saat */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                📅 Test Tarihi ve Saati
              </label>
              <input
                type="datetime-local"
                value={testDateTime}
                onChange={(e) => setTestDateTime(e.target.value)}
                max={getTurkeyDateTime()}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none text-gray-700"
                required
                disabled={loading}
              />
              <p className="text-xs text-gray-500 mt-1">
                ⏰ Unutma eğrisi analizi için test çözme zamanı önemlidir
              </p>
            </div>

            {/* Ders */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                📚 Ders
              </label>
              {loadingSubjects ? (
                <div className="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-50 text-gray-500">
                  Dersler yükleniyor...
                </div>
              ) : (
                <select
                  value={subjectId}
                  onChange={(e) => {
                    setSubjectId(e.target.value);
                    setTopicId('');
                  }}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none text-gray-700"
                  required
                  disabled={loading}
                >
                  <option value="" className="text-gray-500">Ders Seçin</option>
                  {subjects.map((subject) => (
                    <option key={subject.id} value={subject.id} className="text-gray-700">
                      {subject.icon} {subject.name_tr}
                    </option>
                  ))}
                </select>
              )}
            </div>

            {/* Konu */}
            {subjectId && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  📖 Konu
                </label>
                {loadingTopics ? (
                  <div className="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-50 text-gray-500">
                    Konular yükleniyor...
                  </div>
                ) : (
                  <select
                    value={topicId}
                    onChange={(e) => setTopicId(e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none text-gray-700"
                    required
                    disabled={loading}
                  >
                    <option value="" className="text-gray-500">Konu Seçin</option>
                    {topics.map((topic) => (
                      <option key={topic.id} value={topic.id} className="text-gray-700">
                        {topic.name_tr} 
                        {topic.difficulty_level && ` (⭐${topic.difficulty_level})`}
                      </option>
                    ))}
                  </select>
                )}
              </div>
            )}

            {/* Soru Sayıları */}
            <div className="grid grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  ✅ Doğru
                </label>
                <input
                  type="number"
                  min="0"
                  value={correctCount}
                  onChange={(e) => setCorrectCount(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none text-gray-700 placeholder-gray-500"
                  placeholder="0"
                  required
                  disabled={loading}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  ❌ Yanlış
                </label>
                <input
                  type="number"
                  min="0"
                  value={wrongCount}
                  onChange={(e) => setWrongCount(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none text-gray-700 placeholder-gray-500"
                  placeholder="0"
                  required
                  disabled={loading}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  ⭕ Boş
                </label>
                <input
                  type="number"
                  min="0"
                  value={emptyCount}
                  onChange={(e) => setEmptyCount(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none text-gray-700 placeholder-gray-500"
                  placeholder="0"
                  required
                  disabled={loading}
                />
              </div>
            </div>

            {/* Net Gösterimi */}
            <div className="bg-blue-50 p-4 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Net</p>
              <p className="text-3xl font-bold text-blue-600">{net.toFixed(2)}</p>
            </div>

            {/* Butonlar */}
            <div className="flex gap-4">
              <button
                type="button"
                onClick={() => router.push('/dashboard')}
                className="flex-1 bg-gray-200 text-gray-700 py-3 rounded-lg hover:bg-gray-300 transition font-semibold"
                disabled={loading}
              >
                İptal
              </button>
              
              <button
                type="submit"
                className="flex-1 bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition font-semibold disabled:bg-gray-400"
                disabled={loading || !subjectId || !topicId}
              >
                {loading ? 'Kaydediliyor...' : 'Kaydet'}
              </button>
            </div>
          </form>
        </div>
      </main>
    </div>
  );
}