// frontend/app/providers.tsx
'use client';

import { useEffect, useState } from 'react';
import { getSupabaseClient } from '@/lib/supabase/client';

export default function Providers({ children }: { children: React.ReactNode }) {
  const [ready, setReady] = useState(false);

  useEffect(() => {
    // ⭐ Basit session check
    async function init() {
      try {
        const supabase = getSupabaseClient();
        await supabase.auth.getSession();
        setReady(true);
      } catch (e) {
        console.error('Providers init failed:', e);
        setReady(true); // Yine de render et
      }
    }

    init();
  }, []);

  if (!ready) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-purple-600 mx-auto mb-4"></div>
          <p className="text-gray-700">Yükleniyor...</p>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}