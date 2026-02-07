'use client';

import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { api } from '@/lib/api/client';
import { calculateAllMotors } from '@/lib/api/endpoints/motors';

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

export default function TestEntryClient() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [loading, setLoading] = useState(false);
  const [loadingSubjects, setLoadingSubjects] = useState(true);
  const [loadingTopics, setLoadingTopics] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // ✅ NEW: motor results & last test like new code
  const [motorResults, setMotorResults] = useState<any>(null);
  const [lastTest, setLastTest] = useState<any>(null);

  // Form state
  const [testDateTime, setTestDateTime] = useState('');
  const [selectedSubject, setSelectedSubject] = useState('');
  const [selectedTopic, setSelectedTopic] = useState('');
  const [correctCount, setCorrectCount] = useState<string>('');
  const [wrongCount, setWrongCount] = useState<string>('');
  const [emptyCount, setEmptyCount] = useState<string>('');
  const [testDuration, setTestDuration] = useState<string>(''); // ✅ Test süresi (dakika)

  // Hesaplanan değerler
  const correct = parseInt(correctCount) || 0;
  const wrong = parseInt(wrongCount) || 0;
  const empty = parseInt(emptyCount) || 0;
  const totalQuestions = correct + wrong + empty;
  const net = Math.max(0, correct - wrong / 4);
  const successRate = totalQuestions > 0 ? (correct / totalQuestions) * 100 : 0;

  // ✅ Test süresi için NaN-safe ve null-aware değer
  const durationMinutes =
    testDuration && !isNaN(parseInt(testDuration))
      ? parseInt(testDuration)
      : null;

  // ✅ TOPLAM SORU KONTROLÜ (EditTestModal gibi)
  const isValidTotal = () => totalQuestions === 12;

  // Max datetime
  const getTurkeyDateTime = () => {
    const now = new Date();

    // Local time için timezone offset düzeltmesi
    const offset = now.getTimezoneOffset() * 60000;
    const localISOTime = new Date(now.getTime() - offset)
      .toISOString()
      .slice(0, 16);

    return localISOTime;
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
    let cancelled = false;

    const fetchSubjects = async () => {
      try {
        setLoadingSubjects(true);

        const response = (await api.get('/subjects')) as any;
        if (cancelled) return;

        setSubjects(response?.data || response);
      } catch (err: any) {
        // ✅ SESSION_NOT_READY gelirse sessizce çık (UI kırma)
        if (err?.code === 'SESSION_NOT_READY' && err?.silent) return;

        console.error('Subjects fetch error:', err);
        setError('Dersler yüklenemedi');
      } finally {
        if (!cancelled) setLoadingSubjects(false);
      }
    };

    fetchSubjects();
    return () => {
      cancelled = true;
    };
  }, []);

  // ✅ Pre-fill from query params (subjects yüklendikten sonra)
  useEffect(() => {
    let cancelled = false;

    const subjectId = searchParams.get('subject_id');
    const topicId = searchParams.get('topic_id');

    // Subjects yüklenene kadar bekle
    if (!subjectId || !topicId || subjects.length === 0) return;

    // Subject seç
    setSelectedSubject(subjectId);

    const loadTopics = async () => {
      try {
        setLoadingTopics(true);

        const response = (await api.get(`/subjects/${subjectId}/topics`)) as any;
        if (cancelled) return;

        const topicsData = response?.data || response;
        setTopics(topicsData);

        // Topic seç + scroll
        setTimeout(() => {
          if (cancelled) return;
          setSelectedTopic(topicId);

          setTimeout(() => {
            if (cancelled) return;
            document.getElementById('test-form')?.scrollIntoView({
              behavior: 'smooth',
              block: 'start',
            });
          }, 300);
        }, 100);
      } catch (e: any) {
        if (e?.code === 'SESSION_NOT_READY' && e?.silent) return;

        console.error('Topics fetch error:', e);
        setError('Konular yüklenemedi');
      } finally {
        if (!cancelled) setLoadingTopics(false);
      }
    };

    loadTopics();

    return () => {
      cancelled = true;
    };
  }, [searchParams, subjects]);

  // Subject değişince topics yükle
  useEffect(() => {
    let cancelled = false;

    if (!selectedSubject) {
      setTopics([]);
      return;
    }

    localStorage.setItem('last_subject_id', selectedSubject);

    const fetchTopics = async () => {
      setLoadingTopics(true);
      try {
        const response = (await api.get(`/subjects/${selectedSubject}/topics`)) as any;
        if (cancelled) return;

        setTopics(response?.data || response);
      } catch (err: any) {
        if (err?.code === 'SESSION_NOT_READY' && err?.silent) return;

        console.error('Topics fetch error:', err);
        setError('Konular yüklenemedi');
      } finally {
        if (!cancelled) setLoadingTopics(false);
      }
    };

    fetchTopics();

    return () => {
      cancelled = true;
    };
  }, [selectedSubject]);

  // Konu seçildiğinde kaydet
  useEffect(() => {
    if (selectedTopic) {
      localStorage.setItem('last_topic_id', selectedTopic);
    }
  }, [selectedTopic]);

  const handleReset = () => {
    setCorrectCount('');
    setWrongCount('');
    setEmptyCount('');
    setTestDuration('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // ✅ TOPLAM SORU KONTROLÜ
    if (!isValidTotal()) {
      setError('Toplam soru sayısı tam olarak 12 olmalıdır!');
      return;
    }

    setLoading(true);
    setError(null);
    setSuccess(false);
    setMotorResults(null);
    setLastTest(null);

    try {
      // ✅ Gelecek tarih kontrolü
      const nowLocal = getTurkeyDateTime();

      if (testDateTime > nowLocal) {
        throw new Error('⚠️ Gelecek tarih seçilemez! Test zaten çözülmüş olmalı.');
      }

      // 1) Test kaydet (Backend)
      const testPayload = {
        subject_id: selectedSubject,
        topic_id: selectedTopic,
        test_date: testDateTime + ':00',
        correct_count: correct,
        wrong_count: wrong,
        empty_count: empty,
        net_score: parseFloat(net.toFixed(2)),
        success_rate: parseFloat(successRate.toFixed(2)),
        test_duration_minutes: durationMinutes,
      };

      const saved = await api.post('/test-results', testPayload);

      setLastTest(saved);

      // 2) Motorları hesapla (fail-safe)
      try {
        const motors = await calculateAllMotors({
          student_id: 'me',
          topic_id: selectedTopic,
          correct,
          incorrect: wrong,
          blank: empty,
          total: 12,
          time_spent: durationMinutes ? durationMinutes * 60 : 900,
          test_date: testDateTime,
          user_tier: 'premium',
        });

        setMotorResults(motors);
      } catch (motorErr) {
        console.error('Motor calculation error:', motorErr);
      }

      setSuccess(true);

      // ✅ 2 sn sonra geçmiş testlere yönlendir
      setTimeout(() => {
        router.push('/past-tests');
      }, 2000);
    } catch (err: any) {
      console.error('Test entry error:', err);
      setError(err.message || 'Test kaydı sırasında hata oluştu');
    } finally {
      setLoading(false);
    }
  };

  // Logout
  const handleLogout = () => {
    document.cookie = 'access_token=; path=/; max-age=0';
    router.push('/login');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-100 via-blue-50 to-purple-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div
            className="flex items-center gap-3 cursor-pointer"
            onClick={() => router.push('/student/dashboard')}
          >
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

      <main className="max-w-2xl mx-auto px-4 py-8" id="test-form">
        {/* Success Message */}
        {success && (
          <div className="bg-green-100 border-2 border-green-500 text-green-800 px-6 py-4 rounded-2xl mb-6 animate-pulse">
            <div className="flex items-center gap-3">
              <span className="text-3xl">✅</span>
              <div className="w-full">
                <div className="font-bold">Test başarıyla kaydedildi!</div>
                <div className="text-sm">Net: {net.toFixed(2)} 🎉</div>
                <div className="text-xs mt-1">Geçmiş testlere yönlendiriliyorsunuz...</div>

                {/* NEW: task auto completed */}
                {lastTest?.task_auto_completed && (
                  <div className="text-xs mt-2 text-green-700">
                    🎉 Görev otomatik tamamlandı: {lastTest.completed_task?.task_name}
                  </div>
                )}

                {/* NEW: Motor sonuçları */}
                {motorResults && (
                  <div className="mt-3 space-y-2">
                    <div className="text-xs text-gray-600">
                      🤖 Aşağıdaki yorumlar analiz motorları tarafından otomatik oluşturulmuştur.
                    </div>

                    {motorResults.bsModel?.data && (
                      <div className="bg-white p-3 rounded-lg border border-green-200">
                        <p className="text-sm font-medium text-gray-700">
                          {motorResults.bsModel.data.analysis}
                        </p>
                        <p className="text-xs text-gray-500 mt-1">
                          Motor: {motorResults.bsModel.meta?.motor_version}
                          {motorResults.bsModel.data?.v2_features?.archetype
                            ? ` | Archetype: ${motorResults.bsModel.data.v2_features.archetype}`
                            : ''}
                        </p>
                      </div>
                    )}

                    {motorResults.difficulty?.data && (
                      <div className="bg-white p-3 rounded-lg border border-green-200">
                        <p className="text-sm font-medium text-gray-700">
                          {motorResults.difficulty.data.analysis}
                        </p>
                        <p className="text-xs text-gray-500 mt-1">
                          Seviye: {motorResults.difficulty.data.difficulty_level}
                        </p>
                      </div>
                    )}

                    {motorResults.priority?.data?.priorities?.[0] && (
                      <div className="bg-white p-3 rounded-lg border border-green-200">
                        <p className="text-sm font-medium text-gray-700">
                          {motorResults.priority.data.priorities[0].suggestion}
                        </p>
                      </div>
                    )}
                  </div>
                )}
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
            <label className="block text-sm font-semibold text-gray-700 mb-2">📚 Ders</label>
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
                {subjects?.map((subject) => (
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
              <label className="block text-sm font-semibold text-gray-700 mb-2">📖 Konu</label>
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
                  {topics?.map((topic) => (
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
              <label className="block text-sm font-semibold text-green-700 mb-2">✅ Doğru</label>
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
              <label className="block text-sm font-semibold text-red-700 mb-2">❌ Yanlış</label>
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
              <label className="block text-sm font-semibold text-gray-700 mb-2">⭕ Boş</label>
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

          {/* Test Süresi */}
          <div className="mb-6">
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              ⏱️ Test Süresi (Opsiyonel)
            </label>
            <div className="flex items-center gap-3">
              <input
                type="number"
                min="1"
                max="120"
                value={testDuration}
                onChange={(e) => setTestDuration(e.target.value)}
                className="w-32 px-4 py-3 border-2 border-blue-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent text-center text-xl font-bold"
                placeholder="0"
                disabled={loading}
              />
              <span className="text-gray-600 font-semibold">dakika</span>
            </div>
            <p className="text-xs text-gray-500 mt-2">
              💡 12 soruyu kaç dakikada çözdüğünüzü girin. Hız analizi için kullanılacak (isteğe
              bağlı)
            </p>
          </div>

          {/* Hesaplanan Değerler */}
          <div
            className={`rounded-2xl p-6 mb-6 border-2 ${
              isValidTotal()
                ? 'bg-gradient-to-br from-purple-50 to-blue-50 border-purple-200'
                : 'bg-gradient-to-br from-red-50 to-orange-50 border-red-300'
            }`}
          >
            <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center justify-center gap-2">
              📊 Hesaplanan Değerler
              {!isValidTotal() && totalQuestions > 0 && (
                <span className="text-sm bg-red-500 text-white px-3 py-1 rounded-full animate-pulse">
                  ⚠️ Toplam 12 soru olmalı!
                </span>
              )}
            </h3>

            <div className="grid grid-cols-3 gap-4 mb-4">
              <div className="text-center">
                <div className="text-sm text-gray-600 mb-1">Toplam Soru</div>
                <div
                  className={`text-3xl font-bold ${
                    totalQuestions === 12
                      ? 'text-green-600'
                      : totalQuestions < 12
                      ? 'text-orange-600'
                      : 'text-red-600'
                  }`}
                >
                  {totalQuestions} / 12
                </div>
              </div>

              <div className="text-center">
                <div className="text-sm text-gray-600 mb-1">📊 Net</div>
                <div className="text-3xl font-bold text-purple-600">{net.toFixed(2)}</div>
              </div>

              <div className="text-center">
                <div className="text-sm text-gray-600 mb-1">📈 Başarı %</div>
                <div className="text-3xl font-bold text-blue-600">
                  {successRate.toFixed(0)}%
                </div>
              </div>
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
              disabled={
                loading ||
                !selectedSubject ||
                !selectedTopic ||
                !testDateTime ||
                !isValidTotal()
              }
              className={`flex-1 py-3 rounded-xl text-white font-semibold transition-all ${
                loading ||
                !selectedSubject ||
                !selectedTopic ||
                !testDateTime ||
                !isValidTotal()
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-gradient-to-r from-purple-600 to-blue-600 hover:scale-105 shadow-lg'
              }`}
            >
              {loading
                ? '⏳ Kaydediliyor...'
                : !isValidTotal()
                ? '❌ Toplam 12 soru olmalı'
                : '💾 Test Sonucunu Kaydet'}
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