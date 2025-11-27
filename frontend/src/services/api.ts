import { WeatherResponse, WeatherError } from '../types/weather';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiService {
  private async request<T>(url: string, options: RequestInit = {}): Promise<T> {
    const fullUrl = `${API_BASE_URL}${url}`;
    
    try {
      const response = await fetch(fullUrl, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        const errorData: WeatherError = await response.json().catch(() => ({ 
          detail: 'Erro desconhecido' 
        }));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('Erro de conexão com o servidor');
    }
  }

  async getWeatherByCity(city: string): Promise<WeatherResponse> {
    if (!city || city.trim() === '') {
      throw new Error('Nome da cidade é obrigatório');
    }

    const params = new URLSearchParams({ city: city.trim() });
    return this.request<WeatherResponse>(`/weather?${params}`);
  }

  async healthCheck(): Promise<{ status: string; service: string; version: string }> {
    return this.request('/health');
  }
}

export const apiService = new ApiService();