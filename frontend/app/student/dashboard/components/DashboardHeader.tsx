'use client';

import React, { useState, useRef, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { ChevronDown } from 'lucide-react';
import { NotificationBell } from '@/components/NotificationBell';
import { getSupabaseClient } from '@/lib/supabase/client';
import { supabase } from '@/lib/supabase/client';

interface DashboardHeaderProps {
  studentName: string;
  streak: number;
  studentId?: string;
}

function DashboardHeader({ studentName, streak, studentId }: DashboardHeaderProps) {
  const router = useRouter();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setIsMenuOpen(false);
      }
    };
    if (isMenuOpen) document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isMenuOpen]);

  const handleLogout = useCallback(async () => {
    try {
      await supabase.auth.signOut();
    } finally {
      router.push('/login');
      router.refresh();
    }
  }, [router]);


  const handleNewTest = useCallback(() => router.push('/test-entry'), [router]);
  const handlePastTests = useCallback(() => router.push('/past-tests'), [router]);
  const handleProfile = useCallback(() => router.push('/student/profile'), [router]);
  const handleSettings = useCallback(() => router.push('/student/settings'), [router]);
  const handleSubscription = useCallback(() => router.push('/student/subscription'), [router]);
  const handleHelp = useCallback(() => router.push('/student/help'), [router]);

  const getInitials = (name: string) =>
    name
      .split(' ')
      .map((n) => n[0])
      .join('')
      .slice(0, 2)
      .toUpperCase();

  return (
    <div className="bg-white rounded-3xl shadow-lg p-6 mb-6">
      <div className="flex flex-col md:flex-row items-center justify-between gap-4">
        {/* Sol Taraf: Avatar + Dropdown Menu */}
        <div className="flex items-center gap-4 w-full md:w-auto relative" ref={menuRef}>
          {/* Tıklanabilir Avatar + İsim */}
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="flex items-center gap-4 hover:bg-gray-50 rounded-2xl p-2 -m-2 transition-colors group"
          >
            <div className="w-16 h-16 bg-gradient-to-br from-purple-600 to-blue-600 rounded-full flex items-center justify-center text-white text-2xl font-bold shrink-0 group-hover:scale-105 transition-transform">
              {getInitials(studentName)}
            </div>

            <div className="text-left">
              <h1 className="text-2xl md:text-3xl font-bold text-gray-800 flex items-center gap-2">
                Hoş geldin, {studentName}! 👋
                <ChevronDown
                  size={20}
                  className={`text-gray-500 transition-transform ${isMenuOpen ? 'rotate-180' : ''}`}
                />
              </h1>
              <div className="flex items-center gap-3 mt-1">
                <span className="text-gray-600 flex items-center gap-1">
                  🔥 <span className="font-semibold">{streak} günlük seri</span>
                </span>
              </div>
            </div>
          </button>

          {/* Dropdown Menu */}
          {isMenuOpen && (
            <div className="absolute top-20 left-0 w-64 bg-white rounded-xl shadow-2xl border border-gray-200 z-50 overflow-hidden animate-slideIn">
              {/* Menu Items */}
              <div className="py-2">
                <button
                  onClick={handleProfile}
                  className="w-full px-4 py-3 text-left hover:bg-gray-50 transition-colors flex items-center gap-3 text-gray-700"
                >
                  <span className="text-xl">👤</span>
                  <span className="font-medium">Profilim</span>
                </button>

                <button
                  onClick={handleSettings}
                  className="w-full px-4 py-3 text-left hover:bg-gray-50 transition-colors flex items-center gap-3 text-gray-700"
                >
                  <span className="text-xl">⚙️</span>
                  <span className="font-medium">Ayarlar</span>
                </button>

                <button
                  onClick={handleSubscription}
                  className="w-full px-4 py-3 text-left hover:bg-gradient-to-r hover:from-purple-50 hover:to-blue-50 transition-colors flex items-center gap-3"
                >
                  <span className="text-xl">💳</span>
                  <span className="font-medium bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
                    Abonelik / Plan Yükselt
                  </span>
                </button>

                <button
                  onClick={handleHelp}
                  className="w-full px-4 py-3 text-left hover:bg-gray-50 transition-colors flex items-center gap-3 text-gray-700"
                >
                  <span className="text-xl">❓</span>
                  <span className="font-medium">Yardım Merkezi</span>
                </button>

                {/* Divider */}
                <div className="my-2 border-t border-gray-200"></div>

                {/* Logout */}
                <button
                  onClick={handleLogout}
                  className="w-full px-4 py-3 text-left hover:bg-red-50 transition-colors flex items-center gap-3 text-red-600"
                >
                  <span className="text-xl">🚪</span>
                  <span className="font-semibold">Çıkış Yap</span>
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Sağ Taraf: Aksiyon Butonları + Divider + Bell Icon */}
        <div className="flex items-center gap-3 w-full md:w-auto justify-end">
          <button
            onClick={handleNewTest}
            className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-xl font-semibold hover:scale-105 transition-transform shadow-lg whitespace-nowrap"
          >
            ➕ Yeni Test Ekle
          </button>

          <button
            onClick={handlePastTests}
            className="px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-xl font-semibold hover:scale-105 transition-transform shadow-lg whitespace-nowrap"
          >
            📝 Geçmiş Testlerim
          </button>

          {/* Vertical Divider */}
          <div className="h-10 w-px bg-gray-300 mx-2"></div>

          {/* Bell Icon with Professional Badge */}
          {studentId && <NotificationBell studentId={studentId} />}
        </div>
      </div>
    </div>
  );
}
export default React.memo(DashboardHeader);
