import { Suspense } from 'react';
import TestEntryClient from './TestEntryClient';

export default function TestEntryPage() {
  return (
    <Suspense fallback={<div className="p-8">Yükleniyor...</div>}>
      <TestEntryClient />
    </Suspense>
  );
}
