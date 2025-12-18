'use client';
import { useState, useEffect } from 'react';
import { api } from '@/lib/api/client';

interface GlobalHealth {
  overall_health: number;
  availability: number;
  avg_performance: number;
  total_errors: number;
  error_rate: number;
  worst_user_impact: string;
  critical_count: number;
  degraded_count: number;
  system_status: 'healthy' | 'degraded' | 'critical';
}

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
  disabled_by: string | null;
  disabled_at: string | null;
  component_path: string | null;
  backend_endpoint: string | null;
  related_files: string[] | null;
  fix_guide: string | null;
  error_severity: string;
  user_impact_level: string;
  error_rate_percent: number;
  depends_on: string[] | null;
  blocks: string[] | null;
  latency_score: number | null;
  error_score: number | null;
  freshness_score: number | null;
  data_volume_score: number | null;
  avg_response_time_ms: number | null;
  p95_response_time_ms: number | null;
  rows_processed: number | null;
  cache_hit_rate: number | null;
  last_error_message: string | null;
  last_error_function: string | null;
  last_error_trace: string | null;
}

const ACCESS_CODE = 'endstp2025';

export default function FeatureControlPage() {
  const [authenticated, setAuthenticated] = useState(false);
  const [flags, setFlags] = useState<FeatureFlag[]>([]);
  const [loading, setLoading] = useState(false);
  const [expandedFlags, setExpandedFlags] = useState<Set<string>>(new Set());

  useEffect(() => {
    if (authenticated) {
      fetchFlags();
    }
  }, [authenticated]);

  const calculateGlobalHealth = (flags: FeatureFlag[]): GlobalHealth => {
    if (!flags.length) {
      return {
        overall_health: 100,
        availability: 100,
        avg_performance: 0,
        total_errors: 0,
        error_rate: 0,
        worst_user_impact: 'none',
        critical_count: 0,
        degraded_count: 0,
        system_status: 'healthy'
      };
    }

    const totalHealth = flags.reduce((sum, f) => sum + f.health_score, 0);
    const overall_health = Math.round(totalHealth / flags.length);

    const enabledCount = flags.filter(f => f.is_enabled).length;
    const availability = Math.round((enabledCount / flags.length) * 100);

    const responseTimes = flags.filter(f => f.avg_response_time_ms).map(f => f.avg_response_time_ms!);
    const avg_performance = responseTimes.length > 0 
      ? Math.round(responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length)
      : 0;

    const total_errors = flags.reduce((sum, f) => sum + f.error_count, 0);
    const error_rate = flags.length > 0
      ? Math.round(flags.reduce((sum, f) => sum + (f.error_rate_percent || 0), 0) / flags.length)
      : 0;

    const impactLevels = ['none', 'low', 'medium', 'high', 'critical'];
    const impacts = flags.map(f => f.user_impact_level || 'none');
    const worstImpact = impacts.reduce((worst, current) => 
      impactLevels.indexOf(current) > impactLevels.indexOf(worst) ? current : worst
    , 'none');

    const critical_count = flags.filter(f => 
      f.error_severity === 'critical' || f.health_score < 50
    ).length;
    
    const degraded_count = flags.filter(f => 
      f.health_score >= 50 && f.health_score < 80
    ).length;

    let system_status: 'healthy' | 'degraded' | 'critical' = 'healthy';
    if (critical_count > 0 || overall_health < 50) {
      system_status = 'critical';
    } else if (degraded_count > 0 || overall_health < 80) {
      system_status = 'degraded';
    }

    return {
      overall_health,
      availability,
      avg_performance,
      total_errors,
      error_rate,
      worst_user_impact: worstImpact,
      critical_count,
      degraded_count,
      system_status
    };
  };

  const toggleExpanded = (flagKey: string) => {
    setExpandedFlags(prev => {
      const newSet = new Set(prev);
      if (newSet.has(flagKey)) {
        newSet.delete(flagKey);
      } else {
        newSet.add(flagKey);
      }
      return newSet;
    });
  };

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
    const flag = flags.find(f => f.flag_key === flagKey);
    const reason = flag?.is_enabled ? prompt('❗ Reason for disabling:') : null;
    
    if (flag?.is_enabled && !reason) return;

    try {
      await api.post(`/flags/${flagKey}/toggle`, { reason });
      fetchFlags();
    } catch (error) {
      console.error('Failed to toggle:', error);
    }
  };

  const quickAction = async (flagKey: string, action: string) => {
    try {
      await api.post(`/flags/${flagKey}/quick-action?action=${action}`);
      fetchFlags();
    } catch (error) {
      console.error('Quick action failed:', error);
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

  const getImpactBadge = (impact: string) => {
    const badges: any = {
      critical: { icon: '👥', text: 'ALL USERS', color: 'bg-red-100 text-red-800 border-red-300' },
      high: { icon: '👤', text: 'MANY USERS', color: 'bg-orange-100 text-orange-800 border-orange-300' },
      medium: { icon: '👤', text: 'SOME USERS', color: 'bg-yellow-100 text-yellow-800 border-yellow-300' },
      low: { icon: '✓', text: 'LIMITED', color: 'bg-green-100 text-green-800 border-green-300' },
      none: { icon: '✓', text: 'NONE', color: 'bg-gray-100 text-gray-600 border-gray-300' }
    };
    return badges[impact] || badges.none;
  };

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

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
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

        {/* Global System Health */}
        {flags.length > 0 && (() => {
          const globalHealth = calculateGlobalHealth(flags);
          
          return (
            <div className="mb-8">
              <div className="bg-gradient-to-r from-purple-600 to-indigo-600 rounded-xl shadow-lg p-6 mb-6">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h2 className="text-white text-2xl font-bold mb-1">System Health</h2>
                    <p className="text-purple-100 text-sm">Overall platform status</p>
                  </div>
                  <div className="text-right">
                    <div className={`text-6xl font-bold ${
                      globalHealth.overall_health >= 80 ? 'text-green-400' :
                      globalHealth.overall_health >= 50 ? 'text-yellow-400' :
                      'text-red-400'
                    }`}>
                      {globalHealth.overall_health}
                    </div>
                    <div className={`text-sm font-semibold mt-1 ${
                      globalHealth.system_status === 'healthy' ? 'text-green-300' :
                      globalHealth.system_status === 'degraded' ? 'text-yellow-300' :
                      'text-red-300'
                    }`}>
                      {globalHealth.system_status === 'healthy' && '✅ All Systems Operational'}
                      {globalHealth.system_status === 'degraded' && '⚠️ Degraded Performance'}
                      {globalHealth.system_status === 'critical' && '🚨 Critical Issues'}
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-4 gap-4">
                  {/* Availability */}
                  <div className="bg-white/10 backdrop-blur rounded-lg p-4">
                    <div className="text-purple-200 text-xs mb-1">Availability</div>
                    <div className="text-white text-2xl font-bold">{globalHealth.availability}%</div>
                    <div className="text-purple-300 text-xs mt-1">
                      {flags.filter(f => f.is_enabled).length}/{flags.length} enabled
                    </div>
                  </div>

                  {/* Performance - P95 Added */}
                  <div className="bg-white/10 backdrop-blur rounded-lg p-4">
                    <div className="text-purple-200 text-xs mb-1">Performance</div>
                    <div className={`text-xl font-bold ${
                      globalHealth.avg_performance < 1000 ? 'text-green-400' :
                      globalHealth.avg_performance < 2000 ? 'text-yellow-400' :
                      'text-red-400'
                    }`}>
                      {globalHealth.avg_performance > 0 ? `${globalHealth.avg_performance}ms` : 'N/A'}
                    </div>
                    <div className="text-purple-300 text-xs mt-1">
                      P95: {(() => {
                        const p95Times = flags.filter(f => f.p95_response_time_ms).map(f => f.p95_response_time_ms!);
                        const avgP95 = p95Times.length > 0 ? Math.round(p95Times.reduce((a,b) => a+b, 0) / p95Times.length) : 0;
                        return avgP95 > 0 ? `${avgP95}ms` : 'N/A';
                      })()}
                    </div>
                  </div>

                  {/* Errors - Trend Arrow Added */}
                  <div className="bg-white/10 backdrop-blur rounded-lg p-4">
                    <div className="text-purple-200 text-xs mb-1">Errors</div>
                    <div className="flex items-baseline gap-2">
                      <div className={`text-2xl font-bold ${
                        globalHealth.total_errors === 0 ? 'text-green-400' :
                        globalHealth.total_errors < 5 ? 'text-yellow-400' :
                        'text-red-400'
                      }`}>
                        {globalHealth.total_errors}
                      </div>
                      <span className="text-green-400 text-lg">→</span>
                    </div>
                    <div className="text-purple-300 text-xs mt-1">{globalHealth.error_rate}% rate</div>
                  </div>

                  {/* User Impact */}
                  <div className="bg-white/10 backdrop-blur rounded-lg p-4">
                    <div className="text-purple-200 text-xs mb-1">User Impact</div>
                    <div className={`text-lg font-bold ${
                      globalHealth.worst_user_impact === 'none' ? 'text-green-400' :
                      globalHealth.worst_user_impact === 'low' ? 'text-yellow-400' :
                      globalHealth.worst_user_impact === 'medium' ? 'text-orange-400' :
                      'text-red-400'
                    }`}>
                      {globalHealth.worst_user_impact.toUpperCase()}
                    </div>
                    <div className="text-purple-300 text-xs mt-1">Worst case</div>
                  </div>
                </div>
                {/* ⭐ SPARKLINES - BURAYA EKLE */}
                <div className="grid grid-cols-3 gap-4 mt-4">
                  {/* Errors Sparkline */}
                  <div className="bg-white/5 backdrop-blur rounded-lg p-3">
                    <div className="text-purple-200 text-xs mb-2">Errors (24h)</div>
                    <svg viewBox="0 0 100 30" className="w-full h-8" preserveAspectRatio="none">
                      <polyline
                        points={(() => {
                          const mockData = [5, 3, 4, 2, 1, 0, 0, 1, 0, 0, 0, 0];
                          const max = Math.max(...mockData, 1);
                          return mockData.map((val, i) => 
                            `${(i / (mockData.length - 1)) * 100},${30 - (val / max) * 28}`
                          ).join(' ');
                        })()}
                        fill="none"
                        stroke={globalHealth.total_errors === 0 ? '#4ade80' : '#fbbf24'}
                        strokeWidth="2"
                        vectorEffect="non-scaling-stroke"
                      />
                    </svg>
                    <div className="text-purple-300 text-xs mt-1">
                      {globalHealth.total_errors === 0 ? '✅ Stable' : '⚠️ Monitor'}
                    </div>
                  </div>

                  {/* Latency Sparkline */}
                  <div className="bg-white/5 backdrop-blur rounded-lg p-3">
                    <div className="text-purple-200 text-xs mb-2">Latency (24h)</div>
                    <svg viewBox="0 0 100 30" className="w-full h-8" preserveAspectRatio="none">
                      <polyline
                        points={(() => {
                          const mockData = [1500, 1450, 1600, 1550, 1400, 1350, 1500, 1450, 1400, 1550, 1600, 1571];
                          const max = Math.max(...mockData);
                          const min = Math.min(...mockData);
                          return mockData.map((val, i) => 
                            `${(i / (mockData.length - 1)) * 100},${30 - ((val - min) / (max - min)) * 28}`
                          ).join(' ');
                        })()}
                        fill="none"
                        stroke={globalHealth.avg_performance < 2000 ? '#4ade80' : '#fbbf24'}
                        strokeWidth="2"
                        vectorEffect="non-scaling-stroke"
                      />
                    </svg>
                    <div className="text-purple-300 text-xs mt-1">
                      Avg: {globalHealth.avg_performance}ms
                    </div>
                  </div>

                  {/* Health Sparkline */}
                  <div className="bg-white/5 backdrop-blur rounded-lg p-3">
                    <div className="text-purple-200 text-xs mb-2">Health (24h)</div>
                    <svg viewBox="0 0 100 30" className="w-full h-8" preserveAspectRatio="none">
                      <polyline
                        points={(() => {
                          const mockData = [95, 97, 96, 98, 100, 100, 99, 100, 100, 100, 100, globalHealth.overall_health];
                          const max = 100;
                          const min = Math.min(...mockData);
                          return mockData.map((val, i) => 
                            `${(i / (mockData.length - 1)) * 100},${30 - ((val - min) / (max - min)) * 28}`
                          ).join(' ');
                        })()}
                        fill="none"
                        stroke={globalHealth.overall_health >= 80 ? '#4ade80' : globalHealth.overall_health >= 50 ? '#fbbf24' : '#f87171'}
                        strokeWidth="2"
                        vectorEffect="non-scaling-stroke"
                      />
                    </svg>
                    <div className="text-purple-300 text-xs mt-1">
                      {globalHealth.overall_health >= 80 ? '📈 Excellent' : globalHealth.overall_health >= 50 ? '📊 Good' : '📉 Warning'}
                    </div>
                  </div>
                </div>

              </div>

              {(globalHealth.critical_count > 0 || globalHealth.degraded_count > 0) && (
                <div className="bg-yellow-50 border-2 border-yellow-300 rounded-lg p-4 mb-6">
                  <div className="flex items-start gap-3">
                    <span className="text-2xl">⚠️</span>
                    <div className="flex-1">
                      <div className="font-bold text-yellow-800 mb-2">Attention Needed</div>
                      <div className="space-y-1 text-sm text-yellow-700">
                        {globalHealth.critical_count > 0 && (
                          <div>🚨 {globalHealth.critical_count} feature{globalHealth.critical_count > 1 ? 's' : ''} critical</div>
                        )}
                        {globalHealth.degraded_count > 0 && (
                          <div>⚠️ {globalHealth.degraded_count} feature{globalHealth.degraded_count > 1 ? 's' : ''} degraded</div>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          );
        })()}

        {/* Flags */}
        <div className="space-y-4">
          {flags.map((flag) => {
            const isExpanded = expandedFlags.has(flag.flag_key);
            
            return (
              <div key={flag.id} className="bg-white rounded-xl shadow-sm border-2 border-gray-200 overflow-hidden">
                {/* Summary Row */}
                <button
                  onClick={() => toggleExpanded(flag.flag_key)}
                  className="w-full p-4 hover:bg-gray-50 transition flex items-center justify-between"
                >
                  <div className="flex items-center gap-4 flex-1">
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-gray-900 text-lg">{flag.flag_key}</span>
                      {flag.phase && (
                        <span className={`px-2 py-1 rounded text-xs font-semibold ${getPhaseColor(flag.phase)}`}>
                          {flag.phase.toUpperCase()}
                        </span>
                      )}
                    </div>

                    <div className="flex items-center gap-3 ml-auto">
                      <div className={`px-3 py-1 rounded-lg font-bold text-lg ${
                        flag.health_score >= 80 ? 'bg-green-100 text-green-800' :
                        flag.health_score >= 50 ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {flag.health_score}
                      </div>

                      <div className={`px-3 py-1 rounded text-xs font-semibold ${
                        flag.is_enabled ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                      }`}>
                        {flag.is_enabled ? '✅ ON' : '⭕ OFF'}
                      </div>

                      {flag.error_count > 0 && (
                        <div className="px-3 py-1 rounded bg-red-100 text-red-800 text-xs font-semibold">
                          {flag.error_count} errors
                        </div>
                      )}

                      {flag.avg_response_time_ms && flag.avg_response_time_ms > 1000 && (
                        <div className={`px-3 py-1 rounded text-xs font-semibold ${
                          flag.avg_response_time_ms < 2000 ? 'bg-yellow-100 text-yellow-800' :
                          'bg-red-100 text-red-800'
                        }`}>
                          ⚠️ {flag.avg_response_time_ms}ms
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="ml-4 text-gray-400 text-xl">
                    {isExpanded ? '▼' : '▶'}
                  </div>
                </button>

                {isExpanded && (
                  <div className="border-t-2 border-gray-200 p-6 bg-gray-50">
                    <p className="text-sm text-gray-600 mb-4">{flag.description}</p>

                    <div className="grid grid-cols-4 gap-3 mb-4">
                      <div className="bg-white rounded-lg p-3 shadow-sm">
                        <div className="text-xs text-gray-500 mb-1">Status</div>
                        <div className="text-lg font-bold">{flag.is_enabled ? '✅ ON' : '❌ OFF'}</div>
                      </div>
                      <div className="bg-white rounded-lg p-3 shadow-sm">
                        <div className="text-xs text-gray-500 mb-1">Errors</div>
                        <div className="text-lg font-bold text-gray-800">{flag.error_count}</div>
                      </div>
                      <div className="bg-white rounded-lg p-3 shadow-sm">
                        <div className="text-xs text-gray-500 mb-1">Error Rate</div>
                        <div className="text-lg font-bold text-gray-800">
                          {flag.error_rate_percent ? `${flag.error_rate_percent}%` : '0%'}
                        </div>
                      </div>
                      <div className="bg-white rounded-lg p-3 shadow-sm">
                        <div className="text-xs text-gray-500 mb-1">User Impact</div>
                        <div className={`text-xs font-bold px-2 py-1 rounded border ${getImpactBadge(flag.user_impact_level).color}`}>
                          {getImpactBadge(flag.user_impact_level).icon} {getImpactBadge(flag.user_impact_level).text}
                        </div>
                      </div>
                    </div>

                    {(flag.latency_score || flag.error_score || flag.data_volume_score || flag.freshness_score) && (
                      <div className="bg-gradient-to-r from-purple-50 to-blue-50 border-2 border-purple-200 rounded-lg p-4 mb-4">
                        <div className="text-sm font-bold text-purple-800 mb-3">📊 HEALTH BREAKDOWN</div>
                        <div className="grid grid-cols-4 gap-3">
                          <div>
                            <div className="text-xs text-gray-600 mb-1">Latency</div>
                            <div className={`text-2xl font-bold ${
                              (flag.latency_score || 100) >= 80 ? 'text-green-600' : 
                              (flag.latency_score || 100) >= 50 ? 'text-yellow-600' : 
                              'text-red-600'
                            }`}>
                              {flag.latency_score || 100}
                            </div>
                          </div>
                          <div>
                            <div className="text-xs text-gray-600 mb-1">Errors</div>
                            <div className={`text-2xl font-bold ${
                              (flag.error_score || 100) >= 80 ? 'text-green-600' : 
                              (flag.error_score || 100) >= 50 ? 'text-yellow-600' : 
                              'text-red-600'
                            }`}>
                              {flag.error_score || 100}
                            </div>
                          </div>
                          <div>
                            <div className="text-xs text-gray-600 mb-1">Freshness</div>
                            <div className={`text-2xl font-bold ${
                              (flag.freshness_score || 100) >= 80 ? 'text-green-600' : 
                              (flag.freshness_score || 100) >= 50 ? 'text-yellow-600' : 
                              'text-red-600'
                            }`}>
                              {flag.freshness_score || 100}
                            </div>
                          </div>
                          <div>
                            <div className="text-xs text-gray-600 mb-1">Data Volume</div>
                            <div className={`text-2xl font-bold ${
                              (flag.data_volume_score || 100) >= 80 ? 'text-green-600' : 
                              (flag.data_volume_score || 100) >= 50 ? 'text-yellow-600' : 
                              'text-red-600'
                            }`}>
                              {flag.data_volume_score || 100}
                            </div>
                          </div>
                        </div>
                      </div>
                    )}

                    {(flag.avg_response_time_ms || flag.rows_processed) && (
                      <div className="bg-orange-50 border-2 border-orange-200 rounded-lg p-4 mb-4">
                        <div className="text-sm font-bold text-orange-800 mb-3">⚡ RUNTIME SNAPSHOT</div>
                        <div className="grid grid-cols-3 gap-3">
                          {flag.avg_response_time_ms && (
                            <div>
                              <div className="text-xs text-orange-600">Avg Response</div>
                              <div className={`text-lg font-bold ${
                                flag.avg_response_time_ms > 2000 ? 'text-red-700' : 
                                flag.avg_response_time_ms > 1000 ? 'text-orange-700' : 
                                'text-green-700'
                              }`}>
                                {flag.avg_response_time_ms}ms
                              </div>
                            </div>
                          )}
                          {flag.p95_response_time_ms && (
                            <div>
                              <div className="text-xs text-orange-600">P95 Response</div>
                              <div className={`text-lg font-bold ${
                                flag.p95_response_time_ms > 5000 ? 'text-red-700' : 
                                flag.p95_response_time_ms > 2000 ? 'text-orange-700' : 
                                'text-green-700'
                              }`}>
                                {flag.p95_response_time_ms}ms
                              </div>
                            </div>
                          )}
                          {flag.rows_processed && (
                            <div>
                              <div className="text-xs text-orange-600">Rows Processed</div>
                              <div className={`text-lg font-bold ${
                                flag.rows_processed > 100000 ? 'text-red-700' : 
                                flag.rows_processed > 50000 ? 'text-orange-700' : 
                                'text-green-700'
                              }`}>
                                {flag.rows_processed.toLocaleString()}
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    )}

                    {flag.last_error_message && (
                      <div className="bg-red-50 border-2 border-red-300 rounded-lg p-4 mb-4">
                        <div className="text-sm font-bold text-red-800 mb-2">🔥 LAST ERROR SNAPSHOT</div>
                        <div className="space-y-2">
                          <div>
                            <div className="text-xs text-red-600 font-semibold">Message:</div>
                            <code className="text-sm text-red-800 bg-white px-2 py-1 rounded block mt-1">
                              {flag.last_error_message}
                            </code>
                          </div>
                          {flag.last_error_function && (
                            <div>
                              <div className="text-xs text-red-600 font-semibold">Function:</div>
                              <code className="text-sm text-red-800 bg-white px-2 py-1 rounded block mt-1">
                                {flag.last_error_function}
                              </code>
                            </div>
                          )}
                        </div>
                      </div>
                    )}

                    {flag.component_path && (
                      <div className="bg-blue-50 border-2 border-blue-200 rounded-lg p-4 mb-4">
                        <div className="text-sm font-bold text-blue-800 mb-3">🗺️ NAVIGATION & DIAGNOSTICS</div>
                        <div className="mb-2">
                          <span className="text-xs text-blue-600 font-semibold">📁 Component:</span>
                          <code className="ml-2 text-xs bg-white px-2 py-1 rounded border border-blue-200 font-mono">
                            {flag.component_path}
                          </code>
                        </div>
                        {flag.backend_endpoint && (
                          <div className="mb-2">
                            <span className="text-xs text-blue-600 font-semibold">🔌 API:</span>
                            <code className="ml-2 text-xs bg-white px-2 py-1 rounded border border-blue-200 font-mono">
                              {flag.backend_endpoint}
                            </code>
                          </div>
                        )}
                        {flag.related_files && flag.related_files.length > 0 && (
                          <div className="mb-2">
                            <span className="text-xs text-blue-600 font-semibold">📄 Files:</span>
                            <div className="flex flex-wrap gap-2 mt-1">
                              {flag.related_files.map((f, i) => (
                                <code key={i} className="text-xs bg-white px-2 py-1 rounded border border-blue-200">{f}</code>
                              ))}
                            </div>
                          </div>
                        )}
                        {flag.fix_guide && (
                          <div className="bg-yellow-50 border-2 border-yellow-300 rounded p-3 mt-3">
                            <div className="text-xs font-bold text-yellow-800 mb-1">🔧 QUICK FIX GUIDE:</div>
                            <div className="text-sm text-yellow-800">{flag.fix_guide}</div>
                          </div>
                        )}
                        {flag.depends_on && flag.depends_on.length > 0 && (
                          <div className="mt-3 pt-3 border-t border-blue-200">
                            <span className="text-xs text-blue-600 font-semibold">⚡ Depends on:</span>
                            <div className="flex flex-wrap gap-1 mt-1">
                              {flag.depends_on.map((dep, i) => (
                                <span key={i} className="text-xs bg-purple-100 text-purple-700 px-2 py-0.5 rounded">{dep}</span>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    )}

                    <div className="grid grid-cols-4 gap-2 mb-4">
                      <button onClick={() => quickAction(flag.flag_key, 'reset_health')} className="px-3 py-2 bg-green-100 hover:bg-green-200 text-green-800 rounded text-xs font-semibold transition">
                        💚 Reset Health
                      </button>
                      <button onClick={() => quickAction(flag.flag_key, 'clear_errors')} className="px-3 py-2 bg-blue-100 hover:bg-blue-200 text-blue-800 rounded text-xs font-semibold transition">
                        🧹 Clear Errors
                      </button>
                      <button onClick={() => quickAction(flag.flag_key, 'attempt_recovery')} className="px-3 py-2 bg-purple-100 hover:bg-purple-200 text-purple-800 rounded text-xs font-semibold transition">
                        🔄 Recovery
                      </button>
                      <button 
                        onClick={() => { 
                          const diagnostic = {
                            // Core Info
                            feature: flag.flag_key,
                            phase: flag.phase,
                            is_enabled: flag.is_enabled,
                            
                            // Health Metrics
                            health_score: flag.health_score,
                            latency_score: flag.latency_score,
                            error_score: flag.error_score,
                            freshness_score: flag.freshness_score,
                            data_volume_score: flag.data_volume_score,
                            
                            // Performance
                            avg_response_time_ms: flag.avg_response_time_ms,
                            p95_response_time_ms: flag.p95_response_time_ms,
                            rows_processed: flag.rows_processed,
                            
                            // Errors
                            error_count: flag.error_count,
                            error_rate_percent: flag.error_rate_percent,
                            error_severity: flag.error_severity,
                            last_error_message: flag.last_error_message,
                            last_error_function: flag.last_error_function,
                            last_error_at: flag.last_error_at,
                            
                            // Impact
                            user_impact_level: flag.user_impact_level,
                            
                            // Navigation
                            component_path: flag.component_path,
                            backend_endpoint: flag.backend_endpoint,
                            related_files: flag.related_files,
                            
                            // Dependencies
                            depends_on: flag.depends_on,
                            blocks: flag.blocks,
                            
                            // Troubleshooting
                            fix_guide: flag.fix_guide,
                            disabled_reason: flag.disabled_reason,
                            disabled_by: flag.disabled_by,
                            disabled_at: flag.disabled_at
                          };
                          
                          navigator.clipboard.writeText(JSON.stringify(diagnostic, null, 2));
                          alert('✅ Comprehensive diagnostic copied to clipboard!\n\nPaste this into Claude for detailed analysis.');
                        }} 
                        className="px-3 py-2 bg-gradient-to-r from-indigo-100 to-purple-100 text-indigo-800 rounded text-xs font-semibold transition"
                      >
                        🤖 Ask AI
                      </button>
                    </div>

                    {flag.is_enabled && (
                      <div className="bg-yellow-50 border-2 border-yellow-300 rounded-lg p-3 mb-4">
                        <div className="flex items-start gap-2">
                          <span className="text-yellow-600 text-xl">⚠️</span>
                          <div className="flex-1">
                            <div className="text-sm font-bold text-yellow-800 mb-1">Disable Behavior</div>
                            <div className="text-xs text-yellow-700">
                              {flag.flag_key === 'daily_tasks' && 'Component will NOT render. Users see: "Görevleriniz hazırlanıyor..."'}
                              {flag.flag_key === 'at_risk_display' && 'Component will NOT render. Placeholder card shown.'}
                              {flag.flag_key === 'test_entry' && '⚠️ CRITICAL: Students cannot submit tests! Emergency only.'}
                              {!['daily_tasks', 'at_risk_display', 'test_entry'].includes(flag.flag_key) && 'Component will NOT render. No fallback UI.'}
                            </div>
                          </div>
                        </div>
                      </div>
                    )}

                    <button onClick={() => toggleFlag(flag.flag_key)} className={`w-full py-3 rounded-lg font-bold transition shadow-sm ${flag.is_enabled ? 'bg-red-600 hover:bg-red-700 text-white' : 'bg-green-600 hover:bg-green-700 text-white'}`}>
                      {flag.is_enabled ? '🔴 Disable Feature' : '🟢 Enable Feature'}
                    </button>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}