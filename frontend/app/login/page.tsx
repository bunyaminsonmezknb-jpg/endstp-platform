// frontend/app/login/page.tsx
'use client';

import { useState, FormEvent } from 'react';
import { getSupabaseClient } from '@/lib/supabase/client';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleLogin = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const supabase = getSupabaseClient();

      // 1. Login
      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password,
      });

      console.log('🔐 LOGIN RESULT', {
        hasSession: !!data?.session,
        hasToken: !!data?.session?.access_token,
        error: error?.message ?? null,
      });

      if (error) throw error;

      if (!data?.session) {
        throw new Error('Login başarılı ama session oluşmadı');
      }

      // 2. Session confirm (cookie yazılmasını bekle)
      await new Promise(resolve => setTimeout(resolve, 500));

      const { data: checkData } = await supabase.auth.getSession();
      console.log('🔍 SESSION CONFIRM:', {
        hasSession: !!checkData?.session,
        hasToken: !!checkData?.session?.access_token,
      });

      if (!checkData?.session?.access_token) {
        throw new Error('Session persist edilemedi');
      }

      // 3. Success - Middleware redirect edecek
      console.log('✅ LOGIN SUCCESS - Redirecting');
      window.location.href = '/student/dashboard';

    } catch (err: any) {
      console.error('❌ LOGIN ERROR:', err);
      setError(err.message || 'Giriş başarısız');
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <form onSubmit={handleLogin} className="bg-white shadow-2xl rounded-2xl p-8">
          <h1 className="text-3xl font-bold text-center mb-6">Hoş Geldin! 👋</h1>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
              <div className="font-semibold">❌ Giriş Başarısız</div>
              <div className="text-sm mt-1">{error}</div>
            </div>
          )}

          <div className="space-y-4">
            <div>
              <label className="block text-gray-700 mb-2 font-medium">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:outline-none"
                placeholder="ornek@email.com"
                required
                disabled={loading}
              />
            </div>

            <div>
              <label className="block text-gray-700 mb-2 font-medium">Şifre</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:outline-none"
                placeholder="••••••••"
                required
                disabled={loading}
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white py-3 rounded-lg hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-semibold shadow-lg transition-all"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                      fill="none"
                    />
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    />
                  </svg>
                  Giriş yapılıyor...
                </span>
              ) : (
                'Giriş Yap'
              )}
            </button>
          </div>

          <p className="text-center text-gray-600 mt-6">
            Hesabın yok mu?{' '}
            <a href="/register" className="text-purple-600 hover:underline font-semibold">
              Kayıt Ol
            </a>
          </p>
        </form>
      </div>
    </div>
  );
}