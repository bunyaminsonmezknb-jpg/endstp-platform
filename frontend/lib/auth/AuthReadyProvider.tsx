'use client';

import React, { createContext, useContext, useEffect, useMemo, useState } from 'react';
import type { Session } from '@supabase/supabase-js';
import { getSupabaseClient } from '@/lib/supabase/client';

type AuthReadyState = {
  ready: boolean;
  session: Session | null;
};

const AuthReadyContext = createContext<AuthReadyState>({ ready: false, session: null });

export function AuthReadyProvider({ children }: { children: React.ReactNode }) {
  const supabase = getSupabaseClient();
  const [ready, setReady] = useState(false);
  const [session, setSession] = useState<Session | null>(null);

  useEffect(() => {
    let mounted = true;

    // 1) İlk session fetch (bootstrap)
    supabase.auth.getSession().then(({ data, error }) => {
      if (!mounted) return;
      if (!error) setSession(data.session ?? null);
      setReady(true); // ✅ “hazırım” bayrağı
    });

    // 2) Session değişimlerini dinle
    const { data: sub } = supabase.auth.onAuthStateChange((_event, newSession) => {
      if (!mounted) return;
      setSession(newSession ?? null);
    });

    return () => {
      mounted = false;
      sub?.subscription?.unsubscribe();
    };
  }, [supabase]);

  const value = useMemo(() => ({ ready, session }), [ready, session]);

  return <AuthReadyContext.Provider value={value}>{children}</AuthReadyContext.Provider>;
}

export function useAuthReadyFromProvider() {
  return useContext(AuthReadyContext);
}
