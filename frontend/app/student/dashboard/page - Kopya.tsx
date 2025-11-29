'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useStudentDashboard } from '@/lib/store/studentDashboardStore';
import DashboardHeader from './components/DashboardHeader';
import CriticalAlert from './components/CriticalAlert';
import HeroStats from './components/HeroStats';
import ActionCards from './components/ActionCards';
import TopicHealthBar from './components/TopicHealthBar';
import MotorAnalysisPanel from './components/MotorAnalysisPanel';

/**
 * Student Dashboard - TAB SİSTEMLİ
 * 
 * [Genel Bakış] [4 Motor Analizi]
 *      ↓              ↓
 *   Mevcut         Yeni 4
 *   Dashboard      Motorlu
 */

export default function StudentDashboard() {
  const router = useRouter();
  const { dashboardData, isLoading, error, fetchDashboardData } = useStudentDashboard();
  const [activeTab, setActiveTab] = useState<'overview' | 'motors'>('overview');

  useEffect(() => {
    const userStr = localStorage.getItem('user');
    const accessToken = localStorage.getItem('access_token');
    
    if (!userStr || !accessToken) {
      router.push('/login');
      return;
    }

    const user = JSON.parse(userStr);
    fetchDashboardData(user.id);
  }, [router]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-200 via-purple-100 to-blue-200 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-purple-600 mx-auto mb-4"></div>
          <p className="text-gray-700 text-xl mb-2 font-semibold">⏳ Dashboard yükleniyor...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-200 via-purple-100 to-blue-200 flex items-center justify-center">
        <div className="bg-white rounded-3xl p-8 max-w-md text-center shadow-2xl">
          <div className="text-6xl mb-4">⚠️</div>
          <h2 className="text-2xl font-bold text-red-600 mb-2">Bağlantı Hatası</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700"
          >
            Tekrar Dene
          </button>
        </div>
      </div>
    );
  }

  if (!dashboardData) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-200 via-purple-100 to-blue-200 p-5">
      <div className="max-w-7xl mx-auto">
        <DashboardHeader
          studentName={dashboardData.studentName}
          streak={dashboardData.streak}
        />

        {/* TAB NAVIGATION */}
        <div className="bg-white rounded-2xl shadow-lg p-2 mb-5 flex gap-2">
          <button
            onClick={() => setActiveTab('overview')}
            className={`flex-1 py-3 px-6 rounded-xl font-semibold transition-all ${
              activeTab === 'overview'
                ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow-lg'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <span className="text-xl mr-2">📊</span>
            Genel Bakış
          </button>
          <button
            onClick={() => setActiveTab('motors')}
            className={`flex-1 py-3 px-6 rounded-xl font-semibold transition-all ${
              activeTab === 'motors'
                ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow-lg'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <span className="text-xl mr-2">🚀</span>
            4 Motor Analizi
            <span className="ml-2 bg-green-500 text-white text-xs px-2 py-1 rounded-full">YENİ</span>
          </button>
        </div>

        {/* TAB CONTENT */}
        {activeTab === 'overview' ? (
          <>
            {/* ESKİ SİSTEM - GENEL BAKIŞ */}
            <div className="bg-green-500 text-white text-sm px-4 py-2 rounded-lg mb-3 flex items-center gap-2 w-fit ml-auto shadow-md">
              <span className="animate-pulse">🟢</span>
              <span className="font-semibold">Canlı Veri (Gerçek Backend API)</span>
            </div>

            {dashboardData.criticalAlert && dashboardData.criticalAlert.show && (
              <CriticalAlert
                topicName={dashboardData.criticalAlert.topicName}
                daysAgo={dashboardData.criticalAlert.daysAgo}
                forgetRisk={dashboardData.criticalAlert.forgetRisk}
              />
            )}

            <HeroStats
              dailyGoal={dashboardData.dailyGoal}
              weeklySuccess={dashboardData.weeklySuccess}
              weeklyTarget={dashboardData.weeklyTarget}
              studyTimeToday={dashboardData.studyTimeToday}
              weeklyQuestions={dashboardData.weeklyQuestions}
              weeklyIncrease={dashboardData.weeklyIncrease}
              projection={dashboardData.projection}
            />

            <ActionCards />

            <TopicHealthBar topics={dashboardData.topics} />

            <div className="bg-white rounded-3xl p-8 shadow-lg mt-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-6">
                📈 Son 30 Gün Performans Trendi
              </h2>
              <div className="h-72 bg-gradient-to-b from-gray-50 to-white rounded-xl flex flex-col items-center justify-center text-gray-400">
                <div className="text-6xl mb-4">📊</div>
                <div className="text-lg">Grafik buraya gelecek (Chart.js veya Recharts ile)</div>
              </div>
            </div>
          </>
        ) : (
          <>
            {/* YENİ SİSTEM - 4 MOTOR ANALİZİ */}
            <div className="bg-gradient-to-r from-green-500 to-emerald-600 text-white text-sm px-4 py-2 rounded-lg mb-3 flex items-center gap-2 w-fit ml-auto shadow-md">
              <span className="animate-pulse">🟢</span>
              <span className="font-semibold">4 Motor Sistemi (POST /api/v1/student/analyze)</span>
            </div>

            <MotorAnalysisPanel />
          </>
        )}

        <button className="fixed bottom-5 right-5 w-16 h-16 bg-gradient-to-br from-purple-600 to-purple-800 rounded-full flex items-center justify-center text-white text-3xl shadow-2xl hover:scale-110 transition-transform">
          💬
        </button>
      </div>
    </div>
  );
}
