'use client';

import { useState, FormEvent } from 'react';
import { supabase } from '@/lib/supabase/client';

export default function RegisterPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleRegister = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Supabase ile kayıt ol
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: {
            full_name: fullName,
          }
        }
      });

      if (error) throw error;

      // Token'ları kaydet
      const token = data.session?.access_token;
      if (token) {
        localStorage.setItem('access_token', token);
        localStorage.setItem('user', JSON.stringify(data.user));
        document.cookie = `access_token=${token}; path=/; max-age=3600`;

        console.log('✅ Kayıt başarılı, redirect ediliyor...');

        // 250ms stabilization delay + window.location
        setTimeout(() => {
          window.location.href = '/student/dashboard';
        }, 250);
      } else {
        setError('Email doğrulama gerekli. Lütfen emailinizi kontrol edin.');
        setLoading(false);
      }

    } catch (err: any) {
      setError(err.message || 'Kayıt başarısız');
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <form onSubmit={handleRegister} className="bg-white shadow-2xl rounded-2xl p-8">
          <h1 className="text-3xl font-bold text-center mb-6">Hesap Oluştur 🚀</h1>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
              {error}
            </div>
          )}

          <div className="space-y-4">
            <div>
              <label className="block text-gray-700 mb-2">Ad Soyad</label>
              <input
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                required
              />
            </div>

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
              <label className="block text-gray-700 mb-2">Şifre (min 6 karakter)</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
                minLength={6}
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-purple-600 text-white py-3 rounded-lg hover:bg-purple-700 disabled:opacity-50"
            >
              {loading ? 'Kayıt yapılıyor...' : 'Kayıt Ol'}
            </button>
          </div>

          <p className="text-center text-gray-600 mt-6">
            Zaten hesabın var mı?{' '}
            <a href="/login" className="text-purple-600 hover:underline">
              Giriş Yap
            </a>
          </p>
        </form>
      </div>
    </div>
  );
}
