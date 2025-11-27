from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Configurações da API
    api_title: str = "Clima Cana API"
    api_version: str = "1.0.0"
    debug: bool = False
    
    # Configurações de Cache
    cache_enabled: bool = True
    cache_ttl_geocoding: int = 86400  # 24 horas em segundos
    cache_ttl_weather: int = 300      # 5 minutos em segundos
    cache_max_size: int = 1000        # Número máximo de itens no cache
    
    # Configurações de timeout
    request_timeout: float = 10.0
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()