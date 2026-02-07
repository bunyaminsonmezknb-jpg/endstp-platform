'use client';

import Sidebar from '@/app/components/Sidebar';
import { useAuthReady } from '@/lib/hooks/useAuthReady';

function StudentBootstrapScreen() {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
      <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-6 w-full max-w-md">
        <div className="flex items-center gap-3 mb-3">
          <div className="h-10 w-10 rounded-xl bg-gray-100 flex items-center justify-center">
            <span className="text-xl">⏳</span>
          </div>
          <div>
            <div className="font-bold text-gray-900">Oturum hazırlanıyor</div>
            <div className="text-sm text-gray-500">
              Güvenli oturum anahtarı yükleniyor…
            </div>
          </div>
        </div>

        <div className="h-2 w-full bg-gray-100 rounded-full overflow-hidden">
          <div className="h-full w-1/2 bg-gray-300 animate-pulse" />
        </div>

        <div className="text-xs text-gray-500 mt-3">
          Bu ekran, “SESSION_NOT_READY” durumunda sayfaların API çağrısı yapmasını engeller.
        </div>
      </div>
    </div>
  );
}

export default function StudentLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  // ✅ Auth guard middleware’de
  // ✅ Burada auth kontrolü yok; sadece "session bootstrap ready" gate var
  const { ready } = useAuthReady();

  // Session hazır değilken hiçbir student sayfası mount olmaz → SESSION_NOT_READY kesilir
  if (!ready) return <StudentBootstrapScreen />;


  return (
    <div className="min-h-screen bg-gray-50 flex justify-center">
      <div className="flex">
        <Sidebar />

        <main className="min-h-screen">
          <div className="max-w-[1280px] w-full px-6">{children}</div>
        </main>
      </div>
    </div>
  );
}
