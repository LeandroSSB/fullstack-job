import React from 'react';
import { WeatherResponse } from '../types/weather';

interface WeatherCardProps {
  data: WeatherResponse;
}

export default function WeatherCard({ data }: WeatherCardProps) {
  const { location, current, agriculturalInsights } = data;
  
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getRiskLevelClass = (level: string) => {
    switch (level) {
      case 'low':
        return 'risk-low';
      case 'medium':
        return 'risk-medium';
      case 'high':
        return 'risk-high';
      default:
        return 'risk-low';
    }
  };

  const getRiskLevelText = (level: string) => {
    switch (level) {
      case 'low':
        return 'Baixo ✅';
      case 'medium':
        return 'Médio ⚠️';
      case 'high':
        return 'Alto 🚨';
      default:
        return 'Desconhecido';
    }
  };

  return (
    <div className="space-y-6 fade-in">
      {/* Localização */}
      <div className="weather-card">
        <div className="flex items-center space-x-3 mb-4">
          <div className="text-3xl">📍</div>
          <div>
            <h2 className="text-xl font-bold text-gray-800">{location.name}</h2>
            <p className="text-sm text-gray-500">
              {location.latitude.toFixed(4)}°, {location.longitude.toFixed(4)}°
            </p>
          </div>
        </div>
      </div>

      {/* Dados Climáticos */}
      <div className="weather-card">
        <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
          <span className="mr-2">🌡️</span>
          Condições Atuais
        </h3>
        
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          <div className="bg-blue-50 rounded-lg p-3 text-center">
            <div className="text-2xl mb-1">🌡️</div>
            <p className="text-sm text-gray-600">Temperatura</p>
            <p className="text-lg font-bold text-blue-600">{current.temperature}°C</p>
          </div>
          
          <div className="bg-green-50 rounded-lg p-3 text-center">
            <div className="text-2xl mb-1">💧</div>
            <p className="text-sm text-gray-600">Umidade</p>
            <p className="text-lg font-bold text-green-600">{current.humidity}%</p>
          </div>
          
          <div className="bg-cyan-50 rounded-lg p-3 text-center">
            <div className="text-2xl mb-1">🌧️</div>
            <p className="text-sm text-gray-600">Chuva</p>
            <p className="text-lg font-bold text-cyan-600">{current.precipitation}mm</p>
          </div>
          
          <div className="bg-gray-50 rounded-lg p-3 text-center">
            <div className="text-2xl mb-1">💨</div>
            <p className="text-sm text-gray-600">Vento</p>
            <p className="text-lg font-bold text-gray-600">{current.wind_speed}km/h</p>
          </div>
          
          <div className="bg-purple-50 rounded-lg p-3 text-center">
            <div className="text-2xl mb-1">📊</div>
            <p className="text-sm text-gray-600">Pressão</p>
            <p className="text-lg font-bold text-purple-600">{current.pressure}hPa</p>
          </div>
          
          <div className="bg-yellow-50 rounded-lg p-3 text-center">
            <div className="text-2xl mb-1">☁️</div>
            <p className="text-sm text-gray-600">Nuvens</p>
            <p className="text-lg font-bold text-yellow-600">{current.cloud_cover}%</p>
          </div>
        </div>
        
        <div className="mt-4 text-center text-sm text-gray-500">
          🕐 Última atualização: {formatDate(current.last_updated)}
        </div>
      </div>

      {/* Insights Agrícolas */}
      <div className="weather-card">
        <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
          <span className="mr-2">🌾</span>
          Análise para Cana-de-Açúcar
        </h3>
        
        <div className="mb-4">
          <div className={`inline-flex items-center px-4 py-2 rounded-full font-medium ${getRiskLevelClass(agriculturalInsights.riskLevel)}`}>
            <span className="mr-2">⚠️</span>
            Nível de Risco: {getRiskLevelText(agriculturalInsights.riskLevel)}
          </div>
        </div>
        
        <div>
          <h4 className="font-medium text-gray-700 mb-3 flex items-center">
            <span className="mr-2">💡</span>
            Recomendações:
          </h4>
          <ul className="space-y-2">
            {agriculturalInsights.recommendations.map((recommendation: string, index: number) => (
              <li key={index} className="flex items-start space-x-2">
                <span className="text-green-600 mt-1">•</span>
                <span className="text-gray-700">{recommendation}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}