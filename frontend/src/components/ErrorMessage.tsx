import React from 'react';

interface ErrorMessageProps {
  message: string;
  onRetry?: () => void;
  showRetry?: boolean;
}

export default function ErrorMessage({ message, onRetry, showRetry = true }: ErrorMessageProps) {
  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center max-w-md mx-auto">
      <div className="text-red-600 text-4xl mb-4">❌</div>
      <h3 className="text-lg font-semibold text-red-800 mb-2">
        Ops! Algo deu errado
      </h3>
      <p className="text-red-600 mb-6">{message}</p>
      
      {showRetry && onRetry && (
        <button
          onClick={onRetry}
          className="btn-primary bg-red-600 hover:bg-red-700 focus:ring-red-500"
        >
          Tentar Novamente
        </button>
      )}
    </div>
  );
}