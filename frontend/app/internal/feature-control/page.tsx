'use client';
import { useState, useEffect } from 'react';
import { api } from '@/lib/api/client';
import { useFeatureFlag } from '@/hooks/useFeatureFlag';  // ✅ DÜZELTİLDİ

interface FeatureFlag {
  id: string;
  flag_key: string;
  is_enabled: boolean;
  description: string;
  phase: string;
  health_score: number;
  error_count: number;
  last_error_at: string | null;
  disabled_reason: string | null;
}

const ACCESS_CODE = 'endstp2025';

export default function FeatureControlPage() {
  const [authenticated, setAuthenticated] = useState(false);
  const [flags, setFlags] = useState<FeatureFlag[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (authenticated) {
      fetchFlags();
    }
  }, [authenticated]);

  const fetchFlags = async () => {
    setLoading(true);
    try {
      const response = await api.get('/flags/admin') as any;
      setFlags(response.flags || []);
    } catch (error) {
      console.error('Failed to fetch flags:', error);
    } finally {
      setLoading(false);
    }
  };

  const toggleFlag = async (flagKey: string) => {
    const reason = flags.find(f => f.flag_key === flagKey)?.is_enabled
      ? prompt('❗ Reason for disabling:')
      : null;
    
    if (flags.find(f => f.flag_key === flagKey)?.is_enabled && !reason) {
      return; // Cancelled
    }

    try {
      await api.post(`/flags/${flagKey}/toggle`, { reason });
      fetchFlags();
    } catch (error) {
      console.error('Failed to toggle:', error);
    }
  };

  const getHealthColor = (score: number) => {
    if (score >= 80) return 'bg-green-100 text-green-800 border-green-200';
    if (score >= 50) return 'bg-yellow-100 text-yellow-800 border-yellow-200';
    return 'bg-red-100 text-red-800 border-red-200';
  };

  const getPhaseColor = (phase: string) => {
    if (phase === 'mvp') return 'bg-blue-100 text-blue-800';
    if (phase === 'v1.1') return 'bg-purple-100 text-purple-800';
    return 'bg-gray-100 text-gray-800';
  };

  // Login screen
  if (!authenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-800 to-indigo-900 flex items-center justify-center">
        <div className="bg-white rounded-2xl p-8 shadow-2xl w-96">
          <div className="text-center mb-6">
            <div className="text-4xl mb-2">🎛️</div>
            <h1 className="text-2xl font-bold text-gray-800">Feature Control</h1>
            <p className="text-sm text-gray-500 mt-1">Internal Access Only</p>
          </div>
          <input
            type="password"
            placeholder="Access code"
            className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-purple-600 focus:outline-none text-center text-lg font-mono"
            onKeyDown={(e) => {
              if (e.key === 'Enter' && e.currentTarget.value === ACCESS_CODE) {
                setAuthenticated(true);
              }
            }}
            autoFocus
          />
          <p className="text-xs text-gray-400 mt-3 text-center">End.STP Internal Tool</p>
        </div>
      </div>
    );
  }

  // Control panel
  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-800">🎛️ Feature Control Panel</h1>
            <p className="text-gray-600 mt-1">Health-aware feature management • Internal only</p>
          </div>
          <button
            onClick={() => fetchFlags()}
            disabled={loading}
            className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50"
          >
            {loading ? '⏳' : '🔄'} Refresh
          </button>
        </div>

        {/* Flags */}
        <div className="space-y-4">
          {flags.map((flag) => (
            <div
              key={flag.id}
              className="bg-white rounded-xl border-2 border-gray-200 p-6 hover:border-purple-300 transition"
            >
              {/* Header */}
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <h3 className="text-lg font-bold text-gray-800">
                      {flag.flag_key}
                    </h3>
                    <span className={`px-2 py-0.5 rounded-full text-xs font-bold uppercase ${getPhaseColor(flag.phase)}`}>
                      {flag.phase}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600">{flag.description}</p>
                </div>

                {/* Health Badge */}
                <div className={`px-4 py-2 rounded-lg border-2 font-bold ${getHealthColor(flag.health_score)}`}>
                  <div className="text-xs">Health</div>
                  <div className="text-2xl">{flag.health_score}</div>
                </div>
              </div>

              {/* Stats Grid */}
              <div className="grid grid-cols-3 gap-4 mb-4">
                <div className="bg-gray-50 rounded-lg p-3">
                  <div className="text-xs text-gray-500 mb-1">Status</div>
                  <div className="text-xl font-bold">
                    {flag.is_enabled ? '✅ ON' : '❌ OFF'}
                  </div>
                </div>
                <div className="bg-gray-50 rounded-lg p-3">
                  <div className="text-xs text-gray-500 mb-1">Errors</div>
                  <div className="text-xl font-bold text-gray-800">{flag.error_count}</div>
                </div>
                <div className="bg-gray-50 rounded-lg p-3">
                  <div className="text-xs text-gray-500 mb-1">Last Error</div>
                  <div className="text-sm font-semibold text-gray-800">
                    {flag.last_error_at ? new Date(flag.last_error_at).toLocaleDateString('tr-TR') : 'None'}
                  </div>
                </div>
              </div>

              {/* Disabled Reason */}
              {flag.disabled_reason && (
                <div className="bg-red-50 border-2 border-red-200 rounded-lg p-3 mb-4">
                  <div className="text-xs font-bold text-red-800 mb-1">⚠️ DISABLED REASON:</div>
                  <div className="text-sm text-red-700">{flag.disabled_reason}</div>
                </div>
              )}

              {/* Toggle Button */}
              <button
                onClick={() => toggleFlag(flag.flag_key)}
                className={`w-full py-3 rounded-lg font-bold transition shadow-sm ${
                  flag.is_enabled
                    ? 'bg-red-600 hover:bg-red-700 text-white'
                    : 'bg-green-600 hover:bg-green-700 text-white'
                }`}
              >
                {flag.is_enabled ? '🔴 Disable Feature' : '🟢 Enable Feature'}
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}