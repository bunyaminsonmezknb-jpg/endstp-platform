'use client';

import { useState, useRef, useEffect } from 'react';

interface Subject {
  subject_id: string;
  subject_name: string;
  progress_percentage: number;
  test_count: number;
  topics_total: number;
  topics_tested: number;
  topics_mastered: number;
  topics_mastered_personal: number;
  avg_success_rate: number;
  trend: string;
  trend_icon: string;
  phase: string;
  disclaimer: string | null;
  last_test_date: string | null;
}

interface SubjectProgressListProps {
  subjects: Subject[] | null;
  isLoading: boolean;
}

// ===== DERS İKONLARI (SUBJECT-SPECIFIC) =====
function getSubjectIcon(subjectName: string): string {
  const name = subjectName.toLowerCase();
  
  if (name.includes('matematik')) return '📐';
  if (name.includes('fizik')) return '⚡';
  if (name.includes('kimya')) return '⚗️';
  if (name.includes('biyoloji')) return '🧬';
  if (name.includes('tarih')) return '📜';
  if (name.includes('coğrafya')) return '🌍';
  if (name.includes('edebiyat')) return '📖';
  if (name.includes('türkçe')) return '🇹🇷';
  if (name.includes('din')) return '☪️';
  if (name.includes('felsefe')) return '🤔';
  if (name.includes('geometri')) return '📏';
  if (name.includes('ingilizce') || name.includes('İngilizce')) return '🇬🇧';
  
  return '📚'; // Default
}

// ===== GÜÇLENDİRİLMİŞ RİSK SKORU (4 MOTOR PRENSİBİ) =====
function calculatePriorityScore(subject: Subject): number {
  let score = 0;
  
  // ✅ MOTOR 1: ÖNCELİK (Risk/Aciliyet) - %45 ağırlık
  const priorityScore = (() => {
    let p = 0;
    
    // Düşük başarı = yüksek risk
    if (subject.progress_percentage < 30) p += 50;
    else if (subject.progress_percentage < 50) p += 35;
    else if (subject.progress_percentage < 70) p += 20;
    
    // Trend durumu
    if (subject.trend === 'declining') p += 40;
    else if (subject.trend === 'stable') p += 15;
    
    // Az test = belirsizlik
    if (subject.test_count < 3) p += 15;
    else if (subject.test_count < 5) p += 8;
    
    return p;
  })();
  
  score += priorityScore * 0.45;
  
  // ✅ MOTOR 2: TEKRAR RİSKİ (Unutma eğrisi) - %25 ağırlık
  const reviewScore = (() => {
    if (!subject.last_test_date) return 60; // Hiç test yok
    
    const daysSinceTest = Math.floor(
      (new Date().getTime() - new Date(subject.last_test_date).getTime()) / (1000 * 60 * 60 * 24)
    );
    
    if (daysSinceTest > 21) return 50; // 3+ hafta
    if (daysSinceTest > 14) return 35; // 2+ hafta
    if (daysSinceTest > 7) return 20; // 1+ hafta
    return 5; // Güncel
  })();
  
  score += reviewScore * 0.25;
  
  // ✅ MOTOR 3: MOMENTUM (Trend + aktivite) - %20 ağırlık
  const momentumScore = (() => {
    let m = 0;
    
    // Trend yönü
    if (subject.trend === 'declining') m += 40;
    else if (subject.trend === 'stable') m += 20;
    else if (subject.trend === 'improving') m += 5;
    
    // Test sıklığı (aktivite)
    if (subject.test_count < 2) m += 30;
    else if (subject.test_count < 5) m += 15;
    
    return m;
  })();
  
  score += momentumScore * 0.20;
  
  // ✅ MOTOR 4: ÖĞRENME ZORLUĞU (Kapsam vs başarı) - %10 ağırlık
  const difficultyScore = (() => {
    const coverage = (subject.topics_tested / subject.topics_total) * 100;
    
    // Düşük kapsam + düşük başarı = zor ders
    if (coverage < 30 && subject.avg_success_rate < 50) return 40;
    if (coverage < 50 && subject.avg_success_rate < 60) return 25;
    if (subject.avg_success_rate < 50) return 15;
    
    return 5;
  })();
  
  score += difficultyScore * 0.10;
  
  return Math.round(score);
}

