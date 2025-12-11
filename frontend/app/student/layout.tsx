'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Sidebar from '@/app/components/Sidebar';

export default function StudentLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();

  useEffect(() => {
    // Auth kontrolü
    const userStr = localStorage.getItem('user');
    const accessToken = localStorage.getItem('access_token');
    
    if (!userStr || !accessToken) {
      router.push('/login');
      return;
    }
  }, [router]);

  return (
<div className="min-h-screen bg-gray-50 flex justify-center">
  <div className="flex">
    <Sidebar />

    <main className="min-h-screen">
      <div className="max-w-[1280px] w-full px-6">
        {children}
      </div>
    </main>
  </div>
</div>
  );
}