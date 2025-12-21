'use client';

import SubjectIcon from '@/components/SubjectIcon';

interface SubjectProgress {
  subject_id: string;
  subject_name: string;
  subject_code: string;
  progress_percentage: number;
  topics_total: number;
  topics_mastered: number;
  topics_mastered_personal: number;
  topics_in_progress: number;
  topics_not_started: number;
  avg_success_rate: number;
  trend: string;
  trend_icon?: string;
  test_count?: number;
  phase?: string;
  disclaimer?: string;
}

interface SubjectProgressListProps {
  subjects: SubjectProgress[] | null;
  isLoading?: boolean;
}

function SubjectProgressList({ subjects, isLoading = false }: SubjectProgressListProps) {
  if (isLoading || !subjects) {
    return (
      <div className="space-y-4">
        {[1, 2, 3].map((i) => (
          <div key={i} className="border border-gray-100 rounded-lg p-4 animate-pulse">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 bg-gray-200 rounded-lg"></div>
                <div>
                  <div className="h-5 bg-gray-200 rounded w-32 mb-2"></div>
                  <div className="h-4 bg-gray-200 rounded w-24"></div>
                </div>
              </div>
              <div className="h-8 bg-gray-200 rounded w-16"></div>
            </div>
            <div className="h-2 bg-gray-200 rounded-full mb-3"></div>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="h-4 bg-gray-200 rounded w-20"></div>
                <div className="h-4 bg-gray-200 rounded w-24"></div>
                <div className="h-4 bg-gray-200 rounded w-20"></div>
              </div>
              <div className="h-4 bg-gray-200 rounded w-16"></div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (subjects.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg className="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
        </div>
        <p className="text-gray-500 text-lg">Henüz test girişi yapılmamış</p>
      </div>
    );
  }

  const getTrendIcon = (trend: string) => {
    if (trend === 'improving') {
      return (
        <svg className="w-4 h-4 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
        </svg>
      );
    } else if (trend === 'declining') {
      return (
        <svg className="w-4 h-4 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
        </svg>
      );
    }
    return (
      <svg className="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14" />
      </svg>
    );
  };

  const getProgressColor = (percentage: number) => {
    if (percentage >= 70) return 'bg-green-500';
    if (percentage >= 40) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const getTrendLabel = (trend: string) => {
    if (trend === 'improving') return 'Gelişiyor';
    if (trend === 'declining') return 'Düşüyor';
    return 'Sabit';
  };

  return (
    <div className="space-y-5">
      {subjects.map((subject) => (
        <div key={subject.subject_id} className="border border-gray-100 rounded-lg p-4 hover:shadow-md transition-shadow bg-white">
          <div className="flex items-start justify-between mb-3">
            <div className="flex items-center gap-3">
              <SubjectIcon 
                subjectCode={subject.subject_code}
                size="md"
                showBadge={true}
              />
              
            <div>
              <h3 className="font-semibold text-gray-900">{subject.subject_name}</h3>
              <p className="text-sm text-gray-500">
                {subject.topics_in_progress}/{subject.topics_total} konuya başlandı
              </p>
            </div>
            </div>

            <div className="text-right">
              <div className="text-2xl font-bold text-gray-900">
                {subject.progress_percentage}%
              </div>
              <div className="flex items-center gap-1 text-sm text-gray-500">
                {getTrendIcon(subject.trend)}
                <span>{getTrendLabel(subject.trend)}</span>
              </div>
            </div>
          </div>

          {/* Progress bar */}
          <div className="mb-3">
            <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
              <div 
                className={`h-full ${getProgressColor(subject.progress_percentage)} transition-all duration-500`}
                style={{ width: `${subject.progress_percentage}%` }}
              ></div>
            </div>
          </div>

          {/* ✅ YENİ: Trend & Ustalık */}
          <div className="flex items-center justify-between mb-3 text-sm">
            {/* Trend */}
            {subject.trend_icon && (
              <div className={`flex items-center gap-1 ${
                subject.trend === 'improving' ? 'text-green-600' :
                subject.trend === 'declining' ? 'text-orange-600' :
                'text-gray-500'
              }`}>
                <span className="text-base">{subject.trend_icon}</span>
                <span className="font-medium">
                  {subject.trend === 'improving' ? 'Hızlanıyor' :
                  subject.trend === 'declining' ? 'Yavaşlıyor' :
                  'Sabit'}
                </span>
              </div>
            )}
            
            {/* Ustalık (sadece varsa göster) */}
            <div className="flex items-center gap-2 text-xs">
              {subject.topics_mastered > 0 && (
                <span className="text-green-600 font-medium">
                  🏆 {subject.topics_mastered} evrensel
                </span>
              )}
              {subject.topics_mastered_personal > 0 && (
                <span className="text-purple-600 font-medium">
                  🧠 {subject.topics_mastered_personal} kişisel
                </span>
              )}
            </div>
          </div>

          {/* Disclaimer */}
          {subject.phase === 'early' && subject.disclaimer && (
            <div className="mb-3 text-xs text-blue-600 bg-blue-50 px-3 py-2 rounded-lg">
              💡 {subject.disclaimer}
            </div>
          )}

          {/* Stats row - Sadece konu dağılımı ve ortalama */}
          <div className="flex items-center justify-between text-sm">
            <div className="flex items-center gap-4">
              <span className="text-blue-600 font-medium">
                📚 {subject.topics_in_progress} aktif
              </span>
              <span className="text-gray-400">
                ⚪ {subject.topics_not_started} başlanmadı
              </span>
            </div>
            <span className="text-gray-600 font-medium">
              Ort: %{Math.round(subject.avg_success_rate)}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}

export default SubjectProgressList;