// ===== TREND EMOJI & TEXT =====
function getTrendDisplay(trend: string) {
  switch(trend) {
    case 'improving':
      return { emoji: '📈', text: 'Yükseliyor', color: 'text-green-700', bg: 'bg-green-50' };
    case 'declining':
      return { emoji: '📉', text: 'Düşüyor', color: 'text-red-700', bg: 'bg-red-50' };
    case 'stable':
      return { emoji: '➡️', text: 'Sabit', color: 'text-blue-700', bg: 'bg-blue-50' };
    default:
      return { emoji: '⏸️', text: 'Belirsiz', color: 'text-gray-700', bg: 'bg-gray-50' };
  }
}

export default function SubjectProgressList({ subjects, isLoading }: SubjectProgressListProps) {
  const [expandedSubjects, setExpandedSubjects] = useState<Set<string>>(new Set());
  const [showTooltip, setShowTooltip] = useState(false);
  const tooltipRef = useRef<HTMLDivElement>(null);

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
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [showTooltip]);

  // İlk render: En kritik dersi aç
  useEffect(() => {
    if (subjects && subjects.length > 0 && expandedSubjects.size === 0) {
      const sortedByPriority = [...subjects].sort((a, b) => 
        calculatePriorityScore(b) - calculatePriorityScore(a)
      );
      setExpandedSubjects(new Set([sortedByPriority[0].subject_id]));
    }
  }, [subjects]);

  // Toggle expand
  const toggleExpand = (subjectId: string) => {
    setExpandedSubjects(prev => {
      const newSet = new Set(prev);
      if (newSet.has(subjectId)) {
        newSet.delete(subjectId);
      } else {
        newSet.add(subjectId);
      }
      return newSet;
    });
  };

  if (isLoading) {
    return (
      <div className="space-y-4">
        {[1, 2, 3].map(i => (
          <div key={i} className="animate-pulse">
            <div className="h-16 bg-gray-200 rounded-xl"></div>
          </div>
        ))}
      </div>
    );
  }

  if (!subjects || subjects.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">Henüz test verisi yok</p>
      </div>
    );
  }

  // ✅ ÖNCELİK SKORUNA GÖRE SIRALA (YÜKSEK → DÜŞÜK)
  const sortedSubjects = [...subjects].sort((a, b) => {
    const scoreA = calculatePriorityScore(a);
    const scoreB = calculatePriorityScore(b);
    
    // Önce skora göre
    if (scoreB !== scoreA) return scoreB - scoreA;
    
    // Eşitse trend'e göre
    const trendOrder = { declining: 3, stable: 2, improving: 1 };
    const trendA = trendOrder[a.trend as keyof typeof trendOrder] || 0;
    const trendB = trendOrder[b.trend as keyof typeof trendOrder] || 0;
    if (trendB !== trendA) return trendB - trendA;
    
    // Eşitse düşük başarıya göre
    return a.progress_percentage - b.progress_percentage;
  });

  // En kritik dersi bul (vurgulama için)
  const mostCriticalId = sortedSubjects[0]?.subject_id;

  return (
    <div>
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
            className="absolute top-full left-0 mt-2 w-80 bg-white border border-gray-200 rounded-xl shadow-xl p-4 z-50">
            <h4 className="font-bold text-gray-900 mb-2">📖 Nasıl Okunur?</h4>
            <ul className="text-sm text-gray-700 space-y-2">
              <li>✅ <strong>Yüzde:</strong> Genel ilerleme puanı</li>
              <li>📈 <strong>Trend:</strong> Son haftalardaki performans yönü</li>
              <li>🎯 <strong>Kapsam:</strong> Kaç konuda test çözüldü</li>
              <li>🏆 <strong>Evrensel Ustalık:</strong> Genel başarı standardına göre uzman olunan konular (%75+ başarı)</li>
              <li>🧠 <strong>Kişisel Ustalık:</strong> Kendi geçmiş performansına göre gelişim gösterilen konular (sürekli artış trendi)</li>
              <li>💡 <strong>En üstteki</strong> en öncelikli derstir</li>
              <li>🔢 <strong>Sıralama:</strong> Risk + Trend + Momentum + Zorluk + Sınav Ağırlığı</li>
            </ul>
          </div>
        )}
      </div>

      {/* Ders Listesi */}
      <div className="space-y-3">
        {sortedSubjects.map((subject) => {
          const isExpanded = expandedSubjects.has(subject.subject_id);
          const isMostCritical = subject.subject_id === mostCriticalId;
          const trendDisplay = getTrendDisplay(subject.trend);
          const subjectIcon = getSubjectIcon(subject.subject_name);
          const priorityScore = calculatePriorityScore(subject);

          return (
            <div 
              key={subject.subject_id}
              className={`border rounded-xl overflow-hidden transition-all ${
                isMostCritical 
                  ? 'border-orange-300 bg-orange-50/30' 
                  : 'border-gray-200 bg-white'
              }`}
            >
              {/* ===== KAPALI DURUM (TEK SATIR) ===== */}
              <button
                onClick={() => toggleExpand(subject.subject_id)}
                className="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
              >
                {/* Sol: İkon + İsim + Kapsam */}
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                    <span className="text-2xl">{subjectIcon}</span>
                  </div>
                  
                  <div className="text-left">
                    <h3 className="font-bold text-gray-900 text-lg">
                      {subject.subject_name}
                    </h3>
                    {/* ✅ DÜZELTME: tested/total formatı */}
                    <p className="text-sm text-gray-500">
                      {subject.topics_tested}/{subject.topics_total} konuda test çözüldü
                    </p>
                  </div>
                </div>

                {/* Sağ: Yüzde + Trend + Badge */}
                <div className="flex items-center gap-6">
                  {/* Yüzde */}
                  <div className="text-right">
                    <div className="text-3xl font-bold text-gray-900">
                      {subject.progress_percentage}%
                    </div>
                  </div>

                  {/* Trend Badge */}
                  <div className={`px-4 py-2 rounded-lg ${trendDisplay.bg} flex items-center gap-2`}>
                    <span className="text-xl">{trendDisplay.emoji}</span>
                    <span className={`font-semibold text-sm ${trendDisplay.color}`}>
                      {trendDisplay.text}
                    </span>
                  </div>

                  {/* En kritik badge */}
                  {isMostCritical && (
                    <div className="px-3 py-1 bg-orange-500 text-white text-xs font-bold rounded-full">
                      ÖNCELİKLİ
                    </div>
                  )}

                  {/* Expand icon */}
                  <svg 
                    className={`w-6 h-6 text-gray-400 transition-transform ${
                      isExpanded ? 'rotate-180' : ''
                    }`}
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </div>
              </button>

              {/* ===== AÇIK DURUM (DETAYLAR) ===== */}
              {isExpanded && (
                <div className="px-6 pb-6 pt-2 border-t border-gray-200 space-y-4 bg-gray-50">
                  {/* ✅ YENİ: NEDEN ÖNCELİKLİ? */}
                  {isMostCritical && (
                    <div className="bg-orange-100 border border-orange-300 rounded-lg p-4">
                      <h4 className="font-bold text-orange-900 mb-2 flex items-center gap-2">
                        <span>🎯</span> Bu ders neden öncelikli?
                      </h4>
                      <ul className="text-sm text-orange-800 space-y-1">
                        {subject.progress_percentage < 50 && (
                          <li>• Düşük ilerleme (%{subject.progress_percentage})</li>
                        )}
                        {subject.trend === 'declining' && (
                          <li>• Performans düşüş eğiliminde</li>
                        )}
                        {subject.last_test_date && (() => {
                          const days = Math.floor(
                            (new Date().getTime() - new Date(subject.last_test_date).getTime()) / (1000 * 60 * 60 * 24)
                          );
                          if (days > 14) return <li>• {days} gündür test çözülmedi</li>;
                        })()}
                        {subject.test_count < 3 && (
                          <li>• Az test verisi (belirsizlik yüksek)</li>
                        )}
                        <li className="text-xs text-orange-600 mt-2">
                          💡 Öncelik skoru: {priorityScore}/100
                        </li>
                      </ul>
                    </div>
                  )}

                  {/* Progress Bar */}
                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span className="text-gray-600">İlerleme</span>
                      <span className="font-semibold">{subject.progress_percentage}%</span>
                    </div>
                    <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
                      <div 
                        className={`h-full transition-all duration-500 ${
                          subject.progress_percentage >= 75 ? 'bg-green-500' :
                          subject.progress_percentage >= 50 ? 'bg-yellow-500' :
                          'bg-red-500'
                        }`}
                        style={{ width: `${subject.progress_percentage}%` }}
                      />
                    </div>
                  </div>

                  {/* Trend detayı */}
                  {subject.test_count >= 3 && (
                    <div className="flex items-center gap-2 text-sm">
                      <span className="text-gray-600">Trend:</span>
                      <span className={`font-semibold ${trendDisplay.color}`}>
                        {trendDisplay.emoji} {trendDisplay.text}
                      </span>
                    </div>
                  )}

                  {/* Ustalık */}
                  {(subject.topics_mastered > 0 || subject.topics_mastered_personal > 0) && (
                    <div className="grid grid-cols-2 gap-3">
                      {subject.topics_mastered > 0 && (
                        <div className="bg-white p-3 rounded-lg border border-gray-200">
                          <div className="flex items-center gap-2 mb-1">
                            <span className="text-lg">🏆</span>
                            <span className="text-xs text-gray-500">Evrensel Ustalık</span>
                          </div>
                          <div className="text-xl font-bold text-purple-600">
                            {subject.topics_mastered} konu
                          </div>
                        </div>
                      )}
                      
                      {subject.topics_mastered_personal > 0 && (
                        <div className="bg-white p-3 rounded-lg border border-gray-200">
                          <div className="flex items-center gap-2 mb-1">
                            <span className="text-lg">🧠</span>
                            <span className="text-xs text-gray-500">Kişisel Ustalık</span>
                          </div>
                          <div className="text-xl font-bold text-blue-600">
                            {subject.topics_mastered_personal} konu
                          </div>
                        </div>
                      )}
                    </div>
                  )}

                  {/* Disclaimer */}
                  {subject.disclaimer && (
                    <div className={`text-xs px-3 py-2 rounded-lg ${
                      subject.phase === 'no_data' 
                        ? 'text-gray-600 bg-gray-100' 
                        : 'text-blue-600 bg-blue-50'
                    }`}>
                      💡 {subject.disclaimer}
                    </div>
                  )}

                  {/* İstatistikler */}
                  <div className="grid grid-cols-3 gap-3 pt-2 border-t border-gray-200">
                    <div className="text-center">
                      <div className="text-xs text-gray-500 mb-1">Test Sayısı</div>
                      <div className="text-lg font-bold text-gray-900">{subject.test_count}</div>
                    </div>
                    <div className="text-center">
                      <div className="text-xs text-gray-500 mb-1">Ort. Başarı</div>
                      <div className="text-lg font-bold text-gray-900">%{subject.avg_success_rate.toFixed(0)}</div>
                    </div>
                    <div className="text-center">
                      <div className="text-xs text-gray-500 mb-1">Kapsam</div>
                      <div className="text-lg font-bold text-gray-900">
                        {subject.topics_tested}/{subject.topics_total}
                      </div>
                    </div>
                  </div>

                  {/* Son test tarihi */}
                  {subject.last_test_date && (
                    <div className="text-xs text-gray-500 text-center pt-2 border-t border-gray-200">
                      Son test: {new Date(subject.last_test_date).toLocaleDateString('tr-TR')}
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}