'use client';

import { Fragment, useEffect, useMemo, useState } from 'react';
import { api } from '@/lib/api/client';

type AuditLogItem = {
  id: string;
  created_at: string;
  actor_id?: string | null;
  actor_email?: string | null;
  action_type: string;
  entity: string;
  entity_id?: string | null;
  request_id?: string | null;
  ip?: string | null;
  user_agent?: string | null;
  payload?: any;
  diff?: any;
};

type ApiResp = {
  items: AuditLogItem[];
  next_cursor?: string | null;
};

type PageState = 'loading' | 'ready' | 'error';

function unwrap<T>(res: unknown): T {
  if (res && typeof res === 'object' && 'data' in res) return (res as any).data as T;
  return res as T;
}

function fmt(ts: string) {
  try {
    const d = new Date(ts);
    return d.toLocaleString();
  } catch {
    return ts;
  }
}

function buildQuery(params: Record<string, string | number | boolean | null | undefined>) {
  const sp = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) {
    if (v === undefined || v === null || v === '') continue;
    sp.set(k, String(v));
  }
  const qs = sp.toString();
  return qs ? `?${qs}` : '';
}

export default function AuditLogPage() {
  const [state, setState] = useState<PageState>('loading');
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const [q, setQ] = useState('');
  const [entity, setEntity] = useState('');
  const [actionType, setActionType] = useState('');

  const [items, setItems] = useState<AuditLogItem[]>([]);
  const [nextCursor, setNextCursor] = useState<string | null>(null);
  const [loadingMore, setLoadingMore] = useState(false);

  const [openId, setOpenId] = useState<string | null>(null);

  const entities = useMemo(() => {
    const set = new Set(items.map((i) => i.entity).filter(Boolean));
    return Array.from(set).sort();
  }, [items]);

  const actions = useMemo(() => {
    const set = new Set(items.map((i) => i.action_type).filter(Boolean));
    return Array.from(set).sort();
  }, [items]);

  async function fetchFirst() {
    setState('loading');
    setErrorMsg(null);
    setOpenId(null);

    try {
      const qs = buildQuery({
        q: q || undefined,
        entity: entity || undefined,
        action_type: actionType || undefined,
        limit: 50,
      });

      const res = await api.get(`/admin/audit-log${qs}`);
      const data = unwrap<ApiResp>(res) ?? { items: [], next_cursor: null };

      setItems(Array.isArray(data.items) ? data.items : []);
      setNextCursor(data.next_cursor ?? null);
      setState('ready');
    } catch (e: any) {
      setState('error');
      setErrorMsg(e?.message ?? 'Audit log could not be loaded');
    }
  }

  async function loadMore() {
    if (!nextCursor || loadingMore) return;
    setLoadingMore(true);
    setErrorMsg(null);

    try {
      const qs = buildQuery({
        q: q || undefined,
        entity: entity || undefined,
        action_type: actionType || undefined,
        limit: 50,
        cursor: nextCursor,
      });

      const res = await api.get(`/admin/audit-log${qs}`);
      const data = unwrap<ApiResp>(res) ?? { items: [], next_cursor: null };

      const more = Array.isArray(data.items) ? data.items : [];
      setItems((prev) => [...prev, ...more]);
      setNextCursor(data.next_cursor ?? null);
    } catch (e: any) {
      setErrorMsg(e?.message ?? 'Load more failed');
    } finally {
      setLoadingMore(false);
    }
  }

  useEffect(() => {
    fetchFirst();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Audit Log</h1>
            <p className="text-sm text-gray-600">Admin aksiyon geçmişi (append-only)</p>
          </div>

          <div className="flex flex-col md:flex-row gap-2 md:items-center">
            <input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="Ara: TOGGLE_FEATURE, feature_flags, admin@email..."
              className="w-full md:w-80 px-4 py-2 border border-gray-300 rounded-lg"
            />

            <select
              value={entity}
              onChange={(e) => setEntity(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg bg-white"
            >
              <option value="">Entity (tümü)</option>
              {entities.map((v) => (
                <option key={v} value={v}>
                  {v}
                </option>
              ))}
            </select>

            <select
              value={actionType}
              onChange={(e) => setActionType(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg bg-white"
            >
              <option value="">Action (tümü)</option>
              {actions.map((v) => (
                <option key={v} value={v}>
                  {v}
                </option>
              ))}
            </select>

            <button
              onClick={fetchFirst}
              className="px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
              disabled={state === 'loading'}
            >
              Filtrele
            </button>
          </div>
        </div>

        {state === 'loading' && (
          <div className="bg-white rounded-xl shadow p-6">
            <div className="animate-pulse text-gray-500">Yükleniyor...</div>
          </div>
        )}

        {state === 'error' && (
          <div className="bg-white rounded-xl shadow p-6">
            <div className="text-red-600 font-semibold mb-2">Hata</div>
            <div className="text-gray-700 mb-4">{errorMsg}</div>
            <button
              onClick={fetchFirst}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Tekrar Dene
            </button>
          </div>
        )}

        {state === 'ready' && (
          <div className="bg-white rounded-xl shadow overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-100">
                  <tr>
                    <th className="text-left px-6 py-3 text-sm font-semibold text-gray-700">Zaman</th>
                    <th className="text-left px-6 py-3 text-sm font-semibold text-gray-700">Actor</th>
                    <th className="text-left px-6 py-3 text-sm font-semibold text-gray-700">Action</th>
                    <th className="text-left px-6 py-3 text-sm font-semibold text-gray-700">Entity</th>
                    <th className="text-left px-6 py-3 text-sm font-semibold text-gray-700">Entity ID</th>
                    <th className="text-center px-6 py-3 text-sm font-semibold text-gray-700">Detay</th>
                  </tr>
                </thead>

                <tbody>
                  {items.map((it) => {
                    const isOpen = openId === it.id;
                    return (
                      <Fragment key={it.id}>
                        <tr className="border-t">
                          <td className="px-6 py-4 text-sm text-gray-800 whitespace-nowrap">
                            {fmt(it.created_at)}
                          </td>
                          <td className="px-6 py-4 text-sm text-gray-800">
                            <div className="font-medium">{it.actor_email ?? '-'}</div>
                            <div className="text-xs text-gray-500 font-mono">{it.actor_id ?? ''}</div>
                          </td>
                          <td className="px-6 py-4 text-sm">
                            <span className="px-3 py-1 rounded-full bg-blue-50 text-blue-700 font-semibold">
                              {it.action_type}
                            </span>
                          </td>
                          <td className="px-6 py-4 text-sm text-gray-800 font-mono">{it.entity}</td>
                          <td className="px-6 py-4 text-sm text-gray-700 font-mono">{it.entity_id ?? '-'}</td>
                          <td className="px-6 py-4 text-center">
                            <button
                              onClick={() => setOpenId(isOpen ? null : it.id)}
                              className="px-3 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 text-sm"
                            >
                              {isOpen ? 'Kapat' : 'Aç'}
                            </button>
                          </td>
                        </tr>

                        {isOpen && (
                          <tr className="border-t bg-gray-50">
                            <td colSpan={6} className="px-6 py-5">
                              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div className="bg-white border rounded-lg p-4">
                                  <div className="text-sm font-semibold text-gray-800 mb-2">Request</div>
                                  <div className="text-xs text-gray-600 mb-1">
                                    IP: <span className="font-mono">{it.ip ?? '-'}</span>
                                  </div>
                                  <div className="text-xs text-gray-600 mb-3">
                                    UA: <span className="font-mono break-all">{it.user_agent ?? '-'}</span>
                                  </div>
                                  <pre className="text-xs bg-gray-50 border rounded p-3 overflow-auto max-h-80">
{JSON.stringify(it.payload ?? {}, null, 2)}
                                  </pre>
                                </div>

                                <div className="bg-white border rounded-lg p-4">
                                  <div className="text-sm font-semibold text-gray-800 mb-2">Diff</div>
                                  <pre className="text-xs bg-gray-50 border rounded p-3 overflow-auto max-h-80">
{JSON.stringify(it.diff ?? {}, null, 2)}
                                  </pre>
                                </div>
                              </div>
                            </td>
                          </tr>
                        )}
                      </Fragment>
                    );
                  })}

                  {items.length === 0 && (
                    <tr className="border-t">
                      <td colSpan={6} className="px-6 py-10 text-center text-gray-500">
                        Kayıt bulunamadı
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>

            <div className="p-4 border-t flex items-center justify-between">
              <div className="text-sm text-gray-600">
                {items.length} kayıt
                {nextCursor ? ' • daha fazla var' : ' • son'}
              </div>

              <button
                onClick={loadMore}
                disabled={!nextCursor || loadingMore}
                className={`px-4 py-2 rounded-lg font-semibold ${
                  nextCursor && !loadingMore
                    ? 'bg-blue-600 text-white hover:bg-blue-700'
                    : 'bg-gray-200 text-gray-600 cursor-not-allowed'
                }`}
              >
                {loadingMore ? 'Yükleniyor...' : 'Daha Fazla'}
              </button>
            </div>

            {errorMsg && (
              <div className="p-4 border-t bg-red-50 text-red-700 text-sm">{errorMsg}</div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
