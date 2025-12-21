'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import ProjectionCard from '../dashboard/components/ProjectionCard';
import UniversityGoalCard from '../dashboard/components/UniversityGoalCard';

/**
 * İlerleme & Hedefler Sayfası
 * 
 * - Tahmini Bitiriş Tarihi (Projection)
 * - Üniversite Hedef Tracking
 * - Haftalık/Aylık İlerleme Grafikleri
 * 
 * Sol menüden erişilebilir
 */

export default function ProgressPage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const userStr = localStorage.getItem('user');
    const accessToken = localStorage.getItem('access_token');
    
    if (!userStr || !accessToken) {
      router.push('/login');
      return;
    }

    setIsLoading(false);
  }, [router]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-purple-600 mx-auto mb-4"></div>
          <p className="text-gray-700 text-xl mb-2 font-semibold">⏳ Yükleniyor...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-[1280px] mx-auto">
        {/* HEADER */}
        <div className="mb-8">
          <button
            onClick={() => router.push('/student/dashboard')}
            className="text-gray-600 hover:text-gray-900 mb-4 flex items-center gap-2 transition-colors"
          >
            <span>←</span>
            <span className="font-medium">Dashboard'a Dön</span>
          </button>
          
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            📈 İlerleme & Hedefler
          </h1>
          <p className="text-gray-600 text-lg">
            Tahmini bitiriş tarihin, üniversite hedefin ve genel ilerleme durumun
          </p>
        </div>

        {/* PROJECTION & GOAL CARDS */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <ProjectionCard />
          <UniversityGoalCard />
        </div>

        {/* WEEKLY PROGRESS SECTION */}
        <div className="bg-white rounded-3xl p-8 shadow-lg mb-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">
            📊 Haftalık İlerleme
          </h2>
          <div className="h-72 bg-gradient-to-b from-gray-50 to-white rounded-xl flex flex-col items-center justify-center text-gray-400">
            <div className="text-6xl mb-4">📈</div>
            <div className="text-lg">Haftalık ilerleme grafiği (Chart.js)</div>
          </div>
        </div>

        {/* MONTHLY PROGRESS SECTION */}
        <div className="bg-white rounded-3xl p-8 shadow-lg mb-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">
            📅 Aylık İlerleme
          </h2>
          <div className="h-72 bg-gradient-to-b from-gray-50 to-white rounded-xl flex flex-col items-center justify-center text-gray-400">
            <div className="text-6xl mb-4">📊</div>
            <div className="text-lg">Aylık ilerleme grafiği (Recharts)</div>
          </div>
        </div>

        {/* SUBJECT BREAKDOWN */}
        <div className="bg-white rounded-3xl p-8 shadow-lg">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">
            📚 Ders Bazlı İlerleme
          </h2>
          <div className="space-y-4">
            {/* Placeholder - Backend'den gelecek */}
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center text-2xl">
                  📐
                </div>
                <div>
                  <div className="font-semibold text-gray-900">Matematik</div>
                  <div className="text-sm text-gray-600">120 konu • %68 tamamlandı</div>
                </div>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-purple-600">68%</div>
                <div className="text-xs text-gray-500">İlerleme</div>
              </div>
            </div>

            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center text-2xl">
                  ⚗️
                </div>
                <div>
                  <div className="font-semibold text-gray-900">Fizik</div>
                  <div className="text-sm text-gray-600">85 konu • %45 tamamlandı</div>
                </div>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-blue-600">45%</div>
                <div className="text-xs text-gray-500">İlerleme</div>
              </div>
            </div>

            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center text-2xl">
                  🧪
                </div>
                <div>
                  <div className="font-semibold text-gray-900">Kimya</div>
                  <div className="text-sm text-gray-600">92 konu • %52 tamamlandı</div>
                </div>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-green-600">52%</div>
                <div className="text-xs text-gray-500">İlerleme</div>
              </div>
            </div>

            <div className="text-center pt-4">
              <p className="text-gray-500 text-sm">
                💡 Gerçek veri backend'den gelecek
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}