'use client';

import { createBrowserClient } from '@supabase/ssr';
import type { SupabaseClient } from '@supabase/supabase-js';

// Global type declarations
declare global {
  // eslint-disable-next-line no-var
  var __endstp_supabase__: SupabaseClient | undefined;
}

export function getSupabaseClient(): SupabaseClient {
  if (globalThis.__endstp_supabase__) {
    return globalThis.__endstp_supabase__;
  }

  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  if (!url || !anonKey) {
    throw new Error('Missing NEXT_PUBLIC_SUPABASE_URL or NEXT_PUBLIC_SUPABASE_ANON_KEY');
  }

  const client = createBrowserClient(url, anonKey);

  globalThis.__endstp_supabase__ = client;
  return client;
}

// Backward compatibility export
export const supabase = getSupabaseClient();