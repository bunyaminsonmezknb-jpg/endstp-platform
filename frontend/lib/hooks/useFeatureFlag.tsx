'use client';
import React, { useEffect, useState } from 'react';
import { api } from '@/lib/api/client';

interface FeatureFlags {
  [key: string]: boolean;
}

let cachedFlags: FeatureFlags = {};
let flagsPromise: Promise<FeatureFlags> | null = null;

async function fetchFlags(): Promise<FeatureFlags> {
  if (!flagsPromise) {
    flagsPromise = api.get('/flags')
      .then((response: any) => {
        cachedFlags = response.flags || {};
        return cachedFlags;
      })
      .catch((error) => {
        console.error('⚠️ Feature flags fetch error:', error);
        return {};
      });
  }
  return flagsPromise;
}

export function useFeatureFlag(flagKey: string): boolean {
  const [isEnabled, setIsEnabled] = useState<boolean>(() => {
    return cachedFlags[flagKey] ?? false;
  });

  useEffect(() => {
    let active = true;

    fetchFlags().then((flags) => {
      if (active) {
        setIsEnabled(flags[flagKey] ?? false);
      }
    });

    return () => {
      active = false;
    };
  }, [flagKey]);


  return isEnabled;
}

export async function reportFeatureError(flagKey: string, error: Error) {
  try {
    await api.post(`/flags/${flagKey}/report-error`, {
      error_message: error.message
    });
    console.log(`🚨 Reported error for ${flagKey}`);
  } catch (e) {
    console.error('Failed to report feature error:', e);
  }
}

export function withFeatureFlag<P extends object>(
  Component: React.ComponentType<P>,
  flagKey: string
): React.FC<P> {
  return function FeatureFlagWrapper(props: P) {
    const isEnabled = useFeatureFlag(flagKey);
    
    if (!isEnabled) {
      return null;
    }
    
    return <Component {...props} />;
  };
}