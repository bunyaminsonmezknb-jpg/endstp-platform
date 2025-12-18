'use client';
import { useState, useEffect } from 'react';
import { api } from '@/lib/api/client';

export default function FloatingFeatureMonitor() {
  const [status, setStatus] = useState<any>(null);
  const [visible, setVisible] = useState(false);
  const [showPopup, setShowPopup] = useState(false);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await api.get('/flags/health-status') as any;
        setStatus(response);
        
        // Show badge if any issues
        if (response.critical_count > 0 || response.high_count > 0) {
          setVisible(true);
          setShowPopup(true);
          
          // Auto-hide popup after 10 seconds
          setTimeout(() => setShowPopup(false), 10000);
        } else {
          setVisible(false);
        }
      } catch (error) {
        console.error('Health check failed:', error);
      }
    };

    // Check immediately
    checkHealth();
    
    // Check every 30 seconds
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  if (!visible || !status) return null;

  const criticalCount = status.critical_count + status.high_count;

  return (
    <>
      {/* Floating Badge - Bottom Right */}
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
      {showPopup && status.critical_flags && status.critical_flags.length > 0 && (
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
                  {flag.severity.toUpperCase()} • {flag.user_impact} impact
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