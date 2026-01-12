import { useEffect, useRef } from 'react';

interface UsePollingOptions {
  callback: () => Promise<void> | void;
  interval: number;
  enabled?: boolean;
  immediate?: boolean;
  pauseOnHidden?: boolean;
}

export function usePolling({
  callback,
  interval,
  enabled = true,
  immediate = false,
  pauseOnHidden = true,
}: UsePollingOptions) {
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const isRunningRef = useRef(false);
  const callbackRef = useRef(callback);

  // callback güncellendiğinde referansı yenile
  useEffect(() => {
    callbackRef.current = callback;
  }, [callback]);

  useEffect(() => {
    if (typeof document === 'undefined') return;
    if (!enabled) return;

    const run = async () => {
      if (isRunningRef.current) return;
      isRunningRef.current = true;
      try {
        await callbackRef.current();
      } finally {
        isRunningRef.current = false;
      }
    };

    if (immediate) {
      run();
    }

    const startInterval = () => {
      if (intervalRef.current) return;
      intervalRef.current = setInterval(run, interval);
    };

    const stopInterval = () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };

    const handleVisibilityChange = () => {
      if (!pauseOnHidden) return;

      if (document.hidden) {
        stopInterval();
      } else {
        startInterval();
      }
    };

    startInterval();

    if (pauseOnHidden) {
      document.addEventListener('visibilitychange', handleVisibilityChange);
    }

    return () => {
      stopInterval();
      if (pauseOnHidden) {
        document.removeEventListener('visibilitychange', handleVisibilityChange);
      }
    };
  }, [enabled, interval, immediate, pauseOnHidden]);
}
