'use client';

import Sidebar from '@/app/components/Sidebar';

export default function StudentLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  // ✅ DOĞRU: Auth kontrolü KALDIRILDI
  // ❌ useEffect + localStorage kontrolü KALDIRILDI
  // Auth guard middleware'de yapılıyor

  return (
    <div className="min-h-screen bg-gray-50 flex justify-center">
      <div className="flex">
        <Sidebar />

        <main className="min-h-screen">
          <div className="max-w-[1280px] w-full px-6">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
