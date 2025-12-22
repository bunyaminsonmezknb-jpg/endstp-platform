'use client';

import { useState, useEffect, useRef } from 'react';
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
  const [firstVisit, setFirstVisit] = useState(true);
  const [showTooltip, setShowTooltip] = useState(false);
  const tooltipRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const hasVisited = localStorage.getItem('progress_guide_seen');
    if (hasVisited) {
      setFirstVisit(false);
    }
  }, []);

  // Outside click handler
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (tooltipRef.current && !tooltipRef.current.contains(event.target as Node)) {
        setShowTooltip(false);
      }
    };

    if (showTooltip) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [showTooltip]);

  const dismissBanner = () => {
    setFirstVisit(false);
    localStorage.setItem('progress_guide_seen', 'true');
  };

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
    <div>
      {/* İlk Ziyaret Banner */}
      {firstVisit && (
        <div className="bg-blue-50 border-l-4 border-blue-500 p-4 mb-6 rounded-r-lg">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-blue-500" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3 flex-1">
              <p className="text-sm text-blue-700">
                <strong>Sistem şu an başlangıç modunda.</strong> 0-5 test arası sadece test başarısı ölçülür. 
                5+ test girince kapsam, 15+ test girince ustalık oranı da eklenecek.
              </p>
              <button 
                onClick={dismissBanner}
                className="mt-2 text-sm text-blue-600 underline hover:text-blue-800"
              >
                Anladım, gösterme
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Başlık + Tooltip */}
      <div className="flex items-center gap-3 mb-6 relative">
        <h2 className="text-xl font-bold text-gray-900">📊 Ders Bazlı İlerleme</h2>
        
        <button 
          onClick={() => setShowTooltip(!showTooltip)}
          className="text-gray-400 hover:text-purple-600 transition-colors"
          title="Nasıl okunur?"
        >
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z" clipRule="evenodd" />
          </svg>
        </button>

        {/* Tooltip */}
        {showTooltip && (
          <div 
            ref={tooltipRef}
            className="absolute top-8 right-0 w-full max-w-2xl bg-white shadow-2xl rounded-lg p-6 z-50 border border-gray-200"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-bold text-lg text-gray-900">📖 Bu Sayfa Nasıl Okunur?</h3>
              <button 
                onClick={() => setShowTooltip(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <div className="space-y-4 text-sm">
              {/* İlerleme Sistemi */}
              <div>
                <div className="font-semibold text-purple-600 mb-2 flex items-center gap-2">
                  <span>🎯</span>
                  <span>İlerleme Sistemi (3 Aşama)</span>
                </div>
                <ul className="space-y-1.5 text-gray-600 ml-6">
                  <li>• <strong>0-5 test:</strong> Test başarısı (başlangıç - motivasyonel)</li>
                  <li>• <strong>5-15 test:</strong> Başarı + Kapsam (gelişim dönemi)</li>
                  <li>• <strong>15+ test:</strong> Başarı + Kapsam + Ustalık (olgunluk)</li>
                </ul>
              </div>
              
              {/* Trend */}
              <div>
                <div className="font-semibold text-green-600 mb-2 flex items-center gap-2">
                  <span>📈</span>
                  <span>Akıllı Trend Göstergeleri</span>
                </div>
                <ul className="space-y-1.5 text-gray-600 ml-6">
                  <li>🔥 <strong>Hızlanıyor:</strong> Kalan gelişim alanına göre anlamlı artış</li>
                  <li>→ <strong>Sabit:</strong> Performans dengeli</li>
                  <li>🔻 <strong>Düşüyor:</strong> Anlamlı gerileme</li>
                  <li className="text-xs text-gray-500 ml-4">* En az 3 test gerekir</li>
                  <li className="text-xs text-purple-600 ml-4">💡 Düşük başarıda büyük, yüksek başarıda küçük değişimler anlamlıdır</li>
                </ul>
              </div>
              
              {/* Ustalık */}
              <div>
                <div className="font-semibold text-blue-600 mb-2 flex items-center gap-2">
                  <span>🏆</span>
                  <span>Ustalık Seviyeleri</span>
                </div>
                <ul className="space-y-1.5 text-gray-600 ml-6">
                  <li>🏆 <strong>Evrensel:</strong> %80+ başarı, 2+ test (objektif)</li>
                  <li>🧠 <strong>Kişisel Güçlü:</strong> Kendi ortalamanın üstü (motivasyonel)</li>
                </ul>
              </div>
              
              {/* İpucu */}
              <div className="bg-purple-50 p-3 rounded-lg border border-purple-100">
                <p className="text-xs text-purple-800">
                  <strong>💡 İpucu:</strong> Sistem test sayısı arttıkça daha gelişmiş hesaplamalar yapar. 
                  %98'deki +1 puan, %20'deki +5 puan kadar değerlidir!
                </p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Subject List */}
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

              <div className="text-right" space-y-1>
              <div className="text-2xl font-bold text-gray-900">
                {subject.progress_percentage}%
              </div>
              {subject.test_count && subject.test_count >= 3 ? (
                <div className="flex items-center gap-1 text-sm text-gray-500 justify-end">
                  {getTrendIcon(subject.trend)}
                  <span>{getTrendLabel(subject.trend)}</span>
                </div>
              ) : (
                <div className="h-6"></div>
              )}
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

            {/* Trend & Ustalık - SADECE İÇERİK VARSA GÖSTER */}
            {((subject.test_count && subject.test_count >= 3 && subject.trend_icon) || 
              subject.topics_mastered > 0 || 
              subject.topics_mastered_personal > 0) && (
              <div className="flex items-center justify-between mb-3 text-sm">
                {/* Trend (3+ test varsa) */}
                {subject.test_count && subject.test_count >= 3 && subject.trend_icon && (
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
                
                {/* Ustalık */}
                {(subject.topics_mastered > 0 || subject.topics_mastered_personal > 0) && (
                  <div className="flex items-center gap-2 text-xs ml-auto">
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
                )}
              </div>
            )}

            {/* Disclaimer */}
            {subject.disclaimer && (
              <div className={`mb-3 text-xs px-3 py-2 rounded-lg ${
                subject.phase === 'no_data' 
                  ? 'text-gray-600 bg-gray-50' 
                  : 'text-blue-600 bg-blue-50'
              }`}>
                💡 {subject.disclaimer}
              </div>
            )}

            {/* Stats */}
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
    </div>
  );
}

export default SubjectProgressList;