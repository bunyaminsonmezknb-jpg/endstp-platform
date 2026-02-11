// frontend/lib/logout-helper.ts
// Tüm session'ları temizle

import { createBrowserClient } from '@supabase/ssr';

export async function logoutAndClearAll() {
  const supabase = createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );

  try {
    // 1. Supabase logout
    console.log('🚪 Logging out...');
    await supabase.auth.signOut();
    
    // 2. Clear localStorage
    console.log('🧹 Clearing localStorage...');
    localStorage.clear();
    
    // 3. Clear sessionStorage
    console.log('🧹 Clearing sessionStorage...');
    sessionStorage.clear();
    
    // 4. Clear cookies (best effort)
    console.log('🧹 Clearing cookies...');
    document.cookie.split(";").forEach((c) => {
      document.cookie = c
        .replace(/^ +/, "")
        .replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
    });
    
    console.log('✅ All cleared!');
    
    // 5. Redirect to login
    window.location.href = '/login';
    
  } catch (error) {
    console.error('❌ Logout error:', error);
    // Force redirect anyway
    window.location.href = '/login';
  }
}

// Browser console'dan çağrılabilir
if (typeof window !== 'undefined') {
  (window as any).logoutAndClearAll = logoutAndClearAll;
}