'use client';

import { useState, useEffect } from 'react';
import { calculateAllMotors } from '@/lib/api/endpoints/motors';

interface Subject {
  id: string;
  code: string;
  name_tr: string;
  icon?: string;
  color?: string;
}

interface Topic {
  id: string;
  code: string;
  name_tr: string;
}

export default function TestEntry() {
  // State management
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [selectedSubject, setSelectedSubject] = useState('');
  const [selectedTopic, setSelectedTopic] = useState('');
  const [testDateTime, setTestDateTime] = useState('');
  const [correct, setCorrect] = useState('');
  const [wrong, setWrong] = useState('');
  const [empty, setEmpty] = useState('');
  const [testDuration, setTestDuration] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [motorResults, setMotorResults] = useState<any>(null);
  const [lastTest, setLastTest] = useState<any>(null);

  // Load subjects
  useEffect(() => {
    const fetchSubjects = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/subjects');
        const data = await response.json();
        setSubjects(data);
      } catch (err: any) {
        console.error('Subjects fetch error:', err);
        setError('Dersler yüklenemedi');
      }
    };
    fetchSubjects();
  }, []);

  // Load topics when subject changes
  useEffect(() => {
    if (!selectedSubject) {
      setTopics([]);
      return;
    }

    const fetchTopics = async () => {
      try {
        const response = await fetch(
          `http://localhost:8000/api/v1/subjects/${selectedSubject}/topics`
        );
        const data = await response.json();
        setTopics(data);
      } catch (err: any) {
        console.error('Topics fetch error:', err);
        setError('Konular yüklenemedi');
      }
    };
    fetchTopics();
  }, [selectedSubject]);

  // Calculate totals
  const total = parseInt(correct || '0') + parseInt(wrong || '0') + parseInt(empty || '0');
  const net = parseFloat(correct || '0') - parseFloat(wrong || '0') / 4;
  const successRate = total > 0 ? (parseFloat(correct || '0') / total) * 100 : 0;

  // Validation
  const isValidTotal = () => total === 12;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!isValidTotal()) {
      setError('Toplam soru sayısı tam olarak 12 olmalıdır!');
      return;
    }

    setLoading(true);
    setError(null);
    setSuccess(false);
    setMotorResults(null);

    try {
      const userStr = localStorage.getItem('user');
      const accessToken = localStorage.getItem('access_token');

      if (!userStr || !accessToken) {
        throw new Error('Lütfen giriş yapın');
      }

      const user = JSON.parse(userStr);

      // 1. Save test result
      const testData = {
        student_id: user.id,
        subject_id: selectedSubject,
        topic_id: selectedTopic,
        test_date: testDateTime + ':00',
        correct_count: parseInt(correct),
        wrong_count: parseInt(wrong),
        empty_count: parseInt(empty),
        net_score: parseFloat(net.toFixed(2)),
        success_rate: parseFloat(successRate.toFixed(2)),
        test_duration_minutes: testDuration ? parseInt(testDuration) : null,
      };

      const response = await fetch('http://localhost:8000/api/v1/test-results', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify(testData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Test kaydedilemedi');
      }

      const result = await response.json();
      setLastTest(result);

      // 2. Calculate motors (parallel)
      try {
        const motors = await calculateAllMotors({
          student_id: user.id,
          topic_id: selectedTopic,
          correct: parseInt(correct),
          incorrect: parseInt(wrong),
          blank: parseInt(empty),
          total: 12,
          time_spent: testDuration ? parseInt(testDuration) * 60 : 900,
          test_date: testDateTime,
          user_tier: 'premium',
        });

        setMotorResults(motors);
      } catch (motorError) {
        console.error('Motor calculation error:', motorError);
        // Don't fail the whole operation if motors fail
      }

      setSuccess(true);

      // Clear form after 5 seconds
      setTimeout(() => {
        setCorrect('');
        setWrong('');
        setEmpty('');
        setTestDuration('');
        setSuccess(false);
        setMotorResults(null);
      }, 5000);
    } catch (err: any) {
      console.error('Submit error:', err);
      setError(err.message || 'Bir hata oluştu');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 p-8">
      <form onSubmit={handleSubmit} className="bg-white rounded-3xl shadow-2xl p-8 max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">📝 Konu Öğrenme Testi</h1>
        <p className="text-gray-600 mb-6">Çözdüğünüz 12 soruluk test sonucunu girin</p>

        {/* Error message */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6">
            <p className="text-red-700">❌ {error}</p>
          </div>
        )}

        {/* Success message */}
        {success && (
          <div className="bg-green-50 border-l-4 border-green-500 p-4 mb-6">
            <p className="text-green-700 font-semibold">✅ Test başarıyla kaydedildi!</p>
            
            {lastTest?.task_auto_completed && (
              <p className="text-green-600 mt-2">
                🎉 Görev otomatik tamamlandı: {lastTest.completed_task?.task_name}
              </p>
            )}

            {motorResults && (
              <div className="mt-4 space-y-2">
                {motorResults.bsModel?.data && (
                  <div className="bg-white p-3 rounded-lg border border-green-200">
                    <p className="text-sm font-medium text-gray-700">
                      {motorResults.bsModel.data.analysis}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      Motor: {motorResults.bsModel.meta.motor_version} | 
                      Archetype: {motorResults.bsModel.data.v2_features?.archetype}
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

                {motorResults.priority?.data && motorResults.priority.data.priorities?.[0] && (
                  <div className="bg-white p-3 rounded-lg border border-green-200">
                    <p className="text-sm font-medium text-gray-700">
                      {motorResults.priority.data.priorities[0].suggestion}
                    </p>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* Test Date */}
        <div className="mb-6">
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            📅 Test Tarihi ve Saati
          </label>
          <input
            type="datetime-local"
            value={testDateTime}
            onChange={(e) => setTestDateTime(e.target.value)}
            max={new Date().toISOString().slice(0, 16)}
            required
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
          />
        </div>

        {/* Subject Selection */}
        <div className="mb-6">
          <label className="block text-sm font-semibold text-gray-700 mb-2">📚 Ders</label>
          <select
            value={selectedSubject}
            onChange={(e) => {
              setSelectedSubject(e.target.value);
              setSelectedTopic('');
            }}
            required
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-500"
          >
            <option value="">Ders seçin...</option>
            {subjects.map((subject) => (
              <option key={subject.id} value={subject.id}>
                {subject.icon || '📖'} {subject.name_tr}
              </option>
            ))}
          </select>
        </div>

        {/* Topic Selection */}
        <div className="mb-6">
          <label className="block text-sm font-semibold text-gray-700 mb-2">📖 Konu</label>
          <select
            value={selectedTopic}
            onChange={(e) => setSelectedTopic(e.target.value)}
            required
            disabled={!selectedSubject}
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-500 disabled:bg-gray-100"
          >
            <option value="">Konu seçin...</option>
            {topics.map((topic) => (
              <option key={topic.id} value={topic.id}>
                {topic.name_tr}
              </option>
            ))}
          </select>
        </div>

        {/* Answer counts */}
        <div className="grid grid-cols-3 gap-4 mb-6">
          <div>
            <label className="block text-sm font-semibold text-green-600 mb-2">✅ Doğru</label>
            <input
              type="number"
              value={correct}
              onChange={(e) => setCorrect(e.target.value)}
              min="0"
              max="12"
              required
              className="w-full px-4 py-3 border-2 border-green-200 rounded-xl focus:border-green-500"
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-red-600 mb-2">❌ Yanlış</label>
            <input
              type="number"
              value={wrong}
              onChange={(e) => setWrong(e.target.value)}
              min="0"
              max="12"
              required
              className="w-full px-4 py-3 border-2 border-red-200 rounded-xl focus:border-red-500"
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-gray-600 mb-2">⚪ Boş</label>
            <input
              type="number"
              value={empty}
              onChange={(e) => setEmpty(e.target.value)}
              min="0"
              max="12"
              required
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-gray-500"
            />
          </div>
        </div>

        {/* Duration */}
        <div className="mb-6">
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            ⏱️ Süre (dakika) <span className="text-xs text-gray-500">(Opsiyonel - daha iyi analiz için önerilir)</span>
          </label>
          <input
            type="number"
            value={testDuration}
            onChange={(e) => setTestDuration(e.target.value)}
            min="1"
            placeholder="Örn: 15"
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-500"
          />
        </div>

        {/* Summary */}
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-2xl mb-6">
          <div className="flex justify-between items-center">
            <div className="text-center">
              <p className="text-sm text-gray-600">Toplam</p>
              <p className={`text-3xl font-bold ${total === 12 ? 'text-green-600' : 'text-red-600'}`}>
                {total}/12
              </p>
            </div>
            <div className="text-center">
              <p className="text-sm text-gray-600">Net</p>
              <p className="text-3xl font-bold text-blue-600">{net.toFixed(2)}</p>
            </div>
          </div>
          {total !== 12 && (
            <p className="text-red-600 text-sm mt-2 text-center">
              ⚠️ Toplam tam 12 olmalı!
            </p>
          )}
        </div>

        {/* Submit */}
        <button
          type="submit"
          disabled={loading || !isValidTotal()}
          className="w-full py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold rounded-xl hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
        >
          {loading ? '⏳ Kaydediliyor...' : '💾 Kaydet ve Analiz Et'}
        </button>
      </form>
    </div>
  );
}
