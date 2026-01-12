'use client';

import { useState, FormEvent } from 'react';
import { supabase } from '@/lib/supabase/client';

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
      // ✅ DOĞRU: Sadece Supabase login
      const { error } = await supabase.auth.signInWithPassword({
        email,
        password,
      });

      if (error) throw error;

      // ✅ Supabase session cookie'yi otomatik set eder
      // ❌ localStorage.setItem KALDIRILDI
      // ❌ document.cookie KALDIRILDI
      
      console.log('✅ Login başarılı, redirect ediliyor...');
      window.location.href = '/student/dashboard';

    } catch (err: any) {
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
              {error}
            </div>
          )}

          <div className="space-y-4">
            <div>
              <label className="block text-gray-700 mb-2">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                required
              />
            </div>

            <div>
              <label className="block text-gray-700 mb-2">Şifre</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-purple-600 text-white py-3 rounded-lg hover:bg-purple-700 disabled:opacity-50"
            >
              {loading ? 'Giriş yapılıyor...' : 'Giriş Yap'}
            </button>
          </div>

          <p className="text-center text-gray-600 mt-6">
            Hesabın yok mu?{' '}
            <a href="/register" className="text-purple-600 hover:underline">
              Kayıt Ol
            </a>
          </p>
        </form>
      </div>
    </div>
  );
}
