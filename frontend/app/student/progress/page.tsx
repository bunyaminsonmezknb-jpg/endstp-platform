'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '@/lib/api/client';

import ProjectionCard from '../dashboard/components/ProjectionCard';
import UniversityGoalCard from '../dashboard/components/UniversityGoalCard';
import ProgressTrendChart from './components/ProgressTrendChart';
import SubjectProgressList from './components/SubjectProgressList';
import ProgressSkeleton from './components/ProgressSkeleton';

/**
 * İlerleme & Hedefler Sayfası
 *
 * SORUMLULUKLAR:
 * - Layout
 * - Data orchestration
 * - Error & loading state
 *
 * AUTH:
 * - Supabase session → api-client içinde
 * - 401 → login redirect
 */

// ==================== TYPES ====================

interface ProgressData {
  subjects: any[] | null;
  trends: {
    weekly: any | null;
    monthly: any | null;
  };
}

// ==================== MAIN PAGE ====================

export default function ProgressPage() {
  const router = useRouter();

  const [isLoading, setIsLoading] = useState(true);
  const [data, setData] = useState<ProgressData>({
    subjects: null,
    trends: { weekly: null, monthly: null },
  });
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // ==================== DATA LOAD ====================

  async function loadData() {
    try {
      setIsLoading(true);
      setError(null);

      /**
       * ✅ Paralel fetch
       * Auth + token otomatik → api-client
       */
      const [subjects, weekly, monthly] = await Promise.all([
        api.get<any>('/student/progress/subjects'),
        api.get<any>('/student/progress/trends?period=weekly'),
        api.get<any>('/student/progress/trends?period=monthly'),
      ]);

      setData({
        subjects: subjects?.data ?? null,
        trends: {
          weekly: weekly?.data ?? null,
          monthly: monthly?.data ?? null,
        },
      });
      } 
      catch (err: any) {
        if (err?.code === 'SESSION_NOT_READY') return;

        if (err?.status === 401) {
          router.push('/login');
          return;
        }

        console.error('Progress data load error:', err);
        setError('Veriler yüklenirken hata oluştu');
      }


    finally {
      setIsLoading(false);
    }
  }

  // ==================== STATES ====================

  if (isLoading && !data.subjects) {
    return <ProgressSkeleton />;
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

        {/* ERROR */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-xl p-6 mb-6">
            <p className="text-red-600 font-semibold mb-2">❌ {error}</p>
            <button
              onClick={loadData}
              className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
            >
              Tekrar Dene
            </button>
          </div>
        )}


        {/* PROJECTION & GOAL */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <ProjectionCard />
          <UniversityGoalCard />
        </div>

        {/* TREND CHART */}
        <div className="bg-white rounded-3xl p-8 shadow-lg mb-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">
            📊 İlerleme Trendi
          </h2>
          <ProgressTrendChart
            weeklyData={data.trends.weekly}
            monthlyData={data.trends.monthly}
            isLoading={isLoading}
          />
        </div>

        {/* SUBJECT BREAKDOWN */}
        <div className="bg-white rounded-3xl p-8 shadow-lg">
          <SubjectProgressList
            subjects={data.subjects}
            isLoading={isLoading}
          />
        </div>
      </div>
    </div>
  );
}
