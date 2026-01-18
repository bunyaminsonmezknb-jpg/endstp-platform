/**
 * API Client – Supabase Session Guarded (L5)
 */
import { getUserTimezone } from '@/lib/utils/timezone';
import { getSupabaseClient } from '@/lib/supabase/client';

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

interface RequestOptions extends RequestInit {
  headers?: Record<string, string>;
}

export async function apiRequest<T>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<T> {
  const supabase = getSupabaseClient();
  const { data: { session } } = await supabase.auth.getSession();

  const token = session?.access_token;

  // ⚠️ Session henüz hazır değil
  if (!token) {
    throw {
      code: 'SESSION_NOT_READY',
      silent: true,
    };
  }

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    'X-User-Timezone': getUserTimezone(),
    Authorization: `Bearer ${token}`,
    ...options.headers,
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let errorBody: any = {};
    try {
      errorBody = await response.json();
    } catch {}

    if (response.status === 401) {
      await supabase.auth.signOut();
      window.location.href = '/login';
    }

    throw {
      status: response.status,
      body: errorBody,
    };
  }

  return response.json();
}


export const api = {
  get: <T>(endpoint: string) => apiRequest<T>(endpoint, { method: 'GET' }),
  post: <T>(endpoint: string, body?: any) =>
    apiRequest<T>(endpoint, {
      method: 'POST',
      body: body ? JSON.stringify(body) : undefined,
    }),
  put: <T>(endpoint: string, body?: any) =>
    apiRequest<T>(endpoint, {
      method: 'PUT',
      body: body ? JSON.stringify(body) : undefined,
    }),
  delete: <T>(endpoint: string) => apiRequest<T>(endpoint, { method: 'DELETE' }),
};
