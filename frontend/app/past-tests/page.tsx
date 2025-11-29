'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import EditTestModal from './EditTestModal';

interface TestRecord {
  id: string;
  test_date: string;
  correct_count: number;
  wrong_count: number;
  empty_count: number;
  net_score: number;
  success_rate: number;
  topic: {
    name_tr: string;
  };
  subject: {
    name_tr: string;
  };
}

export default function PastTestsPage() {
  const router = useRouter();
  const [tests, setTests] = useState<TestRecord[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deleteConfirm, setDeleteConfirm] = useState<string | null>(null);
  const [editingTest, setEditingTest] = useState<TestRecord | null>(null);

  useEffect(() => {
    loadTests();
  }, []);

  const loadTests = async () => {
    try {
      setIsLoading(true);
      
      const userStr = localStorage.getItem('user');
      const accessToken = localStorage.getItem('access_token');
      
      if (!userStr || !accessToken) {
        router.push('/login');
        return;
      }

      const user = JSON.parse(userStr);

      const response = await fetch(
        `http://localhost:8000/api/v1/student/${user.id}/tests`,
        {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
          },
        }
      );

      if (!response.ok) {
        throw new Error('Testler yüklenemedi');
      }

      const data = await response.json();
      setTests(data.tests || []);
      setError(null);
    } catch (err: any) {
      console.error('Test yükleme hatası:', err);
      setError(err.message || 'Bir hata oluştu');
    } finally {
      setIsLoading(false);
    }
  };

  // ✅ BACKEND'E UPDATE İSTEĞİ YAPAN FONKSİYON
  const updateTestInBackend = async (updatedTestData: any) => {
    const accessToken = localStorage.getItem('access_token');
    
    const response = await fetch(
      `http://localhost:8000/api/v1/tests/${updatedTestData.id}`,
      {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          test_date: updatedTestData.test_date,
          correct_count: updatedTestData.correct_count,
          wrong_count: updatedTestData.wrong_count,
          empty_count: updatedTestData.empty_count,
        }),
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Güncelleme başarısız');
    }

    // Başarılı olduysa listeyi yenile
    await loadTests();
  };

  const handleDelete = async (testId: string) => {
    try {
      const accessToken = localStorage.getItem('access_token');
      
      const response = await fetch(
        `http://localhost:8000/api/v1/tests/${testId}`,
        {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${accessToken}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error('Test silinemedi');
      }

      setTests(tests.filter(t => t.id !== testId));
      setDeleteConfirm(null);
    } catch (err: any) {
      alert('Silme hatası: ' + err.message);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('tr-TR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-pink-50 p-6">
        <div className="max-w-7xl mx-auto">
          <div className="bg-white rounded-2xl p-12 text-center shadow-lg">
            <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-purple-600 mx-auto mb-4"></div>
            <p className="text-gray-600 text-lg">Testler yükleniyor...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-pink-50 p-6">
        <div className="max-w-7xl mx-auto">
          <div className="bg-red-50 border-2 border-red-300 rounded-2xl p-8 text-center">
            <div className="text-6xl mb-4">⚠️</div>
            <h2 className="text-2xl font-bold text-red-600 mb-2">Hata Oluştu</h2>
            <p className="text-red-700 mb-4">{error}</p>
            <button
              onClick={loadTests}
              className="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700"
            >
              Tekrar Dene
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-pink-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-2xl p-6 mb-6 shadow-xl">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold mb-2">📝 Geçmiş Testlerim</h1>
              <p className="text-sm opacity-90">Tüm test sonuçlarını görüntüle ve düzenle</p>
            </div>
            <div className="text-right">
              <div className="text-4xl font-bold">{tests.length}</div>
              <div className="text-sm opacity-90">Toplam Test</div>
            </div>
          </div>
        </div>

        {/* Test Tablosu */}
        {tests.length > 0 ? (
          <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gradient-to-r from-purple-100 to-blue-100">
                  <tr>
                    <th className="px-6 py-4 text-left text-sm font-bold text-gray-700">Tarih</th>
                    <th className="px-6 py-4 text-left text-sm font-bold text-gray-700">Ders</th>
                    <th className="px-6 py-4 text-left text-sm font-bold text-gray-700">Konu</th>
                    <th className="px-6 py-4 text-center text-sm font-bold text-gray-700">D / Y / B</th>
                    <th className="px-6 py-4 text-center text-sm font-bold text-gray-700">Net</th>
                    <th className="px-6 py-4 text-center text-sm font-bold text-gray-700">Başarı %</th>
                    <th className="px-6 py-4 text-center text-sm font-bold text-gray-700">İşlemler</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {tests.map((test) => (
                    <tr key={test.id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-6 py-4 text-sm text-gray-700">
                        {formatDate(test.test_date)}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-700">
                        {test.subject?.name_tr || '-'}
                      </td>
                      <td className="px-6 py-4 text-sm font-semibold text-gray-800">
                        {test.topic?.name_tr || '-'}
                      </td>
                      <td className="px-6 py-4 text-center">
                        <div className="flex items-center justify-center gap-2 text-sm">
                          <span className="text-green-600 font-semibold">{test.correct_count}</span>
                          <span className="text-gray-400">/</span>
                          <span className="text-red-600 font-semibold">{test.wrong_count}</span>
                          <span className="text-gray-400">/</span>
                          <span className="text-gray-500 font-semibold">{test.empty_count}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 text-center">
                        <span className="text-lg font-bold text-purple-600">
                          {test.net_score.toFixed(2)}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-center">
                        <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                          test.success_rate >= 80 ? 'bg-green-100 text-green-700' :
                          test.success_rate >= 60 ? 'bg-yellow-100 text-yellow-700' :
                          'bg-red-100 text-red-700'
                        }`}>
                          %{test.success_rate.toFixed(0)}
                        </span>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center justify-center gap-2">
                          <button
                            onClick={() => setEditingTest(test)}
                            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors"
                          >
                            ✏️ Düzenle
                          </button>
                          
                          {deleteConfirm === test.id ? (
                            <div className="flex gap-1">
                              <button
                                onClick={() => handleDelete(test.id)}
                                className="bg-red-600 hover:bg-red-700 text-white px-3 py-2 rounded-lg text-xs font-semibold"
                              >
                                ✓ Evet
                              </button>
                              <button
                                onClick={() => setDeleteConfirm(null)}
                                className="bg-gray-500 hover:bg-gray-600 text-white px-3 py-2 rounded-lg text-xs font-semibold"
                              >
                                ✗ Hayır
                              </button>
                            </div>
                          ) : (
                            <button
                              onClick={() => setDeleteConfirm(test.id)}
                              className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors"
                            >
                              🗑️ Sil
                            </button>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        ) : (
          <div className="bg-white rounded-2xl p-12 text-center shadow-lg">
            <div className="text-6xl mb-4">📝</div>
            <h3 className="text-2xl font-bold text-gray-800 mb-2">Henüz Test Girmediniz</h3>
            <p className="text-gray-600 mb-4">
              Test girişi yapmak için ana sayfaya gidin ve yeni test ekleyin.
            </p>
            <a
              href="/test-entry"
              className="inline-block bg-gradient-to-r from-purple-600 to-blue-600 text-white px-8 py-3 rounded-xl font-bold hover:scale-105 transition-transform shadow-lg"
            >
              ➕ Yeni Test Ekle
            </a>
          </div>
        )}

        {/* Geri Dön Butonu */}
        <div className="mt-6 text-center">
          <a
            href="/student/dashboard"
            className="inline-block bg-gradient-to-r from-purple-600 to-blue-600 text-white px-8 py-3 rounded-xl font-bold hover:scale-105 transition-transform shadow-lg"
          >
            ← Dashboard'a Dön
          </a>
        </div>
      </div>

      {/* Edit Modal - ✅ DOĞRU onSave KULLANIMI */}
      {editingTest && (
        <EditTestModal
          test={editingTest}
          onClose={() => setEditingTest(null)}
          onSave={async (updatedData) => {
            await updateTestInBackend(updatedData);
            setEditingTest(null);
          }}
        />
      )}
    </div>
  );
}