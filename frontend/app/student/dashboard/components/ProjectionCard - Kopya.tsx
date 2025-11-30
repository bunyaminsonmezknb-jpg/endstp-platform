'use client';

import { useState } from 'react';

interface ProjectionCardProps {
  projection: {
    totalTopics: number;
    completedTopics: number;
    estimatedDays: number;
    estimatedDate: string;
  };
}

export default function ProjectionCard({ projection }: ProjectionCardProps) {
  const [showDetails, setShowDetails] = useState(false);

  // Kalan konuları hesapla
  const remainingTopics = projection.totalTopics - projection.completedTopics;
  
  // İlerleme yüzdesi
  const progressPercent = (projection.completedTopics / projection.totalTopics) * 100;
  
  // Günlük hız hesapla (tahmini)
  const dailyVelocity = remainingTopics > 0 && projection.estimatedDays > 0
    ? (remainingTopics / projection.estimatedDays).toFixed(2)
    : '0';

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
              Hız: ~{dailyVelocity} konu/gün
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

      {/* Accordion Detaylar */}
      {showDetails && (
        <div className="mt-4 pt-4 border-t border-white/20 space-y-3 animate-fade-in">
          {/* A. Tempo Analizi */}
          <div className="bg-white/10 rounded-lg p-3">
            <div className="text-xs font-bold opacity-90 mb-2">📊 TEMPO ANALİZİ</div>
            <div className="space-y-1 text-sm">
              <div>
                <span className="opacity-75">Güncel Hızın:</span>{' '}
                <span className="font-bold">~{dailyVelocity} konu/gün</span>
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
                ? `Günde ${dailyVelocity} konu çalışarak hedefe ulaşabilirsin`
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
    </div>
  );
}
