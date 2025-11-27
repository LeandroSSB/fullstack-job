from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from ...services.weather_service import WeatherService
from ...models.weather import WeatherResponse
from ...utils.exceptions import (
    handle_city_not_found,
    handle_weather_data_unavailable,
    handle_external_api_error
)

router = APIRouter(prefix="/weather", tags=["weather"])
weather_service = WeatherService()


@router.get("", response_model=WeatherResponse, summary="Obter informações climáticas por cidade")
async def get_weather_by_city(
    city: str = Query(..., min_length=1, max_length=100, description="Nome da cidade para busca")
) -> WeatherResponse:
    """
    Retorna informações climáticas atuais e insights agrícolas para a cidade especificada.
    
    - **city**: Nome da cidade (ex: "São Paulo", "Ribeirão Preto")
    
    Retorna dados como temperatura, umidade, precipitação, vento, pressão,
    além de análises específicas para cultivo de cana-de-açúcar.
    """
    try:
        
        if not city or city.strip() == "":
            raise HTTPException(status_code=400, detail="Nome da cidade é obrigatório")
        
        
        city_normalized = city.strip()
        
        
        weather_data = await weather_service.get_weather_by_city(city_normalized)
        
        return weather_data
        
    except Exception as e:
        
        error_message = str(e).lower()
        
        if "não encontrada" in error_message or "not found" in error_message:
            handle_city_not_found()
        elif "indisponíveis" in error_message or "unavailable" in error_message:
            handle_weather_data_unavailable()
        elif "clima" in error_message or "geocodificação" in error_message or "api" in error_message:
            handle_external_api_error()
        else:
            
            raise HTTPException(
                status_code=500,
                detail="Erro interno ao processar solicitação. Tente novamente."
            )


@router.get("/health", summary="Health check do serviço de clima")
async def health_check():
    """Endpoint para verificação de saúde do serviço"""
    return {"status": "healthy", "service": "weather-api"}