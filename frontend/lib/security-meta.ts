import { Metadata } from 'next';

/**
 * Güvenlik Meta Tags
 * 
 * layout.tsx içinde metadata olarak kullanılacak
 * Global – tüm sayfalar için geçerli
 */
export const securityMetadata: Metadata = {
  referrer: 'no-referrer',

  robots: {
    index: true,
    follow: true,
    'max-image-preview': 'large',
    'max-snippet': -1,
  },

  other: {
    'Content-Security-Policy': 'upgrade-insecure-requests',
  },
};
