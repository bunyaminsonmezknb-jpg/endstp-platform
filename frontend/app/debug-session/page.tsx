// frontend/app/debug-session/page.tsx
// Session debug sayfası

'use client';

import { useEffect, useState } from 'react';
import { createBrowserClient } from '@supabase/ssr';

export default function DebugSessionPage() {
  const [sessionInfo, setSessionInfo] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const supabase = createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );

  useEffect(() => {
    async function checkSession() {
      try {
        // 1. Get session
        const { data: { session }, error } = await supabase.auth.getSession();
        
        if (error) {
          setSessionInfo({ error: error.message });
          return;
        }

        if (!session) {
          setSessionInfo({ 
            status: 'NO SESSION',
            message: 'Kullanıcı login olmamış'
          });
          return;
        }

        // 2. Get user profile
        const { data: profile, error: profileError } = await supabase
          .from('user_profiles')
          .select('*')
          .eq('id', session.user.id)
          .single();

        setSessionInfo({
          status: 'LOGGED IN',
          email: session.user.email,
          userId: session.user.id,
          role: profile?.role ?? 'Unknown',
          profile: profile,
          profileError: profileError?.message,
          sessionCreatedAt: session.user.created_at,
          expiresAt: session.expires_at
        });

      } catch (err: any) {
        setSessionInfo({ error: err.message });
      } finally {
        setLoading(false);
      }
    }

    checkSession();
  }, []);

  async function handleLogout() {
    await supabase.auth.signOut();
    window.location.href = '/login';
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-lg">Kontrol ediliyor...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">🔍 Session Debug</h1>

        <div className="bg-white rounded-lg shadow-md p-6 mb-4">
          <h2 className="text-xl font-semibold mb-4">Session Durumu</h2>
          
          {sessionInfo?.status === 'NO SESSION' && (
            <div className="p-4 bg-yellow-50 border border-yellow-200 rounded">
              <p className="text-yellow-900 font-semibold">⚠️ Session Yok</p>
              <p className="text-yellow-800 mt-2">Kullanıcı login olmamış.</p>
              <a 
                href="/login"
                className="mt-4 inline-block px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                Login Sayfasına Git
              </a>
            </div>
          )}

          {sessionInfo?.status === 'LOGGED IN' && (
            <div>
              <div className="space-y-3">
                <div className="flex items-start gap-4">
                  <span className="font-semibold w-32">Email:</span>
                  <span className={`font-mono ${
                    sessionInfo.email === 'admin2@admin.com' 
                      ? 'text-green-700 font-bold' 
                      : 'text-red-700 font-bold'
                  }`}>
                    {sessionInfo.email}
                  </span>
                </div>

                <div className="flex items-start gap-4">
                  <span className="font-semibold w-32">User ID:</span>
                  <span className="font-mono text-sm text-gray-700">
                    {sessionInfo.userId}
                  </span>
                </div>

                <div className="flex items-start gap-4">
                  <span className="font-semibold w-32">Role:</span>
                  <span className={`font-bold ${
                    sessionInfo.role === 'admin' 
                      ? 'text-purple-700' 
                      : sessionInfo.role === 'student'
                      ? 'text-blue-700'
                      : 'text-gray-700'
                  }`}>
                    {sessionInfo.role}
                  </span>
                </div>

                {sessionInfo.profileError && (
                  <div className="p-3 bg-red-50 border border-red-200 rounded mt-3">
                    <p className="text-red-900 font-semibold">❌ Profile Fetch Error:</p>
                    <p className="text-red-800 text-sm mt-1 font-mono">
                      {sessionInfo.profileError}
                    </p>
                  </div>
                )}
              </div>

              <div className="mt-6 pt-6 border-t">
                <h3 className="font-semibold mb-3">Doğru Kullanıcı mı?</h3>
                
                {sessionInfo.email === 'admin2@admin.com' ? (
                  <div className="p-4 bg-green-50 border border-green-200 rounded">
                    <p className="text-green-900">✅ Doğru kullanıcı ile login olmuşsun!</p>
                    <a 
                      href="/admin"
                      className="mt-3 inline-block px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                    >
                      Admin Paneline Git
                    </a>
                  </div>
                ) : (
                  <div className="p-4 bg-red-50 border border-red-200 rounded">
                    <p className="text-red-900 font-semibold">❌ Yanlış kullanıcı!</p>
                    <p className="text-red-800 mt-2">
                      Beklenen: <span className="font-mono">admin2@admin.com</span><br />
                      Gerçek: <span className="font-mono">{sessionInfo.email}</span>
                    </p>
                    <button
                      onClick={handleLogout}
                      className="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
                    >
                      Logout + Yeniden Login
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}

          {sessionInfo?.error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded">
              <p className="text-red-900 font-semibold">❌ Hata:</p>
              <p className="text-red-800 font-mono text-sm mt-2">
                {sessionInfo.error}
              </p>
            </div>
          )}
        </div>

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h3 className="font-semibold text-blue-900 mb-2">💡 Sonraki Adımlar:</h3>
          <ol className="list-decimal list-inside space-y-1 text-blue-800 text-sm">
            <li>Eğer yanlış kullanıcı ise: Logout → Login (admin2@admin.com)</li>
            <li>Eğer "permission denied" ise: RLS fix uygula</li>
            <li>Cache temizle: <code className="bg-blue-100 px-1 rounded">rm -rf .next</code></li>
          </ol>
        </div>

        <div className="mt-4 text-center">
          <button
            onClick={handleLogout}
            className="px-6 py-2 bg-gray-600 text-white rounded hover:bg-gray-700"
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  );
}