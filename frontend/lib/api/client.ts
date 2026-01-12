/**
 * API Client - Supabase session kullanır
 */
import { getUserTimezone } from '@/lib/utils/timezone';
import { supabase } from '@/lib/supabase/client';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

interface RequestOptions extends RequestInit {
  headers?: Record<string, string>;
}

export async function apiRequest<T>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<T> {
  // ✅ DOĞRU: Supabase session'dan token al
  const { data: { session } } = await supabase.auth.getSession();
  const token = session?.access_token;

  // Token yoksa hata fırlat
  if (!token) {
    const err: any = new Error('UNAUTHORIZED');
    err.status = 401;
    throw err;
  }

  // Headers birleştir
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    'X-User-Timezone': getUserTimezone(),
    'Authorization': `Bearer ${token}`, // ✅ Token eklendi
    ...options.headers,
  };

  // İstek at
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  // Hata kontrolü (status kaybolmasın)
if (!response.ok) {
  let errorBody: any = {}
  try {
    errorBody = await response.json()
  } catch {}

  // 🔐 GLOBAL 401 INTERCEPTOR (ALTIN STANDART)
  if (response.status === 401) {
    await supabase.auth.signOut()

    if (typeof window !== 'undefined') {
      window.location.href = '/login'
    }
  }

  const err: any = new Error(
    errorBody?.detail ||
    errorBody?.message ||
    `HTTP ${response.status}`
  )

  err.status = response.status
  err.body = errorBody

  throw err
}
  
  return response.json();
}

// Helper fonksiyonlar
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
