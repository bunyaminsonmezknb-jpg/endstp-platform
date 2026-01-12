'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useStudentDashboard } from '@/lib/store/studentDashboardStore';
import DashboardHeader from './components/DashboardHeader';
import CriticalAlert from './components/CriticalAlert';
import HeroStats from './components/HeroStats';
import ActionCards from './components/ActionCards';
import TopicHealthBar from './components/TopicHealthBar';

export default function StudentDashboard() {
  const router = useRouter();
  const { dashboardData, isLoading, error, fetchDashboardData } = useStudentDashboard();

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

        <button className="fixed bottom-5 right-5 w-16 h-16 bg-gradient-to-br from-purple-600 to-purple-800 rounded-full flex items-center justify-center text-white text-3xl shadow-2xl hover:scale-110 transition-transform">
          💬
        </button>
      </div>
    </div>
  );
}
