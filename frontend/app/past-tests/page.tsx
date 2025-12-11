'use client';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function PastTestsRedirect() {
  const router = useRouter();
  
  useEffect(() => {
    router.replace('/student/past-tests');
  }, [router]);
  
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center">
        <div className="animate-spin h-12 w-12 border-4 border-blue-600 border-t-transparent rounded-full mx-auto mb-4" />
        <p className="text-gray-600">Yönlendiriliyor...</p>
      </div>
    </div>
  );
}
