'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useEffect, useState } from 'react';
import { createBrowserClient } from '@supabase/ssr';
import Logo from './Logo';

const menuItems = [
  { icon: '🏠', label: 'Dashboard', href: '/student/dashboard' },
  { icon: '📝', label: 'Test Girişi', href: '/student/test-entry' },
  { icon: '📊', label: 'Analiz Merkezi', href: '/student/analytics' },
  { icon: '🎯', label: 'Görevlerim', href: '/student/tasks' },
  { icon: '📚', label: 'Konu Haritası', href: '/student/topics' },
  { icon: '📖', label: 'Geçmiş Testler', href: '/student/past-tests' },
  { icon: '📈', label: 'İlerleme & Hedefler', href: '/student/progress' },
];

interface UserInfo {
  email: string;
  role: string;
  firstName?: string;
  lastName?: string;
}

export default function Sidebar() {
  const pathname = usePathname();
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null);
  const [loading, setLoading] = useState(true);

  // ✅ Create Supabase client
  const supabase = createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );

  useEffect(() => {
    async function loadUserInfo() {
      try {
        // 1. Get session
        const { data: { session }, error: sessionError } = await supabase.auth.getSession();
        
        if (sessionError || !session) {
          console.error('❌ [Sidebar] No session');
          setUserInfo(null);
          setLoading(false);
          return;
        }

        // 2. Get profile from user_profiles
        const { data: profile, error: profileError } = await supabase
          .from('user_profiles')
          .select('email, role, first_name, last_name')
          .eq('id', session.user.id)
          .single();

        if (profileError) {
          console.error('❌ [Sidebar] Profile error:', profileError);
          // Fallback: use session email
          setUserInfo({
            email: session.user.email || 'Unknown',
            role: 'student'
          });
          setLoading(false);
          return;
        }

        // 3. Set user info
        setUserInfo({
          email: profile?.email || session.user.email || 'Unknown',
          role: profile?.role || 'student',
          firstName: profile?.first_name,
          lastName: profile?.last_name
        });

        console.log('✅ [Sidebar] User loaded:', profile?.email, profile?.role);

      } catch (err) {
        console.error('❌ [Sidebar] Error:', err);
        setUserInfo(null);
      } finally {
        setLoading(false);
      }
    }

    loadUserInfo();
  }, []);

  // ✅ Helper: Get display name
  const getDisplayName = () => {
    if (!userInfo) return 'User';
    
    if (userInfo.firstName && userInfo.lastName) {
      return `${userInfo.firstName} ${userInfo.lastName}`;
    }
    
    if (userInfo.firstName) {
      return userInfo.firstName;
    }
    
    // Fallback: role-based name
    if (userInfo.role === 'admin') return 'Admin User';
    if (userInfo.role === 'coach') return 'Coach User';
    return 'Demo Öğrenci';
  };

  // ✅ Helper: Get avatar initials
  const getInitials = () => {
    if (!userInfo) return 'U';
    
    if (userInfo.firstName && userInfo.lastName) {
      return `${userInfo.firstName[0]}${userInfo.lastName[0]}`.toUpperCase();
    }
    
    if (userInfo.firstName) {
      return userInfo.firstName[0].toUpperCase();
    }
    
    // Fallback: from email
    return userInfo.email[0].toUpperCase();
  };

  return (
    <aside className="w-60 h-screen bg-white border-r border-gray-200 flex flex-col sticky top-0">
      {/* Logo */}
      <div className="p-6 border-b border-gray-200">
        <Logo size={40} />
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
        {menuItems.map((item) => {
          const isActive = pathname === item.href;
          
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`
                flex items-center gap-3 px-4 py-3 rounded-lg
                transition-all duration-200
                ${isActive 
                  ? 'bg-blue-50 text-blue-600 font-semibold border-l-4 border-blue-600' 
                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                }
              `}
            >
              <span className="text-xl">{item.icon}</span>
              <span className="text-sm">{item.label}</span>
            </Link>
          );
        })}
      </nav>

      {/* Footer - User (GERÇEK SESSION) */}
      <div className="p-4 border-t border-gray-200">
        {loading ? (
          // Loading skeleton
          <div className="flex items-center gap-3 px-4 py-3">
            <div className="w-10 h-10 rounded-full bg-gray-200 animate-pulse" />
            <div className="flex-1 space-y-2">
              <div className="h-4 bg-gray-200 rounded w-24 animate-pulse" />
              <div className="h-3 bg-gray-200 rounded w-32 animate-pulse" />
            </div>
          </div>
        ) : userInfo ? (
          // User info loaded
          <div className="flex items-center gap-3 px-4 py-3">
            <div className={`
              w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-sm
              ${userInfo.role === 'admin' 
                ? 'bg-gradient-to-br from-purple-500 to-pink-600' 
                : 'bg-gradient-to-br from-blue-500 to-purple-600'
              }
            `}>
              {getInitials()}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-semibold text-gray-900 truncate">
                {getDisplayName()}
              </p>
              <p className="text-xs text-gray-500 truncate">
                {userInfo.email}
              </p>
            </div>
            {userInfo.role === 'admin' && (
              <div className="shrink-0 px-2 py-1 bg-purple-100 text-purple-700 text-xs font-semibold rounded">
                Admin
              </div>
            )}
          </div>
        ) : (
          // No session
          <div className="px-4 py-3 text-center">
            <p className="text-xs text-gray-500">Not logged in</p>
            <a 
              href="/login" 
              className="text-xs text-blue-600 hover:underline"
            >
              Login
            </a>
          </div>
        )}
      </div>
    </aside>
  );
}