import httpx
from datetime import datetime
from typing import List, Literal
from ..models.weather import Location, CurrentWeather, AgriculturalInsight, WeatherResponse
from ..utils.exceptions import (
    CityNotFoundException,
    WeatherDataUnavailableException,
    ExternalAPIException
)
from ..utils.cache import cached
from ..config import settings


class WeatherService:
    def __init__(self):
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
        self.weather_url = "https://api.open-meteo.com/v1/forecast"
        self.timeout = settings.request_timeout

    @cached(ttl=None, key_prefix="geocoding")
    async def get_coordinates(self, city_name: str) -> Location:
        """Obtém coordenadas da cidade usando a API de geocodificação"""
        params = {
            "name": city_name,
            "count": 1,
            "language": "pt",
            "format": "json"
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(self.geocoding_url, params=params)
                response.raise_for_status()
                data = response.json()
                
                if not data.get("results") or len(data["results"]) == 0:
                    raise CityNotFoundException(f"Cidade '{city_name}' não encontrada")
                
                result = data["results"][0]
                return Location(
                    name=result.get("name", city_name),
                    latitude=result["latitude"],
                    longitude=result["longitude"]
                )
        except httpx.HTTPError as e:
            raise ExternalAPIException(f"Erro na API de geocodificação: {str(e)}")
        except Exception as e:
            if isinstance(e, (CityNotFoundException, ExternalAPIException)):
                raise
            raise ExternalAPIException(f"Erro ao buscar coordenadas: {str(e)}")

    @cached(ttl=None, key_prefix="weather")
    async def get_weather_data(self, location: Location) -> dict:
        """Obtém dados climáticos atuais usando a API Open-Meteo"""
        params = {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "current": [
                "temperature_2m",
                "relativehumidity_2m",
                "precipitation",
                "windspeed_10m",
                "pressure_msl",
                "cloudcover"
            ],
            "timezone": "auto"
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(self.weather_url, params=params)
                response.raise_for_status()
                data = response.json()
                
                if "current" not in data:
                    raise WeatherDataUnavailableException("Dados climáticos não disponíveis")
                
                return data
        except httpx.HTTPError as e:
            raise ExternalAPIException(f"Erro na API de clima: {str(e)}")
        except Exception as e:
            if isinstance(e, (WeatherDataUnavailableException, ExternalAPIException)):
                raise
            raise ExternalAPIException(f"Erro ao buscar dados climáticos: {str(e)}")

    def analyze_agricultural_risk(self, weather_data: dict) -> tuple[Literal["low", "medium", "high"], List[str]]:
        """Analisa os dados climáticos e retorna nível de risco e recomendações"""
        current = weather_data["current"]
        
        temp = current.get("temperature_2m", 0)
        humidity = current.get("relativehumidity_2m", 0)
        precipitation = current.get("precipitation", 0)
        wind_speed = current.get("windspeed_10m", 0)
        
        risk_factors = []
        recommendations = []
        
        
        if temp > 35 or temp < 10:
            risk_factors.append("temperature")
            if temp > 35:
                recommendations.append("⚠️ Temperatura muito alta - risco de estresse hídrico")
            else:
                recommendations.append("⚠️ Temperatura baixa - risco de crescimento lento")
        elif temp > 30 or temp < 15:
            risk_factors.append("temperature")
            if temp > 30:
                recommendations.append("🌡️ Temperatura elevada - monitore a irrigação")
            else:
                recommendations.append("🌡️ Temperatura amena - boas condições para desenvolvimento")
        else:
            recommendations.append("✅ Temperatura ideal para o desenvolvimento da cana")
        
        
        if precipitation > 50:
            risk_factors.append("precipitation")
            recommendations.append("🌧️ Chuva intensa - risco de erosão e alagamento")
        elif precipitation > 20:
            risk_factors.append("precipitation")
            recommendations.append("💧 Chuva moderada - boas condições de umidade")
        elif precipitation > 0:
            recommendations.append("🌦️ Chuva leve - condições favoráveis")
        else:
            recommendations.append("☀️ Sem chuva - verifique necessidade de irrigação")
        
        
        if humidity < 30 or humidity > 90:
            risk_factors.append("humidity")
            if humidity < 30:
                recommendations.append("🏜️ Umidade baixa - risco de desidratação")
            else:
                recommendations.append("💦 Umidade alta - risco de doenças fúngicas")
        elif humidity < 40 or humidity > 80:
            risk_factors.append("humidity")
            recommendations.append("🌫️ Umidade moderada - monitore pragas e doenças")
        else:
            recommendations.append("💨 Umidade adequada para o cultivo")
        
        
        if wind_speed > 40:
            risk_factors.append("wind")
            recommendations.append("💨 Vento forte - risco de quebra e perda de umidade")
        elif wind_speed > 25:
            risk_factors.append("wind")
            recommendations.append("🍃 Vento moderado - evite pulverização")
        else:
            recommendations.append("🍃 Condições de vento favoráveis")
        
        
        risk_level: Literal["low", "medium", "high"]
        if len(risk_factors) >= 3 or any(factor in ["temperature", "precipitation"] and 
                                          ((temp > 35 or temp < 10) or precipitation > 50) 
                                          for factor in risk_factors):
            risk_level = "high"
        elif len(risk_factors) >= 1:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        
        if risk_level == "high":
            recommendations.insert(0, "🚨 CONDIÇÕES ADVERSAS - Monitore sua lavoura constantemente")
        elif risk_level == "medium":
            recommendations.insert(0, "⚠️ ATENÇÃO - Mantenha-se alerta às condições")
        else:
            recommendations.insert(0, "✅ CONDIÇÕES FAVORÁVEIS - Bom momento para atividades agrícolas")
        
        return risk_level, recommendations

    async def get_weather_by_city(self, city_name: str) -> WeatherResponse:
        """Método principal que obtém dados climáticos completos para uma cidade"""
        try:
            
            location = await self.get_coordinates(city_name)
            
            
            weather_data = await self.get_weather_data(location)
            
            
            current = weather_data["current"]
            current_weather = CurrentWeather(
                temperature=current["temperature_2m"],
                humidity=int(current["relativehumidity_2m"]),
                precipitation=current["precipitation"],
                wind_speed=current["windspeed_10m"],
                pressure=current["pressure_msl"],
                cloud_cover=int(current["cloudcover"]),
                last_updated=datetime.now()
            )
            
            
            risk_level, recommendations = self.analyze_agricultural_risk(weather_data)
            agricultural_insights = AgriculturalInsight(
                risk_level=risk_level,
                recommendations=recommendations
            )
            
            
            return WeatherResponse(
                location=location,
                current=current_weather,
                agricultural_insights=agricultural_insights
            )
            
        except Exception as e:
            if isinstance(e, (CityNotFoundException, WeatherDataUnavailableException, ExternalAPIException)):
                raise
            raise ExternalAPIException(f"Erro ao processar solicitação: {str(e)}")