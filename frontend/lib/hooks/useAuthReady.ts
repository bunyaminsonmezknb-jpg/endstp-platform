// frontend/lib/hooks/useAuthReady.ts
'use client';

import { useEffect, useState } from 'react';
import type { Session } from '@supabase/supabase-js';
import { getSupabaseClient } from '@/lib/supabase/client';

type AuthReadyState = {
  ready: boolean;
  session: Session | null;
};

export function useAuthReady(): AuthReadyState {
  const [ready, setReady] = useState(false);
  const [session, setSession] = useState<Session | null>(null);

  useEffect(() => {
    let mounted = true;
    const supabase = getSupabaseClient();

    async function init() {
      const { data: { session: initialSession } } = await supabase.auth.getSession();
      
      if (!mounted) return;
      
      setSession(initialSession);
      setReady(true);
    }

    init();

    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (_event, newSession) => {
        if (!mounted) return;
        setSession(newSession);
        setReady(true);
      }
    );

    return () => {
      mounted = false;
      subscription.unsubscribe();
    };
  }, []);

  return { ready, session };
}