'use client';

export default function DashboardError({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  console.error('📉 Dashboard route error:', error);

  return (
    <div className="flex flex-col items-center justify-center h-full p-10">
      <h2 className="text-xl font-bold text-red-600">
        Dashboard geçici olarak yüklenemedi
      </h2>
      <p className="text-sm text-gray-500 mt-2">
        Sistem çalışıyor, sadece bu bölüm sorun yaşadı.
      </p>
      <button
        onClick={reset}
        className="mt-6 px-4 py-2 rounded bg-purple-600 text-white hover:bg-purple-700"
      >
        Tekrar Dene
      </button>
    </div>
  );
}
