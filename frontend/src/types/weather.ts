export interface Location {
  name: string;
  latitude: number;
  longitude: number;
}

export interface CurrentWeather {
  temperature: number;
  humidity: number;
  precipitation: number;
  wind_speed: number;
  pressure: number;
  cloud_cover: number;
  last_updated: string;
}

export interface AgriculturalInsight {
  riskLevel: "low" | "medium" | "high";
  recommendations: string[];
}

export interface WeatherResponse {
  location: Location;
  current: CurrentWeather;
  agriculturalInsights: AgriculturalInsight;
}

export interface WeatherError {
  detail: string;
}

export type WeatherStatus = "idle" | "loading" | "success" | "error";