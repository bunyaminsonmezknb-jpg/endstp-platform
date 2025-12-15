import type { Metadata } from 'next';
import './globals.css';
import { Providers } from './providers';

export const metadata: Metadata = {
  title: 'End.STP - Akıllı Öğrenme Analiz Sistemi',
  description: 'Öğrenci performansını analiz eden, kişiselleştirilmiş öğrenme yolları oluşturan yapay zeka destekli platform',
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
        <meta name="referrer" content="no-referrer" />
      </head>
      <body>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
}
