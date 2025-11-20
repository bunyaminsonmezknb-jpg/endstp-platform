'use client';

import Image from 'next/image';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import WeeklyChart from './WeeklyChart';

interface DashboardData {
  student: {
    name: string;
    class: string;
  };
  recent_tests: any[];
  topic_performance: any[];
}

// Loading Skeleton Component
function DashboardSkeleton() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gray-200 rounded-full animate-pulse"></div>
            <div className="w-32 h-8 bg-gray-200 rounded animate-pulse"></div>
          </div>
          <div className="w-24 h-8 bg-gray-200 rounded animate-pulse"></div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {[1,2,3].map(i => (
            <div key={i} className="bg-white p-6 rounded-xl shadow-md">
              <div className="h-20 bg-gray-200 rounded animate-pulse"></div>
            </div>
          ))}
        </div>
        
        <div className="bg-white rounded-xl shadow-md p-6 mb-8">
          <div className="h-64 bg-gray-200 rounded animate-pulse"></div>
        </div>
      </main>
    </div>
  );
}

// Empty State Component
function EmptyState({ onAddTest }: { onAddTest: () => void }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <Image src="/logo.png" alt="End.STP" width={40} height={40} />
            <span className="text-2xl font-bold text-gray-800">End.STP</span>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-16">
        <div className="bg-white rounded-xl shadow-lg p-12 text-center">
          <div className="text-8xl mb-6">📝</div>
          <h2 className="text-3xl font-bold text-gray-800 mb-4">
            Henüz Test Eklemediniz
          </h2>
          <p className="text-gray-600 mb-8 text-lg">
            İlk testinizi ekleyerek analiz sistemini kullanmaya başlayın!
          </p>
          
          <button
            onClick={onAddTest}
            className="inline-flex items-center gap-2 bg-blue-600 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:bg-blue-700 transition shadow-lg hover:shadow-xl transform hover:scale-105"
          >
            <span className="text-2xl">+</span>
            İlk Testimi Ekle
          </button>

          <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6 text-left">
            <div className="p-4 bg-blue-50 rounded-lg">
              <div className="text-3xl mb-2">📊</div>
              <h3 className="font-semibold text-gray-800 mb-1">Detaylı Analiz</h3>
              <p className="text-sm text-gray-600">Performansınızı grafiklerle takip edin</p>
            </div>
            
            <div className="p-4 bg-purple-50 rounded-lg">
              <div className="text-3xl mb-2">🎯</div>
              <h3 className="font-semibold text-gray-800 mb-1">Konu Takibi</h3>
              <p className="text-sm text-gray-600">Hangi konularda eksiğiniz var öğrenin</p>
            </div>
            
            <div className="p-4 bg-green-50 rounded-lg">
              <div className="text-3xl mb-2">📈</div>
              <h3 className="font-semibold text-gray-800 mb-1">Gelişim Raporu</h3>
              <p className="text-sm text-gray-600">Haftalık ilerlemenizi görün</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

// Error State Component
function ErrorState({ error, onRetry, onAddTest }: { error: string; onRetry: () => void; onAddTest: () => void }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <Image src="/logo.png" alt="End.STP" width={40} height={40} />
            <span className="text-2xl font-bold text-gray-800">End.STP</span>
          </div>
        </div>
      </header>

      <main className="max-w-2xl mx-auto px-4 py-16">
        <div className="bg-white rounded-xl shadow-lg p-12 text-center">
          <div className="text-8xl mb-6">⚠️</div>
          <h2 className="text-3xl font-bold text-gray-800 mb-4">
            Bir Sorun Oluştu
          </h2>
          <p className="text-gray-600 mb-8 text-lg">
            {error}
          </p>
          
          <div className="flex gap-4 justify-center">
            <button
              onClick={onRetry}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition font-semibold"
            >
              🔄 Yeniden Dene
            </button>
            
            <button
              onClick={onAddTest}
              className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition font-semibold"
            >
              + Test Ekle
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}

// Main Dashboard Component
export default function Dashboard() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<DashboardData | null>(null);
  const [error, setError] = useState('');

  const fetchDashboard = async () => {
    setLoading(true);
    setError('');
    
    try {
      const userStr = localStorage.getItem('user');
      const accessToken = localStorage.getItem('access_token');
      
      if (!userStr || !accessToken) {
        router.push('/');
        return;
      }

      const user = JSON.parse(userStr);

      // DÜZELTİLMİŞ: Önce student bilgisini al
      const studentResponse = await fetch(`http://localhost:8000/api/user/${user.id}/student`, {
        headers: { 'Authorization': `Bearer ${accessToken}` }
      });

      if (!studentResponse.ok) {
        throw new Error('Öğrenci bilgisi bulunamadı');
      }

      const studentData = await studentResponse.json();
      
      // DÜZELTİLMİŞ: Doğru student ID'yi kullan
      const studentId = studentData.id; // BURASI ÖNEMLİ!

      // Dashboard verilerini al
      const dashboardResponse = await fetch(`http://localhost:8000/api/students/${studentId}/dashboard`, {
        headers: { 'Authorization': `Bearer ${accessToken}` }
      });

      if (!dashboardResponse.ok) {
        throw new Error('Dashboard verileri yüklenemedi');
      }

      const dashboardData = await dashboardResponse.json();
      setData(dashboardData);

    } catch (err: any) {
      console.error('Dashboard hatası:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboard();
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    router.push('/');
  };

  // Loading State
  if (loading) {
    return <DashboardSkeleton />;
  }

  // Error State
  if (error) {
    return (
      <ErrorState 
        error={error} 
        onRetry={fetchDashboard} 
        onAddTest={() => router.push('/test-entry')} 
      />
    );
  }

  // Empty State (hiç test yok)
  if (!data || !data.recent_tests || data.recent_tests.length === 0) {
    return <EmptyState onAddTest={() => router.push('/test-entry')} />;
  }

  // Main Dashboard (veriler var)
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <Image src="/logo.png" alt="End.STP" width={40} height={40} />
            <span className="text-2xl font-bold text-gray-800">End.STP</span>
          </div>
          
          <div className="flex items-center gap-4">
            <span className="text-gray-700">👤 {data.student.name}</span>
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
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 animate-fade-in">
          <div className="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 transform hover:scale-105">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm mb-1">Toplam Test</p>
                <p className="text-3xl font-bold text-blue-600">{data.recent_tests.length}</p>
              </div>
              <div className="text-4xl">📝</div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 transform hover:scale-105">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm mb-1">Güçlü Konular</p>
                <p className="text-3xl font-bold text-green-600">
                  {data.topic_performance?.filter((t: any) => t.mastery_level > 70).length || 0}
                </p>
              </div>
              <div className="text-4xl">✅</div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 transform hover:scale-105">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm mb-1">Sınıf</p>
                <p className="text-3xl font-bold text-purple-600">{data.student.class}</p>
              </div>
              <div className="text-4xl">🎓</div>
            </div>
          </div>
        </div>

        {/* Recent Tests */}
        <div className="bg-white rounded-xl shadow-md p-6 mb-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Son Testler</h2>
          
          <div className="space-y-4">
            {data.recent_tests.slice(0, 5).map((test: any) => (
              <div key={test.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition">
                <div className="flex items-center justify-between">
                  <div>
                    <span className="font-semibold text-gray-800">
                      {test.subject || 'Test'}
                    </span>
                    <p className="text-sm text-gray-500">
                      {test.entry_timestamp 
                        ? new Date(test.entry_timestamp).toLocaleDateString('tr-TR', {
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric',
                            hour: '2-digit',
                            minute: '2-digit'
                          })
                        : 'Tarih bilinmiyor'
                      }
                    </p>
                  </div>
                  <div className="text-right">
                    <span className="text-2xl font-bold text-gray-700">
                      {test.net?.toFixed(2) || '0.00'}
                    </span>
                    <p className="text-xs text-gray-500">net</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 animate-fade-in">
          <button 
            onClick={() => router.push('/test-entry')}
            className="bg-blue-600 text-white py-4 rounded-xl font-semibold text-lg hover:bg-blue-700 transition shadow-lg hover:shadow-xl transform hover:scale-105"
          >
            + Yeni Test Ekle
          </button>
          
          <button 
            onClick={() => router.push('/reports')}
            className="bg-purple-600 text-white py-4 rounded-xl font-semibold text-lg hover:bg-purple-700 transition shadow-lg hover:shadow-xl transform hover:scale-105"
          >
            📈 Raporları Görüntüle
          </button>
        </div>
      </main>
    </div>
  );
}