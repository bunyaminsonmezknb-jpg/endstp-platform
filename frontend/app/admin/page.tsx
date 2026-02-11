// frontend/app/admin/page.tsx
'use client';

import { useRouter } from 'next/navigation';

type AdminCard = {
  title: string;
  desc: string;
  icon: string;
  href: string;
  gradient: string;
  border: string;
};

export default function AdminHomePage() {
  const router = useRouter();

  const cards: AdminCard[] = [
    {
      title: 'Feature Flags',
      desc: 'Kill-switch / health kontrollü flag yönetimi',
      icon: '🚦',
      href: '/admin/feature-flags',
      gradient: 'from-purple-600 to-blue-600',
      border: 'border-purple-500',
    },
    {
      title: 'Dashboard Settings',
      desc: 'Kart görünürlüğü / admin dashboard ayarları',
      icon: '🧩',
      href: '/admin/dashboard-settings',
      gradient: 'from-green-600 to-emerald-600',
      border: 'border-green-500',
    },
    {
      title: 'Audit Log',
      desc: 'Admin aksiyon geçmişi (before/after state)',
      icon: '🧾',
      href: '/admin/audit-log',
      gradient: 'from-orange-600 to-red-600',
      border: 'border-orange-500',
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-6xl mx-auto px-4 py-5 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              End.STP Admin
            </h1>
            <p className="text-sm text-gray-500">Phase-1 Admin Panel</p>
          </div>

          <button
            onClick={() => router.push('/student/dashboard')}
            className="px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-lg transition"
          >
            ← Öğrenci Paneli
          </button>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-10">
        {/* Intro */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-8">
          <div className="flex items-start gap-4">
            <div className="text-4xl">🛡️</div>
            <div>
              <h2 className="text-xl font-bold text-gray-900 mb-1">
                Admin Kontrol Merkezi
              </h2>
              <p className="text-gray-600">
                Phase-1 kapsamı: Feature flags (kill-switch), dashboard ayarları ve audit trail.
              </p>
            </div>
          </div>
        </div>

        {/* Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {cards.map((c) => (
            <button
              key={c.href}
              onClick={() => router.push(c.href)}
              className={`text-left bg-white rounded-2xl shadow-lg border-l-4 ${c.border} hover:shadow-xl transition p-6 group`}
            >
              <div className="flex items-start justify-between mb-4">
                <div className="text-5xl">{c.icon}</div>
                <div
                  className={`px-3 py-1 rounded-full text-xs font-semibold text-white bg-gradient-to-r ${c.gradient}`}
                >
                  Open
                </div>
              </div>

              <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:translate-x-0.5 transition">
                {c.title}
              </h3>
              <p className="text-gray-600">{c.desc}</p>

              <div className="mt-6 text-sm font-semibold text-gray-700">
                Devam →
              </div>
            </button>
          ))}
        </div>

        {/* Quick Tips */}
        <div className="mt-10 bg-white rounded-2xl shadow-lg p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-3">⚡ Hızlı Notlar</h3>
          <ul className="space-y-2 text-gray-700">
            <li>
              • Admin sayfaları middleware tarafından korunur (session yoksa login’e yönlenir).
            </li>
            <li>
              • Backend admin guard: <span className="font-mono text-sm">role=admin</span> kontrolü yapar.
            </li>
            <li>
              • Feature flags güncellemeleri audit log’a yazılır.
            </li>
          </ul>
        </div>
      </main>
    </div>
  );
}
