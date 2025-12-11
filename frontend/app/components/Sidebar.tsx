'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import Logo from './Logo';

const menuItems = [
  { icon: '🏠', label: 'Dashboard', href: '/student/dashboard' },
  { icon: '📝', label: 'Test Girişi', href: '/student/test-entry' },
  { icon: '📊', label: 'Analiz Merkezi', href: '/student/analytics' },
  { icon: '🎯', label: 'Görevlerim', href: '/student/tasks' },
  { icon: '📚', label: 'Konu Haritası', href: '/student/topics' },
  { icon: '📖', label: 'Geçmiş Testler', href: '/student/past-tests' },
  { icon: '⚙️', label: 'Ayarlar', href: '/student/settings' },
];

export default function Sidebar() {
  const pathname = usePathname();

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

      {/* Footer - User */}
      <div className="p-4 border-t border-gray-200">
        <div className="flex items-center gap-3 px-4 py-3">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-bold">
            DÖ
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-semibold text-gray-900 truncate">Demo Öğrenci</p>
            <p className="text-xs text-gray-500 truncate">demo@endstp.com</p>
          </div>
        </div>
      </div>
    </aside>
  );
}