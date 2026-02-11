// frontend/app/admin/dashboard-settings/page.tsx
// ✅ GUARD COMPLIANT: İdempotency + optimistic updates + error handling

'use client';

import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { api } from '@/lib/api/client';

type DashboardSettings = Record<string, boolean | string | number | null | undefined>;

type PageState = 'loading' | 'ready' | 'error';
type SaveState = 'idle' | 'saving' | 'saved' | 'error';

function unwrap<T>(res: unknown): T {
  if (res && typeof res === 'object' && 'data' in res) return (res as any).data as T;
  return res as T;
}

function isBooleanishKey(key: string) {
  return key.startsWith('show_') || key.startsWith('is_') || key.endsWith('_enabled');
}

export default function DashboardSettingsPage() {
  const [state, setState] = useState<PageState>('loading');
  const [saveState, setSaveState] = useState<SaveState>('idle');
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const [settings, setSettings] = useState<DashboardSettings>({});
  const [original, setOriginal] = useState<DashboardSettings>({});

  // ✅ GUARD: Unmount safety
  const mountedRef = useRef(true);
  useEffect(() => {
    mountedRef.current = true;
    return () => {
      mountedRef.current = false;
    };
  }, []);

  const dirty = useMemo(() => {
    const keys = Object.keys({ ...original, ...settings });
    return keys.some((k) => original[k] !== settings[k]);
  }, [original, settings]);

  const fetchSettings = useCallback(async () => {
    setState('loading');
    setErrorMsg(null);
    setSaveState('idle');

    try {
      const res = await api.get('/admin/dashboard/settings');
      const data = unwrap<DashboardSettings>(res) ?? {};
      
      if (!mountedRef.current) return;

      setSettings(data);
      setOriginal(data);
      setState('ready');
    } catch (e: any) {
      if (!mountedRef.current) return;

      // ✅ GUARD: Error handling
      console.error('[DashboardSettings] Fetch error:', e);
      setState('error');
      setErrorMsg(e?.message ?? 'Dashboard settings could not be loaded');
    }
  }, []);

  const save = useCallback(async () => {
    // ✅ GUARD: Double-submit engeli
    if (saveState === 'saving') return;

    setSaveState('saving');
    setErrorMsg(null);

    // ✅ GUARD: Delta hesapla (sadece değişenleri gönder)
    const delta: DashboardSettings = {};
    const keys = Object.keys({ ...original, ...settings });
    keys.forEach((k) => {
      if (original[k] !== settings[k]) {
        delta[k] = settings[k];
      }
    });

    // Rollback için snapshot
    const rollbackSettings = { ...settings };

    try {
      // ✅ GUARD: Backend'de idempotency olmalı
      // Singleton row olduğu için natural idempotency var
      const res = await api.put('/admin/dashboard/settings', delta);
      const saved = unwrap<DashboardSettings>(res) ?? settings;

      if (!mountedRef.current) return;

      // Backend'den dönen güncel state'i kullan
      setSettings(saved);
      setOriginal(saved);

      setSaveState('saved');

      // ✅ GUARD: Success feedback (1.5s sonra idle)
      setTimeout(() => {
        if (mountedRef.current) setSaveState('idle');
      }, 1500);

    } catch (e: any) {
      if (!mountedRef.current) return;

      // ✅ GUARD: Rollback on error
      setSettings(rollbackSettings);

      setSaveState('error');
      setErrorMsg(e?.message ?? 'Save failed');

      // ✅ GUARD: Error log
      console.error('[DashboardSettings] Save error:', {
        delta,
        error: e?.message,
      });
    }
  }, [settings, original, saveState]);

  const toggle = useCallback((key: string) => {
    setSettings((prev) => ({ ...prev, [key]: !prev[key] }));
    setSaveState('idle');
  }, []);

  useEffect(() => {
    fetchSettings();
  }, [fetchSettings]);

  const keys = useMemo(() => {
    const all = Object.keys(settings || {});
    const meta = new Set(['id', 'created_at', 'updated_at', 'updated_by', 'singleton']);
    const bools = all.filter((k) => typeof settings[k] === 'boolean' || isBooleanishKey(k)).sort();
    const rest = all.filter((k) => !bools.includes(k)).sort();

    return [...bools.filter((k) => !meta.has(k)), ...rest.filter((k) => !meta.has(k))];
  }, [settings]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      <div className="max-w-5xl mx-auto px-4 py-8">
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Dashboard Settings</h1>
            <p className="text-sm text-gray-600">Admin • kart görünürlük / UI ayarları</p>
          </div>

          <div className="flex gap-2 items-center">
            <button
              onClick={fetchSettings}
              className="px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-60"
              disabled={state === 'loading' || saveState === 'saving'}
            >
              Yenile
            </button>

            <button
              onClick={save}
              className={`px-4 py-2 rounded-lg font-semibold transition ${
                dirty
                  ? 'bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-60'
                  : 'bg-gray-200 text-gray-600 cursor-not-allowed'
              }`}
              disabled={!dirty || saveState === 'saving' || state !== 'ready'}
            >
              {saveState === 'saving'
                ? 'Kaydediliyor...'
                : saveState === 'saved'
                ? 'Kaydedildi ✅'
                : 'Kaydet'}
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
              onClick={fetchSettings}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Tekrar Dene
            </button>
          </div>
        )}

        {state === 'ready' && (
          <div className="bg-white rounded-xl shadow overflow-hidden">
            <div className="p-6 border-b">
              <div className="text-sm text-gray-600">
                {dirty ? (
                  <span className="text-orange-600 font-semibold">Değişiklik var • Kaydet</span>
                ) : (
                  <span className="text-green-700 font-semibold">Güncel</span>
                )}
              </div>
            </div>

            <div className="divide-y">
              {keys.map((k) => {
                const v = settings[k];

                // Boolean alanlar: toggle UI
                if (typeof v === 'boolean' || isBooleanishKey(k)) {
                  const checked = Boolean(v);
                  return (
                    <div key={k} className="p-6 flex items-center justify-between gap-4">
                      <div>
                        <div className="font-mono text-sm text-gray-900">{k}</div>
                        <div className="text-xs text-gray-500">boolean</div>
                      </div>

                      <button
                        onClick={() => toggle(k)}
                        className={`w-20 px-3 py-2 rounded-full font-semibold transition ${
                          checked
                            ? 'bg-green-100 text-green-800 hover:bg-green-200'
                            : 'bg-red-100 text-red-800 hover:bg-red-200'
                        }`}
                      >
                        {checked ? 'ON' : 'OFF'}
                      </button>
                    </div>
                  );
                }

                // Diğer alanlar (string/number) - read-only
                return (
                  <div key={k} className="p-6 flex items-center justify-between gap-4">
                    <div>
                      <div className="font-mono text-sm text-gray-900">{k}</div>
                      <div className="text-xs text-gray-500">
                        {v === null ? 'null' : typeof v}
                      </div>
                    </div>

                    <div className="text-sm text-gray-700 max-w-[60%] truncate">
                      {String(v ?? '-')}
                    </div>
                  </div>
                );
              })}

              {keys.length === 0 && (
                <div className="p-10 text-center text-gray-500">
                  Ayar bulunamadı
                </div>
              )}
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