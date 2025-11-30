'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

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
  difficulty_level?: number;
  exam_weight?: number;
}

export default function TestEntryPage() {
  const router = useRouter();
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [loading, setLoading] = useState(false);
  const [loadingSubjects, setLoadingSubjects] = useState(true);
  const [loadingTopics, setLoadingTopics] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [validationError, setValidationError] = useState('');

  // Form state
  const [testDateTime, setTestDateTime] = useState('');
  const [selectedSubject, setSelectedSubject] = useState('');
  const [selectedTopic, setSelectedTopic] = useState('');
  const [correctCount, setCorrectCount] = useState<string>('');
  const [wrongCount, setWrongCount] = useState<string>('');
  const [emptyCount, setEmptyCount] = useState<string>('');

  // Hesaplanan değerler
  const correct = parseInt(correctCount) || 0;
  const wrong = parseInt(wrongCount) || 0;
  const empty = parseInt(emptyCount) || 0;
  const totalQuestions = correct + wrong + empty;
  const net = Math.max(0, correct - (wrong / 4));
  const successRate = totalQuestions > 0 ? (correct / totalQuestions) * 100 : 0;

  // Max datetime
  const getTurkeyDateTime = () => {
    const now = new Date();
    return now.toISOString().slice(0, 16);
  };

  // LocalStorage'dan son seçimleri yükle
  useEffect(() => {
    const lastSubject = localStorage.getItem('last_subject_id');
    const lastTopic = localStorage.getItem('last_topic_id');
    
    if (lastSubject) setSelectedSubject(lastSubject);
    if (lastTopic) setSelectedTopic(lastTopic);
  }, []);

  // Subjects yükle
  useEffect(() => {
    const fetchSubjects = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/subjects');
        const data = await response.json();
        setSubjects(data);
      } catch (err) {
        console.error('Subjects fetch error:', err);
        setError('Dersler yüklenemedi');
      } finally {
        setLoadingSubjects(false);
      }
    };

    fetchSubjects();
  }, []);

  // Subject değişince topics yükle
  useEffect(() => {
    if (!selectedSubject) {
      setTopics([]);
      return;
    }

    localStorage.setItem('last_subject_id', selectedSubject);

    const fetchTopics = async () => {
      setLoadingTopics(true);
      try {
        const response = await fetch(`http://localhost:8000/api/v1/subjects/${selectedSubject}/topics`);
        const data = await response.json();
        setTopics(data);
      } catch (err) {
        console.error('Topics fetch error:', err);
        setError('Konular yüklenemedi');
      } finally {
        setLoadingTopics(false);
      }
    };

    fetchTopics();
  }, [selectedSubject]);

  // Konu seçildiğinde kaydet
  useEffect(() => {
    if (selectedTopic) {
      localStorage.setItem('last_topic_id', selectedTopic);
    }
  }, [selectedTopic]);

  // Validasyon kontrolü
  useEffect(() => {
    setValidationError('');

    if (correct < 0 || wrong < 0 || empty < 0) {
      setValidationError('❌ Negatif sayı giremezsiniz!');
      return;
    }

    // KONU ÖĞRENMESİ: 12 SORU
    const maxQuestions = 12;

    if (totalQuestions > maxQuestions) {
      setValidationError(`❌ Toplam soru sayısı ${maxQuestions}'den fazla olamaz! (Şu an: ${totalQuestions})`);
      return;
    }

    if (totalQuestions > 0 && totalQuestions < maxQuestions) {
      setValidationError(`⚠️ Konu öğrenme testi ${maxQuestions} soru olmalı. (Şu an: ${totalQuestions})`);
    }
  }, [correctCount, wrongCount, emptyCount, correct, wrong, empty, totalQuestions]);

  const handleReset = () => {
    setCorrectCount('');
    setWrongCount('');
    setEmptyCount('');
    setValidationError('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (validationError && validationError.includes('❌')) {
      return;
    }

    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      // Gelecek tarih kontrolü
      const selectedDateTime = new Date(testDateTime);
      const now = new Date();
      
      if (selectedDateTime > now) {
        throw new Error('⚠️ Gelecek tarih seçilemez! Test zaten çözülmüş olmalı.');
      }

      // User ve token
      const userStr = localStorage.getItem('user');
      const accessToken = localStorage.getItem('access_token');
      
      if (!userStr || !accessToken) {
        throw new Error('Lütfen giriş yapın');
      }

      const user = JSON.parse(userStr);

      const response = await fetch('http://localhost:8000/api/v1/test-results', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`,
        },
        body: JSON.stringify({
          student_id: user.id,
          subject_id: selectedSubject,
          topic_id: selectedTopic,
          test_date: testDateTime + ':00',
          correct_count: correct,
          wrong_count: wrong,
          empty_count: empty,
          net_score: parseFloat(net.toFixed(2)),
          success_rate: parseFloat(successRate.toFixed(2)),
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Test kaydedilemedi');
      }

      setSuccess(true);
      
      setTimeout(() => {
        router.push('/student/dashboard');
      }, 2000);

    } catch (err: any) {
      console.error('Test entry error:', err);
      setError(err.message || 'Test kaydı sırasında hata oluştu');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    document.cookie = 'access_token=; path=/; max-age=0';
    router.push('/login');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-100 via-blue-50 to-purple-50">
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

      <main className="max-w-2xl mx-auto px-4 py-8">
        {/* Success Message */}
        {success && (
          <div className="bg-green-100 border-2 border-green-500 text-green-800 px-6 py-4 rounded-2xl mb-6 animate-pulse">
            <div className="flex items-center gap-3">
              <span className="text-3xl">✅</span>
              <div>
                <div className="font-bold">Test başarıyla kaydedildi!</div>
                <div className="text-sm">Net: {net.toFixed(2)} 🎉</div>
                <div className="text-xs mt-1">Dashboard'a yönlendiriliyorsunuz...</div>
              </div>
            </div>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="bg-red-100 border-2 border-red-500 text-red-800 px-6 py-4 rounded-2xl mb-6">
            <div className="flex items-center gap-3">
              <span className="text-3xl">❌</span>
              <div>
                <div className="font-bold">Hata!</div>
                <div className="text-sm">{error}</div>
              </div>
            </div>
          </div>
        )}

        {/* Validation Warning */}
        {validationError && (
          <div className={`border-2 px-6 py-4 rounded-2xl mb-6 ${
            validationError.includes('❌') 
              ? 'bg-red-50 border-red-500 text-red-700' 
              : 'bg-yellow-50 border-yellow-500 text-yellow-700'
          }`}>
            <p className="font-medium">{validationError}</p>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="bg-white rounded-3xl shadow-2xl p-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">📝 Konu Öğrenme Testi</h1>
          <p className="text-gray-600 mb-6">Çözdüğünüz 12 soruluk test sonucunu girin</p>

          {/* Tarih ve Saat */}
          <div className="mb-6">
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              📅 Test Tarihi ve Saati
            </label>
            <input
              type="datetime-local"
              value={testDateTime}
              onChange={(e) => setTestDateTime(e.target.value)}
              max={getTurkeyDateTime()}
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              required
              disabled={loading}
            />
            <p className="text-xs text-gray-500 mt-1">
              ⏰ Unutma eğrisi analizi için test çözme zamanı önemlidir
            </p>
          </div>

          {/* Subject Dropdown */}
          <div className="mb-6">
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              📚 Ders
            </label>
            {loadingSubjects ? (
              <div className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl bg-gray-50 text-gray-500">
                Dersler yükleniyor...
              </div>
            ) : (
              <select
                value={selectedSubject}
                onChange={(e) => {
                  setSelectedSubject(e.target.value);
                  setSelectedTopic('');
                }}
                className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                required
                disabled={loading}
              >
                <option value="">Ders seçin...</option>
                {subjects.map((subject) => (
                  <option key={subject.id} value={subject.id}>
                    {subject.icon} {subject.name_tr}
                  </option>
                ))}
              </select>
            )}
          </div>

          {/* Topic Dropdown */}
          {selectedSubject && (
            <div className="mb-6">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                📖 Konu
              </label>
              {loadingTopics ? (
                <div className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl bg-gray-50 text-gray-500">
                  Konular yükleniyor...
                </div>
              ) : (
                <select
                  value={selectedTopic}
                  onChange={(e) => setSelectedTopic(e.target.value)}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  required
                  disabled={loading}
                >
                  <option value="">Konu seçin...</option>
                  {topics.map((topic) => (
                    <option key={topic.id} value={topic.id}>
                      {topic.name_tr}
                      {topic.difficulty_level && ` (⭐${topic.difficulty_level})`}
                    </option>
                  ))}
                </select>
              )}
            </div>
          )}

          {/* Soru Sayıları */}
          <div className="grid grid-cols-3 gap-4 mb-6">
            <div>
              <label className="block text-sm font-semibold text-green-700 mb-2">
                ✅ Doğru
              </label>
              <input
                type="number"
                min="0"
                max="12"
                value={correctCount}
                onChange={(e) => setCorrectCount(e.target.value)}
                className="w-full px-4 py-3 border-2 border-green-300 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent text-center text-xl font-bold"
                placeholder="0"
                required
                disabled={loading}
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-red-700 mb-2">
                ❌ Yanlış
              </label>
              <input
                type="number"
                min="0"
                max="12"
                value={wrongCount}
                onChange={(e) => setWrongCount(e.target.value)}
                className="w-full px-4 py-3 border-2 border-red-300 rounded-xl focus:ring-2 focus:ring-red-500 focus:border-transparent text-center text-xl font-bold"
                placeholder="0"
                required
                disabled={loading}
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                ⭕ Boş
              </label>
              <input
                type="number"
                min="0"
                max="12"
                value={emptyCount}
                onChange={(e) => setEmptyCount(e.target.value)}
                className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-gray-500 focus:border-transparent text-center text-xl font-bold"
                placeholder="0"
                required
                disabled={loading}
              />
            </div>
          </div>

          {/* Hesaplanan Değerler */}
          <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-2xl p-6 mb-6 border-2 border-purple-200">
            <div className="grid grid-cols-2 gap-4">
              <div className="text-center">
                <div className="text-sm text-gray-600 mb-1">📊 Net</div>
                <div className="text-4xl font-bold text-purple-600">
                  {net.toFixed(2)}
                </div>
              </div>
              <div className="text-center">
                <div className="text-sm text-gray-600 mb-1">📈 Başarı Oranı</div>
                <div className="text-4xl font-bold text-blue-600">
                  %{successRate.toFixed(0)}
                </div>
              </div>
            </div>
            <div className="text-center mt-3 text-xs text-gray-500">
              Toplam {totalQuestions}/12 soru
            </div>
          </div>

          {/* Butonlar */}
          <div className="flex gap-4 mb-4">
            <button
              type="button"
              onClick={handleReset}
              className="flex-1 bg-gray-200 text-gray-700 py-3 rounded-xl hover:bg-gray-300 transition font-semibold"
              disabled={loading}
            >
              🔄 Temizle
            </button>

            <button
              type="submit"
              disabled={loading || !selectedSubject || !selectedTopic || !testDateTime || (validationError.includes('❌'))}
              className={`flex-1 py-3 rounded-xl text-white font-semibold transition-all ${
                loading || !selectedSubject || !selectedTopic || !testDateTime || (validationError.includes('❌'))
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-gradient-to-r from-purple-600 to-blue-600 hover:scale-105 shadow-lg'
              }`}
            >
              {loading ? '⏳ Kaydediliyor...' : '💾 Test Sonucunu Kaydet'}
            </button>
          </div>

          <p className="text-xs text-center text-gray-500">
            💡 İpucu: Son seçtiğiniz ders ve konu otomatik hatırlanır
          </p>
        </form>
      </main>
    </div>
  );
}
