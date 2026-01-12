'use client';

import { useState, FormEvent } from 'react';
import { supabase } from '@/lib/supabase/client';

export default function RegisterPage() {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  const handleRegister = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccessMsg('');

    try {
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: { full_name: fullName },
          // Eğer email confirm ON ise, buraya redirect URL eklemek isteyebilirsin:
          // emailRedirectTo: `${window.location.origin}/login`
        },
      });

      if (error) throw error;

      // ✅ Email confirm OFF ise session gelebilir → direkt dashboard
      if (data.session?.access_token) {
        window.location.href = '/student/dashboard';
        return;
      }

      // ✅ Email confirm ON ise session null gelir → kullanıcıya bilgi ver
      setSuccessMsg(
        '✅ Kayıt alındı. Email doğrulama gerekiyorsa lütfen gelen kutunu kontrol et. Doğrulama sonrası giriş yapabilirsin.'
      );
    } catch (err: any) {
      setError(err?.message || 'Kayıt başarısız');
    } finally {
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

          {successMsg && (
            <div className="bg-green-50 border border-green-200 text-green-800 px-4 py-3 rounded-lg mb-4">
              {successMsg}
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
