'use client';
import React from 'react';

interface ErrorBoundaryProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends React.Component<
  ErrorBoundaryProps,
  ErrorBoundaryState
> {
  state: ErrorBoundaryState = { hasError: false };

static getDerivedStateFromError(error: any): ErrorBoundaryState {
  if (error?.silent) {
    return { hasError: false };
  }
  return { hasError: true, error };
}


  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error('🔥 UI ErrorBoundary caught:', error, info);
  }

  render() {
    if (this.state.hasError) {
      return (
        this.props.fallback || (
          <div className="p-6 text-center text-gray-500">
            <h2 className="text-lg font-semibold">Bir şeyler ters gitti</h2>
            <p className="text-sm mt-2">
              Sayfa çalışmaya devam ediyor. Lütfen yenileyin.
            </p>
          </div>
        )
      );
    }

    return this.props.children;
  }
}
