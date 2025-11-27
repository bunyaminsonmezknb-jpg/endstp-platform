import { Metadata } from 'next';

/**
 * Güvenlik Meta Tags
 * 
 * Layout.tsx'e eklenecek - tüm sayfalar için geçerli
 */
export const securityMetadata: Metadata = {
  // Referrer Policy - Veri sızıntısı önleme
  referrer: 'no-referrer',
  
  // Robots - SEO ayarları
  robots: {
    index: true,
    follow: true,
    'max-image-preview': 'large',
    'max-snippet': -1,
  },
};

/**
 * Meta Component (Head'e eklenecek)
 */
export function SecurityMetaTags() {
  return (
    <>
      {/* Referrer Policy - Global */}
      <meta name="referrer" content="no-referrer" />
      
      {/* Content Security Policy (İleride detaylandırılacak) */}
      <meta
        httpEquiv="Content-Security-Policy"
        content="upgrade-insecure-requests"
      />
    </>
  );
}
