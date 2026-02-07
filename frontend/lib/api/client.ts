// frontend/lib/api/client.ts
'use client';

import { getSupabaseClient } from '@/lib/supabase/client';

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';

export type NormalizedError = {
  code?: string;
  message: string;
  silent?: boolean;
  retryable?: boolean;
  status?: number;
  raw?: unknown;
};

type RequestOptions = {
  signal?: AbortSignal;
  headers?: Record<string, string>;
};

const DEBUG = true; // ✅ Production'da false yap

function dbg(...args: any[]) {
  if (!DEBUG) return;
  // eslint-disable-next-line no-console
  console.debug(...args);
}

function normalizeError(err: any): NormalizedError {
  const code = err?.code || err?.error?.code || err?.data?.code;
  const message =
    err?.message ||
    err?.error?.message ||
    err?.data?.message ||
    'Beklenmeyen bir hata oluştu.';
  const silent = Boolean(err?.silent ?? err?.error?.silent);
  const retryable = Boolean(err?.retryable ?? err?.error?.retryable);
  const status = err?.status ?? err?.error?.status;
  return { code, message, silent, retryable, status, raw: err };
}

function makeSessionNotReadyError(): NormalizedError {
  return {
    code: 'SESSION_NOT_READY',
    message: 'Oturum hazırlanamadı.',
    silent: true,
    retryable: true,
  };
}

function sleep(ms: number, signal?: AbortSignal) {
  return new Promise<void>((resolve, reject) => {
    if (signal?.aborted) return reject(new DOMException('Aborted', 'AbortError'));
    const t = setTimeout(resolve, ms);
    signal?.addEventListener(
      'abort',
      () => {
        clearTimeout(t);
        reject(new DOMException('Aborted', 'AbortError'));
      },
      { once: true }
    );
  });
}

/**
 * Token retry logic - Simplified & Reliable
 */
async function getAccessTokenWithRetry(opts?: {
  signal?: AbortSignal;
  attempts?: number;
  baseDelayMs?: number;
  maxDelayMs?: number;
}): Promise<string> {
  const attempts = opts?.attempts ?? 3; // ⭐ 10'dan 3'e düşürüldü
  const baseDelayMs = opts?.baseDelayMs ?? 500;
  const maxDelayMs = opts?.maxDelayMs ?? 2000;
  const signal = opts?.signal;

  const supabase = getSupabaseClient();
  let lastErr: any = null;

  for (let i = 0; i < attempts; i++) {
    if (signal?.aborted) throw new DOMException('Aborted', 'AbortError');

    dbg(`[AUTH] getSession attempt ${i + 1}/${attempts}`);

    try {
      const { data, error } = await supabase.auth.getSession();

      const hasSession = !!data?.session;
      const hasToken = !!data?.session?.access_token;

      dbg('[AUTH] getSession result', {
        hasSession,
        hasToken,
        error: error?.message ?? null,
      });

      if (error) {
        lastErr = normalizeError(error);
        throw lastErr;
      }

      const token = data?.session?.access_token;
      if (token) {
        dbg('[AUTH] ✅ Token obtained');
        return token;
      }

      lastErr = makeSessionNotReadyError();
    } catch (e: any) {
      lastErr = normalizeError(e);
      dbg('[AUTH] getSession exception', lastErr);
    }

    // ⭐ Son attempt'te sleep atla
    if (i < attempts - 1) {
      const delay = Math.min(maxDelayMs, baseDelayMs * Math.pow(2, i));
      dbg('[AUTH] sleep', delay);
      await sleep(delay, signal);
    }
  }

  dbg('[AUTH] ❌ token FAILED after all attempts', lastErr ?? makeSessionNotReadyError());
  throw lastErr ?? makeSessionNotReadyError();
}

function normalizeUrl(baseUrl: string, endpoint: string) {
  const b = baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl;
  const e = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
  return `${b}${e}`;
}

async function request<T>(
  method: HttpMethod,
  endpoint: string,
  body?: any,
  options?: RequestOptions
): Promise<T> {
  dbg('[API] request start', method, endpoint);

  const signal = options?.signal;

  // 1. Get token with retry
  let token: string;
  try {
    token = await getAccessTokenWithRetry({ signal });
    dbg('[API] token ok (len)', token?.length ?? 0);
  } catch (err: any) {
    const ne = normalizeError(err);
    dbg('[API] token FAIL', ne);
    throw ne;
  }

  // 2. Build headers
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`,
    ...(options?.headers ?? {}),
  };

  // 3. Build URL
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
  if (!baseUrl) {
    const e = {
      code: 'API_BASE_URL_MISSING',
      message: 'NEXT_PUBLIC_API_BASE_URL is missing',
      silent: false,
      retryable: false,
    };
    dbg('[API] baseUrl missing', e);
    throw e;
  }

  const url = normalizeUrl(baseUrl, endpoint);
  dbg('[API] url', url);

  // 4. Make request
  let res: Response;
  try {
    res = await fetch(url, {
      method,
      headers,
      body: body !== undefined ? JSON.stringify(body) : undefined,
      signal,
    });
    dbg('[API] fetch done', res.status, method, endpoint);
  } catch (err: any) {
    const ne = normalizeError(err);
    dbg('[API] fetch exception', ne);
    throw ne;
  }

  // 5. Parse response
  let data: any = null;
  const contentType = res.headers.get('content-type') || '';
  if (contentType.includes('application/json')) {
    try {
      data = await res.json();
    } catch {
      data = null;
    }
  } else {
    try {
      data = await res.text();
    } catch {
      data = null;
    }
  }

  // 6. Handle errors
  if (!res.ok) {
    const errObj: NormalizedError = {
      code: data?.code || data?.error?.code,
      message: data?.message || data?.error?.message || `HTTP ${res.status}`,
      silent: Boolean(data?.silent),
      retryable: Boolean(data?.retryable),
      status: res.status,
      raw: data,
    };
    dbg('[API] response not ok', errObj);
    throw errObj;
  }

  return data as T;
}

// ⭐ API Export (Kapsamlı)
export const api = {
  get: <T>(endpoint: string, options?: RequestOptions) =>
    request<T>('GET', endpoint, undefined, options),
  post: <T>(endpoint: string, body?: any, options?: RequestOptions) =>
    request<T>('POST', endpoint, body, options),
  put: <T>(endpoint: string, body?: any, options?: RequestOptions) =>
    request<T>('PUT', endpoint, body, options),
  delete: <T>(endpoint: string, options?: RequestOptions) =>
    request<T>('DELETE', endpoint, undefined, options),
};