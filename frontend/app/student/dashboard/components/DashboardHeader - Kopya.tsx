'use client';

import React from 'react';
import { useRouter } from 'next/navigation';

interface DashboardHeaderProps {
  studentName: string;
  streak: number;
}

export default function DashboardHeader({ studentName, streak }: DashboardHeaderProps) {
  const router = useRouter();

  const handleLogout = () => {
    // End.stp güvenlik prosedürü: Token temizliği
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    
    // Cookie temizliği
    document.cookie = 'access_token=; path=/; max-age=0';
    
    // Login'e güvenli yönlendirme
    router.push('/login');
  };

  const handleNewTest = () => {
    // Next.js router ile hızlı geçiş
    router.push('/test-entry');
  };

  return (
    <div className="bg-white rounded-3xl shadow-lg p-6 mb-6">
      <div className="flex flex-col md:flex-row items-center justify-between gap-4">
        
        {/* Sol Taraf: Profil ve Karşılama */}
        <div className="flex items-center gap-4 w-full md:w-auto">
          <div className="w-16 h-16 bg-gradient-to-br from-purple-600 to-blue-600 rounded-full flex items-center justify-center text-white text-2xl font-bold shrink-0">
            {studentName.split(' ').map(n => n[0]).join('').substring(0, 2)}
          </div>
          <div>
            <h1 className="text-2xl md:text-3xl font-bold text-gray-800">
              Hoş geldin, {studentName}! 👋
            </h1>
            <div className="flex items-center gap-3 mt-1">
              <span className="text-gray-600 flex items-center gap-1">
                🔥 <span className="font-semibold">{streak} günlük seri</span>
              </span>
            </div>
          </div>
        </div>

        {/* Sağ Taraf: Aksiyon Butonları */}
        <div className="flex items-center gap-3 w-full md:w-auto justify-end">
          <button
            onClick={handleNewTest}
            className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-xl font-semibold hover:scale-105 transition-transform shadow-lg whitespace-nowrap"
          >
            ➕ Yeni Test Ekle
          </button>
          
          <button
            onClick={handleLogout}
            className="px-4 py-3 text-gray-600 hover:bg-gray-100 rounded-xl transition border border-gray-200"
          >
            🚪 Çıkış
          </button>
        </div>
      </div>
    </div>
  );
}
