'use client';
import FeedbackWidget from '@/app/components/FeedbackWidget';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useStudentDashboard } from '@/lib/store/studentDashboardStore';
import { api } from '@/lib/api/client';
import DashboardHeader from './components/DashboardHeader';
import CriticalAlert from './components/CriticalAlert';
import HeroStats from './components/HeroStats';
import ProjectionCard from './components/ProjectionCard';
import UniversityGoalCard from './components/UniversityGoalCard';
import SmartActionCards from './components/SmartActionCards';
import TopicHealthBar from './components/TopicHealthBar';
import HealthStatusBar from './components/HealthStatusBar';
import MotorAnalysisPanel from './components/MotorAnalysisPanel';
import TodayStatusCards from './components/TodayStatusCards';

/**
 * Student Dashboard - v4
 * 
 * TAB'LAR:
 * - 📊 Genel Bakış (Projection + HeroStats + Health Bars)
 * - 🚀 4 Motor Analizi
 * - 🎯 Bugünkü Görevler (TodayStatusCards)
 */

export default function StudentDashboard() {
  const router = useRouter();
  const { dashboardData, isLoading, error, fetchDashboardData } = useStudentDashboard();
  const [activeTab, setActiveTab] = useState<'overview' | 'motors' | 'tasks'>('overview');
  const [tasksSummary, setTasksSummary] = useState({
    total_tasks: 5,
    completed_tasks: 0,
    total_time_minutes: 0,
    completed_time_minutes: 0,
    remaining_time_minutes: 0
  });
  const [tasksList, setTasksList] = useState([]);
 const [weeklySubjects, setWeeklySubjects] = useState({
  worst_subjects: [],
  best_subjects: [],
  all_subjects: []
});
 useEffect(() => {
    const userStr = localStorage.getItem('user');
    const accessToken = localStorage.getItem('access_token');
    
    if (!userStr || !accessToken) {
      router.push('/login');
      return;
    }

// Initialize timezone
const user = JSON.parse(userStr);
fetchDashboardData(user.id);
  }, [router]);
useEffect(() => {
  const fetchTasks = async () => {
    try {
      const data = await api.get('/student/tasks/today') as any;
      if (data.success && data.summary) {
        setTasksSummary(data.summary);
        setTasksList(data.tasks || []);
      }
    } catch (err) {
      console.error('Tasks summary fetch error:', err);
    }
  };
  
  fetchTasks(); // İlk yükleme
  
  // 30 saniyede bir yenile
  const interval = setInterval(fetchTasks, 30000);
  
  return () => clearInterval(interval); // Cleanup
  }, []);
  useEffect(() => {
  const fetchWeeklySubjects = async () => {
    try {
      const data = await api.get('/student/weekly-subjects') as any;
      if (data.success) {
        setWeeklySubjects(data);
      }
    } catch (err) {
      console.error('Weekly subjects fetch error:', err);
    }
  };
    fetchWeeklySubjects();
  }, []);
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
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
<div className="min-h-screen p-6">
  <div className="max-w-[1280px] mx-auto">
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

          <button
            onClick={() => setActiveTab('tasks')}
            className={`flex-1 py-3 px-6 rounded-xl font-semibold transition-all ${
              activeTab === 'tasks'
                ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow-lg'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <span className="text-xl mr-2">🎯</span>
            Bugünkü Görevler
            <span className="ml-2 bg-orange-500 text-white text-xs px-2 py-1 rounded-full">YENİ</span>
          </button>
        </div>

        {/* TAB CONTENT */}
        {activeTab === 'overview' ? (
          <>
            {/* YENİ LAYOUT - GENEL BAKIŞ */}
            <div className="bg-green-500 text-white text-sm px-4 py-2 rounded-lg mb-3 flex items-center gap-2 w-fit ml-auto shadow-md">
              <span className="animate-pulse">🟢</span>
              <span className="font-semibold">Canlı Veri (Gerçek Backend API)</span>
            </div>

            {/* ACİL UYARI (Varsa) */}
            {dashboardData.criticalAlert && dashboardData.criticalAlert.show && (
              <CriticalAlert
                topicName={dashboardData.criticalAlert.topicName}
                daysAgo={dashboardData.criticalAlert.daysAgo}
                forgetRisk={dashboardData.criticalAlert.forgetRisk}
              />
            )}

            {/* ÜST ALAN: Projection + University Goal (2'li) */}
            {dashboardData.projection && (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 mb-6">
                <ProjectionCard />
                <UniversityGoalCard />
              </div>
            )}

            {/* BUGÜNKÜ DURUM (3'lü Kartlar) */}
            <HeroStats
              dailyGoal={{
                current: tasksSummary.completed_tasks,
                target: tasksSummary.total_tasks
              }}
              weeklySuccess={dashboardData.weeklySuccess}
              weeklyTarget={dashboardData.weeklyTarget}
              studyTimeToday={tasksSummary.completed_time_minutes}
              weeklyQuestions={dashboardData.weeklyQuestions}
              weeklyIncrease={dashboardData.weeklyIncrease}
              tasksList={tasksList} // ✅ BUNU EKLE
              weeklySubjects={weeklySubjects} // ✅ BUNU EKLE

            />

            {/* SMART ACTION CARDS (4 Motor Önerisi) */}
            <SmartActionCards />

            {/* BİLGİ SAĞLIĞI BAR */}
            {dashboardData.topics.length > 0 ? (
              <HealthStatusBar
                totalTopics={dashboardData.topics.length}
                healthyTopics={dashboardData.topics.filter(t => t.status === 'excellent' || t.status === 'good').length}
                warningTopics={dashboardData.topics.filter(t => t.status === 'warning').length}
                frozenTopics={dashboardData.topics.filter(t => t.status === 'frozen').length}
                criticalTopics={dashboardData.topics.filter(t => t.status === 'critical').length}
                currentlyShown={dashboardData.topics.length}
              />
            ) : (
              <div className="bg-white rounded-2xl p-6 shadow-lg mb-6 text-center">
                <p className="text-gray-500 text-lg">📝 Henüz test eklenmedi. İlk testinizi ekleyerek başlayın!</p>
              </div>
            )}

            {/* TOPIC HEALTH BARS */}
            <TopicHealthBar topics={dashboardData.topics} />

            {/* PERFORMANS TRENDİ (Placeholder) */}
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
        ) : activeTab === 'motors' ? (
          <>
            {/* 4 MOTOR ANALİZİ */}
            <div className="bg-gradient-to-r from-green-500 to-emerald-600 text-white text-sm px-4 py-2 rounded-lg mb-3 flex items-center gap-2 w-fit ml-auto shadow-md">
              <span className="animate-pulse">🟢</span>
              <span className="font-semibold">4 Motor Sistemi (POST /api/v1/student/analyze)</span>
            </div>

            <MotorAnalysisPanel />
          </>
        ) : (
          <>
            {/* BUGÜNKÜ GÖREVLER TAB */}
            <div className="bg-orange-500 text-white text-sm px-4 py-2 rounded-lg mb-3 flex items-center gap-2 w-fit ml-auto shadow-md">
              <span className="animate-pulse">🟢</span>
              <span className="font-semibold">Canlı Veri (GET /api/v1/student/todays-tasks)</span>
            </div>

            <TodayStatusCards />
          </>
        )}

{/* FEEDBACK WIDGET */}
        <FeedbackWidget />
      </div>
    </div>
  );
}