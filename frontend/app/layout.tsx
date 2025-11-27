import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'End.STP - Akıllı Öğrenme Analiz Sistemi',
  description: 'Öğrenci performansını analiz eden, kişiselleştirilmiş öğrenme yolları oluşturan yapay zeka destekli platform',
  // Güvenlik: Referrer Policy
  referrer: 'no-referrer',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="tr">
      <head>
        {/* Güvenlik Meta Tags */}
        <meta name="referrer" content="no-referrer" />
      </head>
      <body>{children}</body>
    </html>
  );
}
