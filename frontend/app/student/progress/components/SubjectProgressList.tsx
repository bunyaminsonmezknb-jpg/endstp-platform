'use client';

import { useState, useRef, useEffect } from 'react';

interface Subject {
  subject_id: string;
  subject_name: string | null; // 🔴 BURASI
  progress_percentage: number;
  test_count: number;
  topics_total: number;
  unique_topics_tested: number;
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

// ===== DERS İKONLARI =====
function getSubjectIcon(subjectName?: string | null): string {
  if (!subjectName || typeof subjectName !== 'string') return '📚';
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
  
  return '📚';
}

// ===== HİBRİT MODEL - ÖNCELİK SKORU ⭐ =====
function calculatePriorityScore(subject: Subject): number {
  // ⚠️ 0 TEST DURUMU - HİBRİT MODEL
  if (subject.test_count === 0) {
    // Orta seviye sabit skor (gerçek riskten ayrı kategoride)
    return 50; // 45-55 arası sabit değer
  }
  
  let score = 0;
  
  // MOTOR 1: ÖNCELİK (Risk/Aciliyet) - %45 ağırlık
  const priorityScore = (() => {
    let p = 0;
    
    if (subject.progress_percentage < 30) p += 50;
    else if (subject.progress_percentage < 50) p += 35;
    else if (subject.progress_percentage < 70) p += 20;
    
    if (subject.trend === 'declining') p += 40;
    else if (subject.trend === 'stable') p += 15;
    
    if (subject.test_count < 3) p += 15;
    else if (subject.test_count < 5) p += 8;
    
    return p;
  })();
  
  score += priorityScore * 0.45;
  
  // MOTOR 2: TEKRAR RİSKİ (Unutma eğrisi) - %25 ağırlık
  const reviewScore = (() => {
    if (!subject.last_test_date) return 60;
    
    const daysSinceTest = Math.floor(
      (new Date().getTime() - new Date(subject.last_test_date).getTime()) / (1000 * 60 * 60 * 24)
    );
    
    if (daysSinceTest > 21) return 50;
    if (daysSinceTest > 14) return 35;
    if (daysSinceTest > 7) return 20;
    return 5;
  })();
  
  score += reviewScore * 0.25;
  
  // MOTOR 3: MOMENTUM - %20 ağırlık
  const momentumScore = (() => {
    let m = 0;
    
    if (subject.trend === 'declining') m += 40;
    else if (subject.trend === 'stable') m += 20;
    else if (subject.trend === 'improving') m += 5;
    
    if (subject.test_count < 2) m += 30;
    else if (subject.test_count < 5) m += 15;
    
    return m;
  })();
  
  score += momentumScore * 0.20;
  
  // MOTOR 4: ÖĞRENME ZORLUĞU - %10 ağırlık
  const difficultyScore = (() => {
    const coverage = (subject.unique_topics_tested / subject.topics_total) * 100;
    
    if (coverage < 30 && subject.avg_success_rate < 50) return 40;
    if (coverage < 50 && subject.avg_success_rate < 60) return 25;
    if (subject.avg_success_rate < 50) return 15;
    
    return 5;
  })();
  
  score += difficultyScore * 0.10;
  
  return Math.round(score);
}

// ===== TREND EMOJI & TEXT ⭐ =====
function getTrendDisplay(trend: string) {
  switch(trend) {
    case 'improving':
      return { emoji: '📈', text: 'Yükseliyor', color: 'text-green-700', bg: 'bg-green-50', description: 'Son testlerde performans artışı var' };
    case 'declining':
      return { emoji: '📉', text: 'Düşüyor', color: 'text-red-700', bg: 'bg-red-50', description: 'Son 3 testin ortalaması düşüş gösteriyor' };
    case 'stable':
      return { emoji: '➡️', text: 'Sabit', color: 'text-blue-700', bg: 'bg-blue-50', description: 'Performans dengeli seyrediyor' };
    case 'unknown':
      return { emoji: '⚪', text: 'Veri Yok', color: 'text-gray-700', bg: 'bg-gray-50', description: 'Henüz yeterli test çözülmedi' };
    default:
      return { emoji: '⏸️', text: 'Belirsiz', color: 'text-gray-700', bg: 'bg-gray-50', description: 'Veri yetersiz' };
  }
}

// ===== ÖNERİ MESAJI OLUŞTUR ⭐ =====
function getActionSuggestion(subject: Subject): string | null {
  if (subject.test_count === 0) {
    return `İlk testini çöz → Analizi aktif hale getir`;
  }
  
  if (subject.unique_topics_tested < subject.topics_total * 0.2) {
    const needMore = Math.ceil(subject.topics_total * 0.2) - subject.unique_topics_tested;
    return `${needMore} yeni konuda daha test çöz → Kapsamı %20'ye çıkar`;
  }
  
  if (subject.trend === 'declining' && subject.test_count >= 3) {
    return `Son performans düştü → Zayıf konulara tekrar dön`;
  }
  
  const daysSinceTest = subject.last_test_date 
    ? Math.floor((new Date().getTime() - new Date(subject.last_test_date).getTime()) / (1000 * 60 * 60 * 24))
    : 999;
  
  if (daysSinceTest > 14) {
    return `${daysSinceTest} gündür test yok → Unutma riski artıyor`;
  }
  
  return null;
}

export default function SubjectProgressList({ subjects, isLoading }: SubjectProgressListProps) {
  const [expandedSubjects, setExpandedSubjects] = useState<Set<string>>(new Set());
  const [showTooltip, setShowTooltip] = useState(false);
  const tooltipRef = useRef<HTMLDivElement>(null);

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

  useEffect(() => {
    if (subjects && subjects.length > 0 && expandedSubjects.size === 0) {
      const sortedByPriority = [...subjects].sort((a, b) => 
        calculatePriorityScore(b) - calculatePriorityScore(a)
      );
      // İlk dersi aç (0 testli değilse)
      const firstWithData = sortedByPriority.find(s => s.test_count > 0);
      if (firstWithData) {
        setExpandedSubjects(new Set([firstWithData.subject_id]));
      }
    }
  }, [subjects]);

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

  // ✅ SIRALAMADA 3 KATEGORİ
  const sortedSubjects = [...subjects].sort((a, b) => {
    const scoreA = calculatePriorityScore(a);
    const scoreB = calculatePriorityScore(b);
    
    // 0 testliler en alta
    if (a.test_count === 0 && b.test_count > 0) return 1;
    if (a.test_count > 0 && b.test_count === 0) return -1;
    
    // Gerçek risk skoru
    if (scoreB !== scoreA) return scoreB - scoreA;
    
    const trendOrder = { declining: 3, stable: 2, improving: 1, unknown: 0 };
    const trendA = trendOrder[a.trend as keyof typeof trendOrder] || 0;
    const trendB = trendOrder[b.trend as keyof typeof trendOrder] || 0;
    if (trendB !== trendA) return trendB - trendA;
    
    return a.progress_percentage - b.progress_percentage;
  });

  const mostCriticalId = sortedSubjects.find(s => s.test_count > 0)?.subject_id;

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

        {showTooltip && (
          <div 
            ref={tooltipRef}
            className="absolute top-full left-0 mt-2 w-96 bg-white border border-gray-200 rounded-xl shadow-xl p-4 z-50">
            <h4 className="font-bold text-gray-900 mb-2">📖 Nasıl Okunur?</h4>
            <ul className="text-sm text-gray-700 space-y-2">
              <li>✅ <strong>Yüzde:</strong> Başarı, kapsam ve istikrarın birleşimi</li>
              <li>📈 <strong>Trend:</strong> Son 3 testin performans yönü</li>
              <li>📝 <strong>Test Sayısı:</strong> Toplam çözülen test adedi</li>
              <li>📚 <strong>Konu Kapsamı:</strong> Kaç farklı konuda çalışıldı</li>
              <li>🏆 <strong>Evrensel Ustalık:</strong> %75+ başarılı konular</li>
              <li>🧠 <strong>Kişisel Ustalık:</strong> Kendi ortalamanın üstü</li>
              <li>💡 <strong>En üstteki</strong> en öncelikli derstir</li>
              <li className="text-xs text-gray-500 mt-2">
                ⚪ Veri olmayan dersler ayrı kategoride gösterilir
              </li>
            </ul>
          </div>
        )}
      </div>

      {/* Ders Listesi */}
      <div className="space-y-3">
        {sortedSubjects.map((subject) => {
          const isExpanded = expandedSubjects.has(subject.subject_id);
          const isMostCritical = subject.subject_id === mostCriticalId;
          const isNoData = subject.test_count === 0;
          const trendDisplay = getTrendDisplay(subject.trend);
          const subjectIcon = getSubjectIcon(subject.subject_name);
          const priorityScore = calculatePriorityScore(subject);
          const actionSuggestion = getActionSuggestion(subject);

          return (
            <div 
              key={subject.subject_id}
              className={`border rounded-xl overflow-hidden transition-all ${
                isNoData
                  ? 'border-gray-300 bg-gray-50/50'
                  : isMostCritical 
                    ? 'border-orange-300 bg-orange-50/30' 
                    : 'border-gray-200 bg-white'
              }`}
            >
              {/* ===== KAPALI DURUM ===== */}
              <button
                onClick={() => toggleExpand(subject.subject_id)}
                className="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center gap-4">
                  <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${
                    isNoData ? 'bg-gray-200' : 'bg-purple-100'
                  }`}>
                    <span className="text-2xl">{subjectIcon}</span>
                  </div>
                  
                  <div className="text-left">
                    <h3 className="font-bold text-gray-900 text-lg">
                      {subject.subject_name ?? 'Ders Adı Yok'}
                    </h3>

                    <p className="text-sm text-gray-500">
                      {isNoData 
                        ? `Henüz test çözülmedi (${subject.topics_total} konu var)`
                        : `📝 ${subject.test_count} test • 📚 ${subject.unique_topics_tested}/${subject.topics_total} konu`
                      }
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-6">
                  {!isNoData && (
                    <div className="text-right">
                      <div className="text-3xl font-bold text-gray-900">
                        {subject.progress_percentage}%
                      </div>
                    </div>
                  )}

                  <div className={`px-4 py-2 rounded-lg ${trendDisplay.bg} flex items-center gap-2`}>
                    <span className="text-xl">{trendDisplay.emoji}</span>
                    <span className={`font-semibold text-sm ${trendDisplay.color}`}>
                      {trendDisplay.text}
                    </span>
                  </div>

                  {isNoData && (
                    <div className="px-3 py-1 bg-gray-400 text-white text-xs font-bold rounded-full">
                      VERİ YOK
                    </div>
                  )}

                  {isMostCritical && !isNoData && (
                    <div className="px-3 py-1 bg-orange-500 text-white text-xs font-bold rounded-full">
                      ÖNCELİKLİ
                    </div>
                  )}

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

              {/* ===== AÇIK DURUM ===== */}
              {isExpanded && (
                <div className="px-6 pb-6 pt-2 border-t border-gray-200 space-y-4 bg-gray-50">
                  {/* 0 TEST UYARISI */}
                  {isNoData && (
                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                      <h4 className="font-bold text-blue-900 mb-2 flex items-center gap-2">
                        <span>ℹ️</span> Bu derste henüz yeterli veri yok
                      </h4>
                      <p className="text-sm text-blue-700">
                        İlk testini çözerek analizi aktif hale getirebilirsin. 
                        Sistemde <strong>{subject.topics_total} konu</strong> mevcut.
                      </p>
                    </div>
                  )}

                  {/* KRİTİK DERS AÇIKLAMASI */}
                  {isMostCritical && !isNoData && (
                    <div className="bg-orange-100 border border-orange-300 rounded-lg p-4">
                      <h4 className="font-bold text-orange-900 mb-2 flex items-center gap-2">
                        <span>🎯</span> Bu ders neden öncelikli?
                      </h4>
                      <ul className="text-sm text-orange-800 space-y-1">
                        {subject.progress_percentage < 50 && (
                          <li>• Düşük ilerleme (%{subject.progress_percentage})</li>
                        )}
                        {subject.trend === 'declining' && (
                          <li>• Performans düşüş eğiliminde (son 3 test)</li>
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
                        {subject.unique_topics_tested < subject.topics_total * 0.3 && (
                          <li>• Düşük konu kapsamı ({subject.unique_topics_tested}/{subject.topics_total})</li>
                        )}
                        <li className="text-xs text-orange-600 mt-2">
                          💡 Öncelik skoru: {priorityScore}/100
                        </li>
                      </ul>
                    </div>
                  )}

                  {/* ÖNERİ AKSIYONU ⭐ */}
                  {actionSuggestion && (
                    <div className="bg-purple-50 border border-purple-200 rounded-lg p-3 flex items-center gap-3">
                      <span className="text-2xl">💡</span>
                      <div className="flex-1">
                        <p className="text-sm font-semibold text-purple-900">Öneri:</p>
                        <p className="text-sm text-purple-700">{actionSuggestion}</p>
                      </div>
                    </div>
                  )}

                  {!isNoData && (
                    <>
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
                        <p className="text-xs text-gray-500 mt-1">
                          Başarı, kapsam ve istikrarın birleşimi
                        </p>
                      </div>

                      {/* Trend detayı ⭐ */}
                      {subject.test_count >= 3 && (
                        <div className="bg-white p-3 rounded-lg border border-gray-200">
                          <div className="flex items-center gap-2 mb-1">
                            <span className={`font-semibold ${trendDisplay.color}`}>
                              {trendDisplay.emoji} {trendDisplay.text}
                            </span>
                          </div>
                          <p className="text-xs text-gray-600">
                            {trendDisplay.description}
                          </p>
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
                        <div className="text-xs px-3 py-2 rounded-lg bg-blue-50 text-blue-600">
                          💡 {subject.disclaimer}
                        </div>
                      )}

                      {/* İstatistikler */}
                      <div className="grid grid-cols-3 gap-3 pt-2 border-t border-gray-200">
                        <div>
                          <p className="text-xs text-gray-500 mb-2">TEST SAYISI</p>
                          <div className="bg-white p-3 rounded-lg border border-gray-200">
                            <div className="text-2xl font-bold text-gray-900 mb-1">
                              📝 {subject.test_count}
                            </div>
                            <p className="text-xs text-gray-500">test çözüldü</p>
                          </div>
                        </div>

                        <div>
                          <p className="text-xs text-gray-500 mb-2">KONU KAPSAMI</p>
                          <div className="bg-white p-3 rounded-lg border border-gray-200">
                            <div className="text-2xl font-bold text-gray-900 mb-1">
                              📚 {subject.unique_topics_tested}/{subject.topics_total}
                            </div>
                            <p className="text-xs text-gray-500">
                              {subject.unique_topics_tested === 0 
                                ? 'henüz çalışılmadı'
                                : `${Math.round((subject.unique_topics_tested / subject.topics_total) * 100)}% kapsam`
                              }
                            </p>
                            <div className="w-full bg-gray-200 rounded-full h-1.5 mt-2">
                              <div 
                                className="bg-purple-500 h-1.5 rounded-full transition-all"
                                style={{ 
                                  width: `${(subject.unique_topics_tested / subject.topics_total) * 100}%` 
                                }}
                              />
                            </div>
                          </div>
                        </div>

                        <div>
                          <p className="text-xs text-gray-500 mb-2">ORT. BAŞARI</p>
                          <div className="bg-white p-3 rounded-lg border border-gray-200">
                            <div className="text-2xl font-bold text-gray-900 mb-1">
                              %{subject.avg_success_rate.toFixed(0)}
                            </div>
                            <p className="text-xs text-gray-500">ortalama</p>
                          </div>
                        </div>
                      </div>

                      {/* Son test performansı ⭐ */}
                      {subject.last_test_date && subject.test_count >= 2 && (
                        <div className="text-xs text-gray-500 text-center pt-2 border-t border-gray-200">
                          Son test: {new Date(subject.last_test_date).toLocaleDateString('tr-TR')}
                        </div>
                      )}
                    </>
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