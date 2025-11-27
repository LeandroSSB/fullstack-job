from datetime import datetime
from typing import List, Literal
from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel


class Location(BaseModel):
    name: str = Field(..., description="Nome da cidade")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude da localização")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude da localização")


class CurrentWeather(BaseModel):
    temperature: float = Field(..., description="Temperatura atual em Celsius")
    humidity: int = Field(..., ge=0, le=100, description="Umidade relativa em percentual")
    precipitation: float = Field(..., ge=0, description="Precipitação em mm")
    wind_speed: float = Field(..., ge=0, description="Velocidade do vento em km/h")
    pressure: float = Field(..., ge=0, description="Pressão atmosférica em hPa")
    cloud_cover: int = Field(..., ge=0, le=100, description="Cobertura de nuvens em percentual")
    last_updated: datetime = Field(..., description="Data e hora da última atualização")


class AgriculturalInsight(BaseModel):
    model_config = {"alias_generator": to_camel, "populate_by_name": True}
    
    risk_level: Literal["low", "medium", "high"] = Field(..., description="Nível de risco agrícola")
    recommendations: List[str] = Field(..., description="Lista de recomendações para o produtor")


class WeatherResponse(BaseModel):
    model_config = {"alias_generator": to_camel, "populate_by_name": True}
    
    location: Location = Field(..., description="Informações da localização")
    current: CurrentWeather = Field(..., description="Dados climáticos atuais")
    agricultural_insights: AgriculturalInsight = Field(..., description="Insights agrícolas")


class GeocodingResponse(BaseModel):
    results: List[dict] = Field(..., description="Resultados da geocodificação")