'use client';

import React, { useMemo } from 'react';

interface HealthStatusBarProps {
  totalTopics: number;
  healthyTopics: number;
  warningTopics: number;
  frozenTopics: number;   // ✅ EKLE
  criticalTopics: number;
  currentlyShown: number;
}

function HealthStatusBar({
  totalTopics,
  healthyTopics,
  warningTopics,
  frozenTopics,
  criticalTopics,
  currentlyShown
}: HealthStatusBarProps) {

  // ✅ SADECE HESAPLAR useMemo
  const healthyPercent = useMemo(
    () => (healthyTopics / totalTopics) * 100,
    [healthyTopics, totalTopics]
  );

  const warningPercent = useMemo(
    () => (warningTopics / totalTopics) * 100,
    [warningTopics, totalTopics]
  );

  const frozenPercent = useMemo(
    () => (frozenTopics / totalTopics) * 100,
    [frozenTopics, totalTopics]
  );

  const criticalPercent = useMemo(
    () => (criticalTopics / totalTopics) * 100,
    [criticalTopics, totalTopics]
  );

  return (
    <div className="bg-white rounded-2xl p-6 shadow-lg mb-6">
      <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center gap-2">
        🧠 Genel Bilgi Sağlığı
      </h3>

      <div className="relative w-full h-2.5 bg-gray-200 rounded-full overflow-hidden mb-4">
        <div
          className="absolute left-0 h-full bg-gradient-to-r from-green-400 to-green-500 transition-all duration-500"
          style={{ width: `${healthyPercent}%` }}
        />

        <div
          className="absolute h-full bg-gradient-to-r from-yellow-400 to-yellow-500 transition-all duration-500"
          style={{
            left: `${healthyPercent}%`,
            width: `${warningPercent}%`
          }}
        />

        <div
          className="absolute h-full bg-gradient-to-r from-blue-300 to-blue-400 transition-all duration-500"
          style={{
            left: `${healthyPercent + warningPercent}%`,
            width: `${frozenPercent}%`
          }}
        />

        <div
          className="absolute h-full bg-gradient-to-r from-red-400 to-red-500 transition-all duration-500"
          style={{
            left: `${healthyPercent + warningPercent + frozenPercent}%`,
            width: `${criticalPercent}%`
          }}
        />
      </div>

      <div className="flex items-center justify-between text-sm flex-wrap gap-2">
        <div className="flex items-center gap-4 flex-wrap">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
            <span className="text-gray-600">
              Sağlıklı: <span className="font-bold text-green-600">{healthyTopics}</span>
            </span>
          </div>

          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
            <span className="text-gray-600">
              ⚠️ Risk: <span className="font-bold text-yellow-600">{warningTopics}</span>
            </span>
          </div>

          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-blue-400"></div>
            <span className="text-gray-600">
              ❄️ Donmuş: <span className="font-bold text-blue-600">{frozenTopics}</span>
            </span>
          </div>

          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <span className="text-gray-600">
              🆘 Kritik: <span className="font-bold text-red-600">{criticalTopics}</span>
            </span>
          </div>
        </div>

        <div className="text-gray-500">
          <span className="font-bold text-purple-600">{totalTopics}</span> konu izleniyor
        </div>
      </div>

      <div className="mt-3 pt-3 border-t border-gray-200 text-xs text-gray-500">
        💡 Güncel Durum:{' '}
        <span className="font-semibold text-gray-700">
          {currentlyShown}/{totalTopics}
        </span>{' '}
        konu gösteriliyor
      </div>
    </div>
  );
}

export default React.memo(HealthStatusBar);