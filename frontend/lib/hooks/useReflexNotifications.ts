'use client';

import { useEffect, useState } from 'react';
import { getSupabaseClient } from '@/lib/supabase/client';

export interface ReflexNotification {
  id: string;
  title?: string;
  message?: string;
  created_at?: string;
  read?: boolean;
  type?: string;
  // diğer alanlar varsa problem değil
  [key: string]: any;
}

export function useReflexNotifications() {
  const [items, setItems] = useState<ReflexNotification[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      setLoading(true);
      setError(null);

      try {
        const supabase = getSupabaseClient();

        // ✅ ÖNEMLİ: RLS'li tablolar için supabase singleton kullanılmalı
        // Burada tablo adı/kolonlar sende farklıysa:
        // - sadece select alanlarını güncelle
        const { data, error } = await supabase
          .from('reflex_notifications')
          .select('*')
          .order('created_at', { ascending: false })
          .limit(20);

        if (cancelled) return;

        if (error) {
          setError(error.message || 'Bildirimler alınamadı.');
          setItems([]);
          return;
        }

        setItems((data as any) ?? []);
      } catch (e: any) {
        if (cancelled) return;
        setError(e?.message || 'Bildirimler alınamadı.');
        setItems([]);
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    void load();
    return () => {
      cancelled = true;
    };
  }, []);

  return { items, loading, error };
}
