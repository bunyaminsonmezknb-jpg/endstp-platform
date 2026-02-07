// frontend/components/FloatingFeatureMonitor.tsx
'use client';

import { useEffect, useRef, useState } from 'react';
import { api } from '@/lib/api/client';
import { getSupabaseClient } from '@/lib/supabase/client'; // ⭐ DEĞİŞTİ

function sleep(ms: number) {
  return new Promise<void>((r) => setTimeout(r, ms));
}

export default function FloatingFeatureMonitor() {
  const [status, setStatus] = useState<any>(null);
  const [visible, setVisible] = useState(false);
  const [showPopup, setShowPopup] = useState(false);

  const popupTimerRef = useRef<any>(null);

  useEffect(() => {
    let cancelled = false;
    let interval: any = null;

    const clearPopupTimer = () => {
      if (popupTimerRef.current) {
        clearTimeout(popupTimerRef.current);
        popupTimerRef.current = null;
      }
    };

    const applyStatusToUI = (response: any) => {
      setStatus(response);

      if (response?.critical_count > 0 || response?.high_count > 0) {
        setVisible(true);
        setShowPopup(true);

        clearPopupTimer();
        popupTimerRef.current = setTimeout(() => {
          if (!cancelled) setShowPopup(false);
        }, 10000);
      } else {
        setVisible(false);
        setShowPopup(false);
      }
    };

    const checkHealthOnce = async () => {
      const response = (await api.get('/flags/health-status')) as any;
      if (cancelled) return;
      applyStatusToUI(response);
    };

    const checkHealthWithRetry = async () => {
      const delays = [0, 1000, 2000, 5000];

      for (const d of delays) {
        if (cancelled) return;

        if (d) await sleep(d);

        try {
          await checkHealthOnce();
          return;
        } catch (error: any) {
          if (error?.code === 'SESSION_NOT_READY' || error?.silent) return;
          if (error?.status === 401) return;

          if (d === 0) {
            console.error('Health check failed:', error);
          }
        }
      }
    };

    (async () => {
      // ⭐ Session check (basit)
      try {
        const supabase = getSupabaseClient();
        const { data: { session } } = await supabase.auth.getSession();
        
        if (!session) {
          console.debug('FloatingFeatureMonitor: No session, skipping');
          return;
        }
      } catch (e) {
        console.debug('FloatingFeatureMonitor: Auth check failed, skipping');
        return;
      }

      if (cancelled) return;

      await checkHealthWithRetry();

      interval = setInterval(() => {
        checkHealthWithRetry();
      }, 30000);
    })();

    return () => {
      cancelled = true;
      clearPopupTimer();
      if (interval) clearInterval(interval);
    };
  }, []);

  if (!visible || !status) return null;

  const criticalCount = (status?.critical_count || 0) + (status?.high_count || 0);

  return (
    <>
      {/* Floating Badge */}
      <div className="fixed bottom-8 right-8 z-50">
        <button
          onClick={() => window.open('/internal/feature-control', '_blank')}
          className="relative bg-gradient-to-r from-red-600 to-orange-600 text-white rounded-full w-16 h-16 shadow-2xl hover:scale-110 transition-transform animate-pulse"
          title="Open Feature Control Panel"
        >
          <div className="text-2xl">🔔</div>
          {criticalCount > 0 && (
            <div className="absolute -top-2 -right-2 bg-red-600 text-white text-xs font-bold rounded-full w-6 h-6 flex items-center justify-center border-2 border-white">
              {criticalCount}
            </div>
          )}
        </button>
      </div>

      {/* Alert Popup */}
      {showPopup && status?.critical_flags && status.critical_flags.length > 0 && (
        <div className="fixed bottom-28 right-8 z-50 bg-white rounded-xl shadow-2xl border-2 border-red-500 p-4 w-80 animate-slide-up">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <span className="text-2xl">🚨</span>
              <span className="font-bold text-red-600">CRITICAL ALERTS</span>
            </div>
            <button
              onClick={() => setShowPopup(false)}
              className="text-gray-400 hover:text-gray-600 text-xl leading-none"
            >
              ×
            </button>
          </div>

          <div className="space-y-2 mb-3">
            {status.critical_flags.slice(0, 3).map((flag: any) => (
              <div key={flag.flag_key} className="bg-red-50 border border-red-200 rounded p-2">
                <div className="text-sm font-bold text-red-800">{flag.flag_key}</div>
                <div className="text-xs text-red-600">
                  Health: {flag.health_score} | Errors: {flag.error_count}
                </div>
                <div className="text-xs text-red-500 mt-1">
                  {String(flag.severity || '').toUpperCase()} • {flag.user_impact} impact
                </div>
              </div>
            ))}
          </div>

          <button
            onClick={() => window.open('/internal/feature-control', '_blank')}
            className="w-full bg-red-600 hover:bg-red-700 text-white py-2 rounded font-bold text-sm transition"
          >
            Open Control Panel →
          </button>
        </div>
      )}
    </>
  );
}