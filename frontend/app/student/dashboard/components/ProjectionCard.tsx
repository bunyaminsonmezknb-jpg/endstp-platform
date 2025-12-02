'use client';

import { useState, useEffect } from 'react';
import FeedbackButtons from './FeedbackButtons';

interface ProjectionData {
  totalTopics: number;
  completedTopics: number;
  estimatedDays: number;
  estimatedDate: string;
}

export default function ProjectionCard() {
  const [projection, setProjection] = useState<ProjectionData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showDetails, setShowDetails] = useState(false);

  useEffect(() => {
    fetchProjection();
  }, []);

  const fetchProjection = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const userStr = localStorage.getItem('user');
      const accessToken = localStorage.getItem('access_token');

      if (!userStr || !accessToken) {
        throw new Error('Lütfen giriş yapın');
      }

      const user = JSON.parse(userStr);

      const response = await fetch('http://localhost:8000/api/v1/student/projection', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`,
        },
        body: JSON.stringify({
          student_id: user.id,
        }),
      });

      if (!response.ok) {
        throw new Error('Projeksiyon alınamadı');
      }

      const data = await response.json();

      if (data.status === 'no_data') {
        setProjection(null);
      } else if (data.projection) {
        setProjection({
          totalTopics: data.projection.total_topics || data.projection.totalTopics,
          completedTopics: data.projection.completed_topics || data.projection.completedTopics,
          estimatedDays: data.projection.estimated_days || data.projection.estimatedDays,
          estimatedDate: data.projection.estimated_date || data.projection.estimatedDate,
        });
      }
    } catch (err: any) {
      setError(err.message || 'Projeksiyon yüklenemedi');
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="bg-purple-100 rounded-2xl p-8 shadow-lg">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-purple-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Projeksiyon hesaplanıyor...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border-2 border-red-300 rounded-2xl p-6">
        <div className="text-center">
          <div className="text-4xl mb-2">⚠️</div>
          <div className="text-red-700 font-bold mb-2">Projeksiyon Hatası</div>
          <div className="text-sm text-red-600 mb-4">{error}</div>
          <button
            onClick={fetchProjection}
            className="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700"
          >
            Tekrar Dene
          </button>
        </div>
      </div>
    );
  }

  if (!projection) {
    return (
      <div className="bg-yellow-50 border-2 border-yellow-300 rounded-2xl p-8 text-center">
        <div className="text-6xl mb-4">📊</div>
        <h3 className="text-xl font-bold text-gray-800 mb-2">Henüz Projeksiyon Verisi Yok</h3>
        <p className="text-gray-600 mb-4">
          Projeksiyon hesaplayabilmek için önce test sonuçları girmelisiniz.
        </p>
        <a
          href="/test-entry"
          className="inline-block bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700"
        >
          Test Ekle
        </a>
      </div>
    );
  }

  // Kalan konuları hesapla
  const remainingTopics = projection.totalTopics - projection.completedTopics;
  
  // İlerleme yüzdesi
  const progressPercent = (projection.completedTopics / projection.totalTopics) * 100;
  
  // VELOCITY DÜZELTMESİ - Daha anlamlı format
  const formatVelocity = () => {
    if (remainingTopics === 0) return 'Tamamlandı! 🎉';
    if (projection.estimatedDays === 0) return 'Veri yetersiz';
    
    const dailyRate = remainingTopics / projection.estimatedDays;
    
    // Günlük 1'den az ise haftalık göster
    if (dailyRate < 1) {
      const weeklyRate = dailyRate * 7;
      if (weeklyRate < 1) {
        // Kaç günde 1 konu
        const daysPerTopic = Math.ceil(1 / dailyRate);
        return `1 konu/${daysPerTopic} günde`;
      }
      return `${weeklyRate.toFixed(1)} konu/hafta`;
    }
    
    return `${dailyRate.toFixed(1)} konu/gün`;
  };

  const velocityText = formatVelocity();

  // Uyarı seviyesi belirle
  const getWarningLevel = () => {
    if (projection.estimatedDays <= 30) return 'success';
    if (projection.estimatedDays <= 60) return 'warning';
    return 'danger';
  };

  const warningLevel = getWarningLevel();

  const getProjectionColor = () => {
    if (warningLevel === 'danger') return 'from-red-500 to-red-700';
    if (warningLevel === 'warning') return 'from-orange-500 to-orange-700';
    return 'from-purple-500 to-indigo-600';
  };

  // Halka grafiği parametreleri
  const circularProgressParams = {
    size: 140,
    strokeWidth: 12,
    center: 70,
    radius: 64
  };

  const circumference = 2 * Math.PI * circularProgressParams.radius;
  const progressOffset = circumference - ((projection.estimatedDays / 365) * circumference);

  return (
    <div className={`bg-gradient-to-r ${getProjectionColor()} text-white rounded-2xl p-6 shadow-xl transition-all`}>
      {/* Kompakt Görünüm */}
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div className="flex items-center gap-4 flex-1">
          <div className="text-5xl animate-bounce-slow">🎯</div>
          <div className="flex-1">
            <div className="text-sm opacity-90 font-medium">Tahmini Bitiş Tarihi</div>
            <div className="text-2xl font-bold">
              Bu hızla gidersen, {projection.estimatedDate} gibi bitecek!
            </div>
            <div className="text-xs opacity-75 mt-1">
              {projection.completedTopics}/{projection.totalTopics} konu tamamlandı • 
              Kalan: {remainingTopics} konu • 
              Hız: {velocityText}
            </div>
          </div>
        </div>

        {/* HALKA GRAFİĞİ */}
        <div className="relative" style={{ width: circularProgressParams.size, height: circularProgressParams.size }}>
          <svg width={circularProgressParams.size} height={circularProgressParams.size} className="transform -rotate-90">
            {/* Arka plan çemberi */}
            <circle
              cx={circularProgressParams.center}
              cy={circularProgressParams.center}
              r={circularProgressParams.radius}
              stroke="rgba(255,255,255,0.2)"
              strokeWidth={circularProgressParams.strokeWidth}
              fill="none"
            />
            {/* İlerleme çemberi */}
            <circle
              cx={circularProgressParams.center}
              cy={circularProgressParams.center}
              r={circularProgressParams.radius}
              stroke="white"
              strokeWidth={circularProgressParams.strokeWidth}
              fill="none"
              strokeDasharray={circumference}
              strokeDashoffset={progressOffset}
              strokeLinecap="round"
              className="transition-all duration-1000 ease-out"
            />
          </svg>
          {/* Merkez yazı */}
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <div className="text-4xl font-bold leading-none">{projection.estimatedDays}</div>
            <div className="text-xs opacity-90 mt-1">gün kaldı</div>
          </div>
        </div>
      </div>

      {/* İLERLEME YÜZDESİ AÇIKLAMASI */}
      <div className="mt-4 bg-white/10 rounded-xl p-4">
        <div className="flex items-start gap-2 mb-3">
          <span className="text-blue-200 text-lg">ℹ️</span>
          <div className="flex-1">
            <div className="text-sm font-bold mb-1">📊 Nihai Hedef İlerlemesi: %{progressPercent.toFixed(0)}</div>
            <p className="text-xs opacity-90">
              Bu oran, tüm konuların <strong>%85+ hatırlama oranına</strong> ulaşma hedefinizdir.
              Şu ana kadar <strong>{projection.totalTopics} konunun {projection.completedTopics}'unu</strong> başarıyla tamamladınız.
            </p>
          </div>
        </div>

        {/* PROGRESS BAR - ORTA NOKTA İMİ + NET SAYISI */}
        <div className="relative">
          {/* Progress bar */}
          <div className="w-full h-6 bg-white/20 rounded-full overflow-hidden relative">
            <div 
              className="h-full bg-gradient-to-r from-green-400 to-green-600 transition-all duration-1000"
              style={{ width: `${progressPercent}%` }}
            />
          </div>

          {/* Orta nokta imi + Net sayısı */}
          {progressPercent > 0 && (
            <div 
              className="absolute top-0 transform -translate-x-1/2 transition-all duration-1000"
              style={{ left: `${progressPercent}%` }}
            >
              {/* İm (Üstte) */}
              <div className="w-1 h-6 bg-white mx-auto"></div>
              {/* Tooltip (Altta) */}
              <div className="bg-purple-900 text-white px-3 py-1 rounded-lg text-xs font-bold shadow-lg whitespace-nowrap mt-1">
                {projection.completedTopics}/{projection.totalTopics} konu
              </div>
            </div>
          )}

          {/* Yüzde etiketleri */}
          <div className="flex justify-between text-xs opacity-75 mt-1">
            <span>0%</span>
            <span>%{progressPercent.toFixed(0)}</span>
            <span>100%</span>
          </div>
        </div>
      </div>

      {/* Accordion Detaylar */}
      {showDetails && (
        <div className="mt-4 pt-4 border-t border-white/20 space-y-3 animate-fade-in">
          {/* A. Tempo Analizi */}
          <div className="bg-white/10 rounded-lg p-3">
            <div className="text-xs font-bold opacity-90 mb-2">📊 TEMPO ANALİZİ</div>
            <div className="space-y-1 text-sm">
              <div>
                <span className="opacity-75">Güncel Hızın:</span>{' '}
                <span className="font-bold">{velocityText}</span>
              </div>
              <div>
                <span className="opacity-75">İlerleme:</span>{' '}
                <span className="font-bold">%{progressPercent.toFixed(1)}</span>
              </div>
            </div>
          </div>

          {/* B. Kalan İş Yükü */}
          <div className="bg-white/10 rounded-lg p-3">
            <div className="text-xs font-bold opacity-90 mb-2">📦 KALAN İŞ YÜKÜ</div>
            <div className="space-y-1 text-sm">
              <div>
                <span className="opacity-75">Toplam Konu:</span>{' '}
                <span className="font-bold">{projection.totalTopics}</span>
              </div>
              <div>
                <span className="opacity-75">Tamamlanan:</span>{' '}
                <span className="font-bold text-green-300">{projection.completedTopics}</span>
              </div>
              <div>
                <span className="opacity-75">Kalan:</span>{' '}
                <span className="font-bold text-orange-300">{remainingTopics}</span>
              </div>
            </div>
          </div>

          {/* C. Motivasyon Mesajı */}
          <div className="bg-white/5 rounded-lg p-3 border border-white/20">
            <div className="text-xs font-bold opacity-75 mb-1">💡 ÖNERI</div>
            <div className="text-xs opacity-90">
              {remainingTopics > 0 
                ? `${velocityText} çalışarak hedefe ulaşabilirsin`
                : 'Tebrikler! Tüm konuları tamamladın 🎉'
              }
            </div>
          </div>

          {/* D. Simülasyon (Demo) */}
          <div className="bg-yellow-500/20 rounded-lg p-3">
            <div className="text-xs font-bold mb-2">🎯 SİMÜLASYON</div>
            <div className="space-y-1 text-xs">
              <div className="flex justify-between">
                <span className="opacity-75">%20 daha hızlı →</span>
                <span className="font-bold">~{Math.max(1, Math.round(projection.estimatedDays * 0.8))} gün</span>
              </div>
              <div className="flex justify-between">
                <span className="opacity-75">%50 daha hızlı →</span>
                <span className="font-bold">~{Math.max(1, Math.round(projection.estimatedDays * 0.5))} gün</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Detay Butonu */}
      <button
        onClick={() => setShowDetails(!showDetails)}
        className="mt-4 text-xs opacity-75 hover:opacity-100 transition-opacity underline w-full text-center"
      >
        {showDetails ? '▲ Detayları Gizle' : '▼ Detayları Göster'}
      </button>

      {/* FEEDBACK BUTONU */}
      <div className="mt-4 pt-4 border-t border-white/20 flex justify-center">
        <FeedbackButtons
          componentType="projection_card"
          variant="like-dislike"
          size="sm"
          metadata={{ 
            estimated_days: projection.estimatedDays,
            progress_percent: progressPercent.toFixed(1)
          }}
        />
      </div>
    </div>
  );
}