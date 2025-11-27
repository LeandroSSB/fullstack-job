from fastapi import HTTPException


class WeatherAPIException(Exception):
    """Exceção base para erros da API de clima"""
    pass


class CityNotFoundException(WeatherAPIException):
    """Exceção quando cidade não é encontrada"""
    pass


class WeatherDataUnavailableException(WeatherAPIException):
    """Exceção quando dados climáticos não estão disponíveis"""
    pass


class ExternalAPIException(WeatherAPIException):
    """Exceção para erros em APIs externas"""
    pass


def handle_city_not_found():
    """Lança exceção HTTP para cidade não encontrada"""
    raise HTTPException(
        status_code=404,
        detail="Cidade não encontrada. Verifique o nome e tente novamente."
    )


def handle_weather_data_unavailable():
    """Lança exceção HTTP para dados indisponíveis"""
    raise HTTPException(
        status_code=503,
        detail="Dados climáticos temporariamente indisponíveis. Tente novamente mais tarde."
    )


def handle_external_api_error():
    """Lança exceção HTTP para erro em API externa"""
    raise HTTPException(
        status_code=502,
        detail="Erro ao consultar serviço de clima. Tente novamente mais tarde."
    )