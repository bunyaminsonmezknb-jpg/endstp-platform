'use client';

import React, { useState } from 'react';
import RecoveryModal from './RecoveryModal';

interface CriticalAlertProps {
  topicName: string;
  daysAgo: number;
  forgetRisk: number;
}

export default function CriticalAlert({ topicName, daysAgo, forgetRisk }: CriticalAlertProps) {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <>
      <div className="bg-gradient-to-r from-red-500 to-red-600 border-3 border-red-800 rounded-2xl p-6 mb-5 text-white shadow-2xl animate-pulse-slow relative overflow-hidden">
        {/* Shine effect */}
        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-shine" />
        
        <div className="relative z-10 flex items-center justify-between gap-5 flex-wrap">
          <div className="flex-1">
            <div className="text-4xl mb-3 animate-shake">⚠️</div>
            <h2 className="text-2xl font-bold mb-2">ACİL UNUTMA UYARISI!</h2>
            <p className="text-base opacity-95 leading-relaxed">
              <strong>&quot;{topicName}&quot;</strong> konusunu <strong>{daysAgo} gün önce</strong> çalıştın.<br />
              Bugün tekrar etmezsen <strong>%{forgetRisk} unutma riski</strong> var. Bilgi seviyesi kritik seviyede!
            </p>
          </div>
          
          <button
            onClick={() => setIsModalOpen(true)}
            className="bg-white text-red-800 px-8 py-4 rounded-xl text-base font-bold hover:scale-105 transition-transform shadow-lg whitespace-nowrap"
          >
            KURTARMA PLANINI AÇ →
          </button>
        </div>
      </div>

      <RecoveryModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        topicName={topicName}
      />
    </>
  );
}
