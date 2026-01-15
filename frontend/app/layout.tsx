import type { Metadata } from 'next';
import './globals.css';
import { Providers } from './providers';
import FloatingFeatureMonitor from '@/components/FloatingFeatureMonitor';

export const metadata: Metadata = {
  title: 'End.STP - Akıllı Öğrenme Analiz Sistemi',
  description:
    'Öğrenci performansını analiz eden, kişiselleştirilmiş öğrenme yolları oluşturan yapay zeka destekli platform',

  // ✅ GÜVENLİK
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

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="tr">
      <body>
        <Providers>
          {children}
          <FloatingFeatureMonitor />
        </Providers>
      </body>
    </html>
  );
}
