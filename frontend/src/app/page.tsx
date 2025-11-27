'use client';

import React, { useState } from 'react';
import { WeatherResponse, WeatherStatus } from '../types/weather';
import { apiService } from '../services/api';
import WeatherSearch from '../components/WeatherSearch';
import WeatherCard from '../components/WeatherCard';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';

export default function Home() {
  const [weatherData, setWeatherData] = useState<WeatherResponse | null>(null);
  const [status, setStatus] = useState<WeatherStatus>('idle');
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (city: string) => {
    setStatus('loading');
    setError(null);
    setWeatherData(null);

    try {
      const data = await apiService.getWeatherByCity(city);
      setWeatherData(data);
      setStatus('success');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro desconhecido';
      setError(errorMessage);
      setStatus('error');
    }
  };

  const handleRetry = () => {
    setStatus('idle');
    setError(null);
  };

  const renderContent = () => {
    switch (status) {
      case 'idle':
        return (
          <div className="text-center py-12">
            <div className="text-6xl mb-6">🌾</div>
            <h1 className="text-3xl font-bold text-gray-800 mb-4">
              Clima Cana
            </h1>
            <p className="text-lg text-gray-600 mb-8 max-w-md mx-auto">
              Informações climáticas essenciais para o desenvolvimento saudável da sua lavoura de cana-de-açúcar
            </p>
            
            <div className="max-w-md mx-auto">
              <WeatherSearch onSearch={handleSearch} isLoading={false} />
            </div>
            
            <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
              <div className="bg-white rounded-lg shadow-md p-6 text-center">
                <div className="text-3xl mb-3">🌡️</div>
                <h3 className="font-semibold text-gray-800 mb-2">Temperatura</h3>
                <p className="text-sm text-gray-600">Monitore as condições ideias para o crescimento</p>
              </div>
              
              <div className="bg-white rounded-lg shadow-md p-6 text-center">
                <div className="text-3xl mb-3">💧</div>
                <h3 className="font-semibold text-gray-800 mb-2">Umidade</h3>
                <p className="text-sm text-gray-600">Controle o risco de doenças e pragas</p>
              </div>
              
              <div className="bg-white rounded-lg shadow-md p-6 text-center">
                <div className="text-3xl mb-3">🌧️</div>
                <h3 className="font-semibold text-gray-800 mb-2">Precipitação</h3>
                <p className="text-sm text-gray-600">Otimize sua irrigação e colheita</p>
              </div>
            </div>
          </div>
        );

      case 'loading':
        return (
          <div className="text-center py-12">
            <LoadingSpinner 
              size="large" 
              message="Buscando informações climáticas..." 
            />
          </div>
        );

      case 'success':
        return (
          <div>
            <div className="mb-6">
              <WeatherSearch onSearch={handleSearch} />
            </div>
            <WeatherCard data={weatherData!} />
          </div>
        );

      case 'error':
        return (
          <div className="text-center py-12">
            <div className="mb-6">
              <WeatherSearch onSearch={handleSearch} isLoading={false} />
            </div>
            <ErrorMessage 
              message={error || 'Ocorreu um erro'} 
              onRetry={handleRetry}
            />
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen">
      {renderContent()}
    </div>
  );
}