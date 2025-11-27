'use client';

import React, { useState } from 'react';
import SafeExternalLink from '@/components/SafeExternalLink';

interface RecoveryModalProps {
  isOpen: boolean;
  onClose: () => void;
  topicName: string;
}

interface RecoveryOption {
  id: string;
  icon: string;
  title: string;
  subtitle: string;
  url: string;
  partnerName: string;
}

export default function RecoveryModal({ isOpen, onClose, topicName }: RecoveryModalProps) {
  const [selectedOption, setSelectedOption] = useState<string | null>(null);

  if (!isOpen) return null;

  const recoveryOptions: RecoveryOption[] = [
    {
      id: 'video',
      icon: '📹',
      title: `Dr. Biyoloji - ${topicName} Özet Video`,
      subtitle: '15 dakika • YouTube',
      url: 'https://youtube.com/example',
      partnerName: 'Dr. Biyoloji (YouTube)',
    },
    {
      id: 'book',
      icon: '📚',
      title: `3D Yayınları - ${topicName} Test Bankası`,
      subtitle: '30 soru • Test 4',
      url: 'https://3dyayinlari.com/test',
      partnerName: '3D Yayınları',
    },
    {
      id: 'self',
      icon: '📝',
      title: 'Kendi Notlarımdan Tekrar Edeceğim',
      subtitle: 'Serbest çalışma',
      url: 'self-study',
      partnerName: 'Kendi Çalışma',
    },
  ];

  const handleOptionClick = (option: RecoveryOption) => {
    setSelectedOption(option.id);
    // Self-study için harici link açma
    if (option.url === 'self-study') {
      return;
    }
    // SafeExternalLink component'i zaten güvenli açacak
  };

  const handleComplete = () => {
    alert('Harika! Konudaki bilgi barın güncelleniyor... 🎉\n\n(Gerçek uygulamada: Backend\'e POST isteği gönderilir)');
    setSelectedOption(null);
    onClose();
  };

  return (
    <div
      className="fixed inset-0 bg-black/70 z-50 flex items-center justify-center p-4"
      onClick={onClose}
    >
      <div
        className="bg-white rounded-3xl p-10 max-w-2xl w-full shadow-2xl animate-slideIn"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-red-600 mb-2">
            🔴 {topicName} Konusu Tehlikede!
          </h2>
          <p className="text-gray-600">Nasıl Kurtarmak İstersin?</p>
        </div>

        {/* Options */}
        <div className="space-y-4 mb-8">
          {recoveryOptions.map((option) => (
            option.url === 'self-study' ? (
              // Self-study için normal button
              <button
                key={option.id}
                onClick={() => handleOptionClick(option)}
                className={`w-full bg-gradient-to-r from-gray-50 to-gray-100 border-2 rounded-xl p-5 flex items-center gap-4 transition-all hover:translate-x-2 hover:shadow-lg ${
                  selectedOption === option.id
                    ? 'border-end-purple shadow-lg'
                    : 'border-gray-300'
                }`}
              >
                <div className="text-4xl">{option.icon}</div>
                <div className="flex-1 text-left">
                  <div className="font-semibold text-gray-800">{option.title}</div>
                  <div className="text-sm text-gray-600">{option.subtitle}</div>
                </div>
              </button>
            ) : (
              // External links için SafeExternalLink
              <SafeExternalLink
                key={option.id}
                href={option.url}
                partnerName={option.partnerName}
                className={`w-full bg-gradient-to-r from-gray-50 to-gray-100 border-2 rounded-xl p-5 flex items-center gap-4 transition-all hover:translate-x-2 hover:shadow-lg ${
                  selectedOption === option.id
                    ? 'border-end-purple shadow-lg'
                    : 'border-gray-300'
                } block`}
              >
                <div className="text-4xl">{option.icon}</div>
                <div className="flex-1 text-left">
                  <div className="font-semibold text-gray-800">{option.title}</div>
                  <div className="text-sm text-gray-600">{option.subtitle}</div>
                  <div className="text-xs text-orange-600 mt-1">
                    🔗 Sponsorlu İçerik
                  </div>
                </div>
              </SafeExternalLink>
            )
          ))}
        </div>

        {/* Footer */}
        <div className="border-t pt-5 text-center">
          <button
            onClick={handleComplete}
            disabled={!selectedOption}
            className={`px-10 py-4 rounded-xl text-base font-bold transition-all ${
              selectedOption
                ? 'bg-gradient-to-r from-green-500 to-green-600 text-white hover:scale-105 shadow-lg'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }`}
          >
            ✓ Görevi Tamamladım, Grafiği Güncelle!
          </button>
        </div>
      </div>
    </div>
  );
}
