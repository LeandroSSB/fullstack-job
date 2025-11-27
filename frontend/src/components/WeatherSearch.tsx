import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';

interface WeatherSearchProps {
  onSearch: (city: string) => void;
  isLoading?: boolean;
}

export default function WeatherSearch({ onSearch, isLoading = false }: WeatherSearchProps) {
  const searchParams = useSearchParams();
  const [city, setCity] = useState('');

  // Sincronizar o input com o query parameter da URL
  useEffect(() => {
    const cityFromUrl = searchParams.get('city');
    if (cityFromUrl) {
      setCity(cityFromUrl);
    }
  }, [searchParams]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (city.trim()) {
      onSearch(city.trim());
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCity(e.target.value);
  };

  return (
    <div className="w-full max-w-md mx-auto">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="relative">
          <input
            type="text"
            value={city}
            onChange={handleInputChange}
            placeholder="Digite o nome da cidade..."
            className="input-field pr-12"
            disabled={isLoading}
            autoFocus
          />
          <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
            {isLoading ? (
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-primary-600"></div>
            ) : (
              <span className="text-gray-400">🔍</span>
            )}
          </div>
        </div>
        
        <button
          type="submit"
          disabled={!city.trim() || isLoading}
          className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
        >
          {isLoading ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              <span>Buscando...</span>
            </>
          ) : (
            <>
              <span>🌤️</span>
              <span>Buscar Clima</span>
            </>
          )}
        </button>
      </form>
      
      <div className="mt-4 text-center">
        <p className="text-sm text-gray-500">
          Ex: "São Paulo", "Ribeirão Preto", "Campinas"
        </p>
      </div>
    </div>
  );
}