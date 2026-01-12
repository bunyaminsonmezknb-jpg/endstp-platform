// src/lib/auth/session.ts
import { api } from '@/lib/api/client';

export class AuthError extends Error {
  constructor() {
    super('AUTH_REQUIRED');
  }
}

/**
 * Frontend için tek ve zorunlu auth kapısı
 * - Token / cookie / session işi api-client + backend’e bırakılır
 * - Yetkisizse AuthError fırlatır
 */
export async function requireAuth<TUser = { id: string; email?: string }>() {
  try {
    const user = await api.get<TUser>('/api/v1/auth/me');
    return { user };
  } catch (err: any) {
    if (err?.status === 401) {
      throw new AuthError();
    }
    throw err;
  }
}
