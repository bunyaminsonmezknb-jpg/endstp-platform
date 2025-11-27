'use client';

import { useState } from 'react';

interface SafeExternalLinkProps {
  href: string;
  children: React.ReactNode;
  partnerName: string;
  className?: string;
  showDisclaimer?: boolean;
}

/**
 * Güvenli Dış Link Component
 * 
 * Affiliate/Partner linkler için güvenlik ve SEO önlemleri:
 * - rel="nofollow sponsored noopener noreferrer" (SEO koruması)
 * - target="_blank" (yeni sekmede açılır)
 * - Ara geçiş modalı (kullanıcı uyarısı)
 * - KKVK uyumlu disclaimer
 */
export default function SafeExternalLink({
  href,
  children,
  partnerName,
  className = '',
  showDisclaimer = true,
}: SafeExternalLinkProps) {
  const [showModal, setShowModal] = useState(false);

  const handleClick = (e: React.MouseEvent) => {
    if (showDisclaimer) {
      e.preventDefault();
      setShowModal(true);
    }
  };

  const handleProceed = () => {
    setShowModal(false);
    // Yeni sekmede aç
    window.open(href, '_blank', 'noopener,noreferrer');
  };

  return (
    <>
      <a
        href={href}
        onClick={handleClick}
        className={className}
        // GÜVENLİK VE SEO KORUMALARI (Zorunlu!)
        rel="nofollow sponsored noopener noreferrer"
        target="_blank"
        // Referrer gizleme (veri sızıntısı önleme)
        referrerPolicy="no-referrer"
      >
        {children}
      </a>

      {/* Ara Geçiş Modalı (Disclaimer) */}
      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl">
            {/* Header */}
            <div className="flex items-center gap-3 mb-4">
              <div className="w-12 h-12 rounded-full bg-orange-100 flex items-center justify-center text-2xl">
                🔗
              </div>
              <div>
                <h3 className="text-xl font-bold text-gray-900">
                  Dış Bağlantıya Gidiyorsunuz
                </h3>
                <p className="text-sm text-gray-500">
                  {partnerName}
                </p>
              </div>
            </div>

            {/* Disclaimer */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
              <p className="text-sm text-gray-700 leading-relaxed">
                <strong className="text-blue-900">📌 Önemli Bilgilendirme:</strong>
                <br />
                End.STP dışına çıkıyorsunuz. Gideceğiniz kaynağın içeriğinden, 
                güvenliğinden ve gizlilik politikalarından kurumumuz sorumlu değildir.
              </p>
            </div>

            {/* Sponsorlu İçerik Bildirimi (Yasal Zorunluluk) */}
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3 mb-4">
              <p className="text-xs text-gray-600">
                <strong>⚠️ Sponsorlu İçerik:</strong> Bu link, partner kurumumuza aittir. 
                End.STP bu yönlendirmeden gelir elde edebilir.
              </p>
            </div>

            {/* Actions */}
            <div className="flex gap-3">
              <button
                onClick={() => setShowModal(false)}
                className="flex-1 px-4 py-3 bg-gray-200 text-gray-700 rounded-lg font-semibold hover:bg-gray-300 transition-colors"
              >
                ❌ Vazgeç
              </button>
              <button
                onClick={handleProceed}
                className="flex-1 px-4 py-3 bg-gradient-to-r from-end-purple to-end-purple-dark text-white rounded-lg font-semibold hover:scale-105 transition-transform"
              >
                ✅ Devam Et
              </button>
            </div>

            {/* Footer Note */}
            <p className="text-xs text-gray-400 text-center mt-4">
              Yeni sekmede açılacak. Ana sayfanız açık kalacak.
            </p>
          </div>
        </div>
      )}
    </>
  );
}
