import { normalizeClientError } from '@/lib/errors/clientErrors'

export function handleClientError(
  err: any,
  options?: {
    onUnauthorized?: () => void
    onShowError?: () => void
  }
) {
  const normalized = normalizeClientError(err)

  // 🟡 SESSION_NOT_READY → sessizce yut
  if (normalized.type === 'SESSION_NOT_READY') {
    return
  }

  // 🔴 UNAUTHORIZED → üst seviye zaten yakalıyor
  if (normalized.type === 'UNAUTHORIZED') {
    options?.onUnauthorized?.()
    return
  }

  // 🔴 GERÇEK HATALAR
  options?.onShowError?.()
}
