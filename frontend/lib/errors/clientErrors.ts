export type ClientError =
  | { type: 'SESSION_NOT_READY' }
  | { type: 'UNAUTHORIZED' }
  | { type: 'NETWORK_ERROR' }
  | { type: 'UNKNOWN'; raw?: any }

export function normalizeClientError(err: any): ClientError {
  if (!err) return { type: 'UNKNOWN' }

  if (err.code === 'SESSION_NOT_READY' || err.status === 'SESSION_NOT_READY') {
    return { type: 'SESSION_NOT_READY' }
  }

  if (err.status === 401) {
    return { type: 'UNAUTHORIZED' }
  }

  if (err instanceof TypeError) {
    return { type: 'NETWORK_ERROR' }
  }

  return { type: 'UNKNOWN', raw: err }
}
