'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleLogin = async (e: any) => {
    e.preventDefault?.();
    
    if (!email || !password) {
      setError('Lütfen email ve şifre girin');
      return;
    }
    
    setLoading(true);
    setError(null);

    try {
      console.log('Login başlıyor...', { email });
      
      // Backend API'ye POST isteği
      const response = await fetch('http://localhost:8000/api/v1/signin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      const data = await response.json();
      console.log('Backend response:', data);

      if (!response.ok) {
        setError(data.detail || 'Giriş başarısız');
        setLoading(false);
        return;
      }

      // Başarılı giriş
      console.log('Login başarılı! Yönlendiriliyor...');
      
      // Access token'ı localStorage'a kaydet
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('user', JSON.stringify(data.user));

      // Cookie'ye de kaydet (middleware için)
      document.cookie = `access_token=${data.access_token}; path=/; max-age=3600`;

      // Dashboard'a yönlendir (window.location ile zorla)
      setTimeout(() => {
        window.location.href = '/student/dashboard';
      }, 100);
      
    } catch (err) {
      console.error('Login error:', err);
      setError('Backend bağlantı hatası. Lütfen backend çalıştığından emin olun.');
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-5">
      <div className="bg-white rounded-3xl shadow-2xl p-10 w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-end-purple to-end-purple-dark bg-clip-text text-transparent">
            End.STP
          </h1>
          <p className="text-gray-600 mt-2">Akıllı Öğrenme Analiz Sistemi</p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-6">
            <p className="text-sm">{error}</p>
          </div>
        )}

        {/* Login Form */}
        <div className="space-y-6">
          <div>
            <label htmlFor="email" className="blfock text-sm font-medium text-gray-700 mb-2">
              E-posta
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-end-purple focus:border-transparent"
              placeholder="ornek@email.com"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
              Şifre
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-end-purple focus:border-transparent"
              placeholder="••••••••"
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  handleLogin(e as any);
                }
              }}
            />
          </div>

          <button
            onClick={handleLogin}
            disabled={loading}
            type="button"
            className={`w-full py-3 rounded-lg text-white font-semibold transition-all ${
              loading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-end-purple to-end-purple-dark hover:scale-105'
            }`}
          >
            {loading ? '⏳ Giriş yapılıyor...' : '🚀 Giriş Yap'}
          </button>
        </div>

        {/* Test Credentials */}
        <div className="mt-8 p-4 bg-blue-50 rounded-lg">
          <p className="text-xs text-blue-800 font-semibold mb-2">📝 Test Hesapları:</p>
          <div className="text-xs text-blue-600 space-y-1">
            <p>Email: demo@end-stp.com</p>
            <p>Şifre: demo123</p>
            <p className="text-gray-500 mt-2">(Önce Supabase'de oluşturun)</p>
          </div>
        </div>

        {/* Footer */}
        <p className="text-center text-xs text-gray-500 mt-6">
          End.STP © 2024 - Tüm hakları saklıdır
        </p>
      </div>
    </div>
  );
}
