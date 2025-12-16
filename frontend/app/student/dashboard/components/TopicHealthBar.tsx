'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import type { Topic } from '@/lib/store/studentDashboardStore';

interface TopicHealthBarProps {
  topics: Topic[];
}

export default function TopicHealthBar({ topics }: TopicHealthBarProps) {
  const router = useRouter();
  const [expandedTopicId, setExpandedTopicId] = useState<string | null>(null);

  // Mock dataları filtrele
  const realTopics = topics.filter((t) => !t.id.startsWith('mock-'));
  const hasRealTopics = realTopics.length > 0;

  const toggleExpand = (topicId: string) => {
    setExpandedTopicId(expandedTopicId === topicId ? null : topicId);
  };

  const getBarColorClass = (status: string) => {
    if (status === 'critical') return 'bg-gradient-to-r from-red-500 to-red-700 animate-pulse';
    if (status === 'warning') return 'bg-gradient-to-r from-orange-400 to-orange-600';
    if (status === 'good') return 'bg-gradient-to-r from-emerald-500 to-emerald-700';
    if (status === 'excellent') return 'bg-gradient-to-r from-green-400 to-green-600';
    if (status === 'frozen') return 'bg-gradient-to-r from-blue-300 to-blue-400';
    return 'bg-gray-400';
  };

  const getStatusBgClass = (status: string) => {
    if (status === 'critical') return 'bg-red-50 border-red-200 hover:bg-red-100';
    if (status === 'warning') return 'bg-orange-50 border-orange-200 hover:bg-orange-100';
    if (status === 'good') return 'bg-emerald-50 border-emerald-200 hover:bg-emerald-100';
    if (status === 'excellent') return 'bg-green-50 border-green-200 hover:bg-green-100';
    if (status === 'frozen') return 'bg-gradient-to-r from-blue-50 to-blue-100 border-blue-300 hover:from-blue-100 hover:to-blue-200';
    return 'bg-gray-50 border-gray-200 hover:bg-gray-100';
  };

  const getStatusColor = (status: string) => {
    if (status === 'critical') return 'text-red-600';
    if (status === 'warning') return 'text-orange-600';
    if (status === 'good') return 'text-emerald-600';
    if (status === 'excellent') return 'text-green-600';
    if (status === 'frozen') return 'text-blue-700';
    return 'text-gray-600';
  };

const getNextReviewText = (
  nextReview?: { daysRemaining?: number; urgency?: string }
) => {
  if (!nextReview) {
    return { text: '📅 Bekliyor', color: 'text-gray-500' };
  }
  const { daysRemaining = 0, urgency = 'NORMAL' } = nextReview;
  
  // ✅ GECİKMİŞ KONTROL (daysRemaining = 0 ve urgent ise gecikmiş demektir)
  if (daysRemaining === 0 && (urgency === 'HEMEN' || urgency === 'ACİL')) {
    return { 
      text: '🚨 GECİKMİŞ!', 
      color: 'text-red-600 font-bold animate-pulse' 
    };
  }
  
  if (urgency === 'HEMEN') {
    return { text: '⏰ BUGÜN', color: 'text-red-600 font-bold' };
  }
  if (urgency === 'ACİL') {
    return { text: `📅 ${daysRemaining} gün sonra (ACİL)`, color: 'text-orange-600 font-semibold' };
  }
  if (urgency === 'YAKIN') {
    return { text: `📅 ${daysRemaining} gün sonra`, color: 'text-yellow-600' };
  }
  if (urgency === 'NORMAL') {
    return { text: `📅 ${daysRemaining} gün sonra`, color: 'text-green-600' };
  }
  if (urgency === 'RAHAT') {
    return { text: `📅 ${daysRemaining} gün sonra (Rahat)`, color: 'text-emerald-600' };
  }
  return { text: '📅 Bekliyor', color: 'text-gray-500' };
};

  const getPartnerLinks = (topicName: string) => {
    return [
      { provider: 'TYT.net', type: 'Video', title: `${topicName} Konu Anlatımı`, icon: '🎥', url: '#' },
      { provider: 'Esen Yayınları', type: 'Test', title: `${topicName} Test Bankası`, icon: '📝', url: '#' },
      { provider: 'Khan Academy', type: 'Pratik', title: `${topicName} Alıştırmalar`, icon: '🎯', url: '#' }
    ];
  };

  return (
    <div className="bg-white rounded-3xl p-8 mb-5 shadow-lg">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
          🩺 Bilgi Sağlığı Durumu
        </h2>
        <div className="text-right">
          <div className="text-sm text-gray-500">Dolu bar = İyi hatırlıyorsun</div>
          <div className="text-xs text-gray-400">Toplam {realTopics.length} konu izleniyor</div>
        </div>
      </div>

      <div className="space-y-4">
        {realTopics.map((topic) => {
          const isExpanded = expandedTopicId === topic.id;
          const nextReview = getNextReviewText(topic.nextReview);
          const partnerLinks = getPartnerLinks(topic.name);
          const isFrozen = topic.status === 'frozen';
          const isCritical = topic.status === 'critical';
          
          return (
            <div
              key={topic.id}
              className={`${getStatusBgClass(topic.status)} ${isFrozen ? 'border-dashed' : ''} border-2 rounded-2xl p-5 cursor-pointer transition-all duration-300 hover:shadow-xl ${isExpanded ? 'ring-2 ring-purple-400 shadow-xl' : ''}`}
              onClick={() => toggleExpand(topic.id)}
            >
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-3">
                  <span className="text-3xl">{topic.emoji}</span>
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <h3 className="font-bold text-gray-800 text-lg">{topic.name}</h3>
                      {topic.achievementBadge && (
                        <span className="bg-gradient-to-r from-yellow-400 to-orange-500 text-white text-xs px-3 py-1 rounded-full font-bold inline-flex items-center gap-1 shadow-md">
                          {topic.achievementBadge.icon} {topic.achievementBadge.text}
                        </span>
                      )}
                    </div>
                    <div className="text-sm text-gray-600">{topic.subject}</div>
                    <div className={`text-xs mt-1 ${nextReview.color}`}>{nextReview.text}</div>
                  </div>
                </div>

                <div className="text-right">
                  <div className="text-3xl font-bold text-gray-800">%{topic.rememberingRate}</div>
                  <div className={`text-xs uppercase tracking-wide font-bold ${getStatusColor(topic.status)}`}>
                    {topic.statusText}
                  </div>
                </div>
              </div>

              <div className="mb-3">
                <div className="h-8 bg-white/50 rounded-full overflow-hidden shadow-inner border border-gray-200">
                  <div
                    className={`h-full transition-all duration-700 ${getBarColorClass(topic.status)} flex items-center justify-end px-4`}
                    style={{ width: `${topic.rememberingRate}%` }}
                  >
                    <span className="text-white font-bold text-sm drop-shadow">{topic.rememberingRate}%</span>
                  </div>
                </div>
              </div>

              {isExpanded && (
                <div className="mt-4 pt-4 border-t-2 border-gray-200 space-y-4 animate-fade-in">
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
                    <div className="bg-white rounded-lg p-3 shadow-sm">
                      <div className="text-gray-500 text-xs mb-1">📜 Son Çalışma</div>
                      <div className="font-semibold text-gray-800">{topic.daysSinceLastTest} gün önce</div>
                    </div>
                    
                    <div className="bg-white rounded-lg p-3 shadow-sm">
                      <div className="text-gray-500 text-xs mb-1">📊 Son Başarı</div>
                      <div className="font-semibold text-gray-800">
                        %{Math.round(topic.latestSuccessRate ?? 0)} ({(topic.latestNet ?? 0).toFixed(1)} net)
                      </div>
                    </div>
                    
                    <div className="bg-white rounded-lg p-3 shadow-sm">
                      <div className="text-gray-500 text-xs mb-1">🎯 Toplam Test</div>
                      <div className="font-semibold text-gray-800">{topic.totalTests} kez</div>
                    </div>
                    
                    <div className="bg-white rounded-lg p-3 shadow-sm">
                      <div className="text-gray-500 text-xs mb-1">📅 Sonraki Tekrar</div>
                      <div className={`font-semibold ${nextReview.color}`}>
                        {topic.nextReview?.daysRemaining === 0
                          ? 'Bugün!'
                          : `${topic.nextReview?.daysRemaining ?? '-'} gün`}

                      </div>
                    </div>
                  </div>

                  <div className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-xl p-4 border-2 border-purple-200">
                    <div className="flex items-center gap-2 mb-3">
                      <span className="text-xl">🎯</span>
                      <h4 className="font-bold text-gray-800">Önerilen Çalışma (Kurtarma Reçetesi)</h4>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                      {partnerLinks.map((link, idx) => (
                        <a 
                          key={idx}
                          href={link.url}
                          onClick={(e) => e.stopPropagation()}
                          className="bg-white hover:bg-purple-50 rounded-lg p-3 border border-purple-200 hover:border-purple-400 transition-all hover:shadow-md group block"
                        >
                          <div className="flex items-center gap-2 mb-2">
                            <span className="text-2xl">{link.icon}</span>
                            <div className="text-xs text-purple-600 font-semibold">{link.provider}</div>
                          </div>
                          <div className="text-sm font-medium text-gray-700 group-hover:text-purple-700">
                            {link.title}
                          </div>
                          <div className="text-xs text-gray-500 mt-1">{link.type}</div>
                        </a>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {isFrozen && !isExpanded && (
                <div className="mt-3 bg-blue-200 text-blue-800 rounded-lg px-4 py-2 text-sm font-semibold flex items-center gap-2">
                  <span className="text-xl animate-pulse">❄️</span>
                  <span>Bu konu DONUYOR!</span>
                </div>
              )}

              {isCritical && !isExpanded && (
                <div className="mt-3 bg-red-200 text-red-800 rounded-lg px-4 py-2 text-sm font-semibold flex items-center gap-2 animate-pulse">
                  <span className="text-xl">🔥</span>
                  <span>ACİL DURUM!</span>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {hasRealTopics && (
        <button
          onClick={(e) => {
            e.stopPropagation();
            router.push('/test-entry');
          }}
          className="w-full mt-6 border-2 border-dashed border-gray-300 hover:border-purple-400 bg-gray-50 hover:bg-purple-50 rounded-2xl p-6 text-center transition-all hover:shadow-lg group"
        >
          <div className="text-4xl mb-2 group-hover:scale-110 transition-transform">➕</div>
          <div className="text-lg font-bold text-gray-600 group-hover:text-purple-600">Yeni Konu Test Et</div>
          <div className="text-sm text-gray-500 mt-1">Test Entry'den başka konularda da test ekle</div>
        </button>
      )}

      {!hasRealTopics && (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">📝</div>
          <h3 className="text-xl font-bold text-gray-800 mb-2">Henüz test eklenmemiş</h3>
          <p className="text-gray-600 mb-4">Test Entry sayfasından ilk testini ekle!</p>
          <button
            onClick={() => router.push('/test-entry')}
            className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-3 rounded-xl font-semibold hover:scale-105 transition-transform"
          >
            ➕ İlk Testi Ekle
          </button>
        </div>
      )}
    </div>
  );
}
