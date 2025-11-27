'use client';

import React from 'react';

export default function ActionCards() {
  const actions = [
    {
      icon: '🔥',
      title: 'AKTİF TEKRAR',
      subtitle: '3 konu bekliyor',
      colorClass: 'border-t-red-500',
    },
    {
      icon: '📝',
      title: 'HIZLI TARAMA',
      subtitle: '10 dakika - Bilgi kontrolü',
      colorClass: 'border-t-orange-500',
    },
    {
      icon: '🎬',
      title: 'İZLE & UYGULA',
      subtitle: '2 interaktif video',
      colorClass: 'border-t-blue-500',
    },
  ];

  return (
    <div className="mb-5">
      <h2 className="text-white text-xl font-semibold mb-4">⚡ Hızlı Aksiyonlar</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {actions.map((action, index) => (
          <button
            key={index}
            className={`bg-white rounded-xl p-6 text-center hover:-translate-y-2 transition-all shadow-lg hover:shadow-2xl border-t-4 ${action.colorClass}`}
          >
            <div className="text-5xl mb-4">{action.icon}</div>
            <div className="text-lg font-bold text-gray-800 mb-2">{action.title}</div>
            <div className="text-sm text-gray-600">{action.subtitle}</div>
          </button>
        ))}
      </div>
    </div>
  );
}
