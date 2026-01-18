import { useEffect, useRef } from 'react';

interface UsePollingOptions {
  callback: () => Promise<void> | void;
  interval: number;
  enabled?: boolean;
  immediate?: boolean;
  pauseOnHidden?: boolean;
}

/**
 * L5-safe polling hook
 * - Prevents overlapping calls
 * - Silently ignores 401 / silent errors
 * - Pauses on tab hidden
 * - Does NOT cause UI error spam
 */
export function usePolling({
  callback,
  interval,
  enabled = true,
  immediate = false,
  pauseOnHidden = true,
}: UsePollingOptions) {
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const isRunningRef = useRef(false);
  const isStoppedRef = useRef(false);
  const callbackRef = useRef(callback);

  // Keep callback ref fresh
  useEffect(() => {
    callbackRef.current = callback;
  }, [callback]);

  useEffect(() => {
    if (typeof document === 'undefined') return;
    if (!enabled) return;

    const run = async () => {
      if (isRunningRef.current || isStoppedRef.current) return;

      isRunningRef.current = true;
      try {
        await callbackRef.current();
      } catch (err: any) {
        // 🔕 Silent / expected errors
        if (err?.silent || err?.status === 401) {
          // Stop polling until component re-mounts or enabled toggles
          isStoppedRef.current = true;
          return;
        }

        // ❗ Real error – log but don't crash UI
        console.error('🔁 Polling error:', err);
      }
      finally {
        isRunningRef.current = false;
      }
    };

    const start = () => {
      if (intervalRef.current || isStoppedRef.current) return;
      intervalRef.current = setInterval(run, interval);
    };

    const stop = () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };

    const handleVisibilityChange = () => {
      if (!pauseOnHidden) return;
      if (document.hidden) stop();
      else start();
    };

    if (immediate) {
      run();
    }

    start();

    if (pauseOnHidden) {
      document.addEventListener('visibilitychange', handleVisibilityChange);
    }

    return () => {
      stop();
      isStoppedRef.current = false;
      if (pauseOnHidden) {
        document.removeEventListener(
          'visibilitychange',
          handleVisibilityChange
        );
      }
    };
  }, [enabled, interval, immediate, pauseOnHidden]);
}
