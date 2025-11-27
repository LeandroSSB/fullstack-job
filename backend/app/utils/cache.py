import asyncio
import hashlib
import json
import logging
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Dict, Optional, TypeVar, Union
from ..config import settings

logger = logging.getLogger(__name__)

T = TypeVar('T')


class CacheEntry:
    """Entrada de cache com timestamp e TTL"""
    
    def __init__(self, data: Any, ttl: int):
        self.data = data
        self.created_at = datetime.now()
        self.expires_at = self.created_at + timedelta(seconds=ttl)
    
    def is_expired(self) -> bool:
        """Verifica se a entrada de cache expirou"""
        return datetime.now() > self.expires_at


class MemoryCache:
    """Implementação de cache em memória thread-safe"""
    
    def __init__(self, max_size: int = 1000):
        self._cache: Dict[str, CacheEntry] = {}
        self._max_size = max_size
        self._lock = asyncio.Lock()
    
    async def get(self, key: str) -> Optional[Any]:
        """Obtém um valor do cache"""
        async with self._lock:
            if key not in self._cache:
                return None
            
            entry = self._cache[key]
            if entry.is_expired():
                del self._cache[key]
                logger.debug(f"Cache expired for key: {key}")
                return None
            
            logger.debug(f"Cache hit for key: {key}")
            return entry.data
    
    async def set(self, key: str, value: Any, ttl: int) -> None:
        """Define um valor no cache"""
        async with self._lock:
            # Remove entradas mais antigas se o cache estiver cheio
            if len(self._cache) >= self._max_size:
                await self._evict_oldest()
            
            self._cache[key] = CacheEntry(value, ttl)
            logger.debug(f"Cache set for key: {key}, TTL: {ttl}s")
    
    async def delete(self, key: str) -> bool:
        """Remove uma entrada do cache"""
        async with self._lock:
            if key in self._cache:
                del self._cache[key]
                logger.debug(f"Cache deleted for key: {key}")
                return True
            return False
    
    async def clear(self) -> None:
        """Limpa todo o cache"""
        async with self._lock:
            self._cache.clear()
            logger.debug("Cache cleared")
    
    async def _evict_oldest(self) -> None:
        """Remove a entrada mais antiga do cache"""
        if not self._cache:
            return
        
        oldest_key = min(self._cache.keys(), 
                        key=lambda k: self._cache[k].created_at)
        del self._cache[oldest_key]
        logger.debug(f"Evicted oldest cache entry: {oldest_key}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do cache"""
        return {
            "size": len(self._cache),
            "max_size": self._max_size,
            "keys": list(self._cache.keys())
        }


# Instância global do cache
cache = MemoryCache(max_size=settings.cache_max_size)


def cache_key_generator(*args, **kwargs) -> str:
    """Gera uma chave de cache única baseada nos argumentos"""
    # Serializa argumentos para JSON
    key_data = {
        "args": [str(arg) for arg in args],
        "kwargs": {k: str(v) for k, v in kwargs.items()}
    }
    
    # Gera hash MD5 para criar chave única
    key_json = json.dumps(key_data, sort_keys=True)
    return hashlib.md5(key_json.encode()).hexdigest()


def cached(ttl: Optional[int] = None, key_prefix: str = ""):
    """
    Decorator para cache de funções assíncronas
    
    Args:
        ttl: Time to live em segundos. Se None, usa o TTL padrão
        key_prefix: Prefixo para a chave do cache
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            # Verifica se o cache está habilitado
            if not settings.cache_enabled:
                return await func(*args, **kwargs)
            
            # Gera chave do cache
            key_parts = [key_prefix, func.__name__]
            key = ":".join(key_parts) + ":" + cache_key_generator(*args, **kwargs)
            
            # Tenta obter do cache
            cached_result = await cache.get(key)
            if cached_result is not None:
                return cached_result
            
            # Executa a função e armazena no cache
            result = await func(*args, **kwargs)
            
            # Usa TTL fornecido ou um padrão baseado no tipo de função
            effective_ttl = ttl
            if effective_ttl is None:
                # TTL padrão baseado no nome da função
                if "geocod" in func.__name__.lower():
                    effective_ttl = settings.cache_ttl_geocoding
                elif "weather" in func.__name__.lower():
                    effective_ttl = settings.cache_ttl_weather
                else:
                    effective_ttl = 300  # 5 minutos padrão
            
            await cache.set(key, result, effective_ttl)
            return result
        
        # Adiciona métodos de controle de cache à função decorada
        wrapper.cache_key = lambda *args, **kwargs: ":".join([key_prefix, func.__name__]) + ":" + cache_key_generator(*args, **kwargs)
        wrapper.invalidate_cache = lambda *args, **kwargs: cache.delete(wrapper.cache_key(*args, **kwargs))
        wrapper.clear_cache = lambda: cache.clear()
        wrapper.cache_stats = lambda: cache.get_stats()
        
        return wrapper
    
    return decorator


# Funções utilitárias para controle do cache
async def invalidate_pattern(pattern: str) -> int:
    """
    Invalida todas as entradas do cache que correspondem a um padrão
    
    Args:
        pattern: Padrão para buscar nas chaves (pode ser substring)
    
    Returns:
        Número de entradas removidas
    """
    stats = cache.get_stats()
    removed_count = 0
    
    for key in stats["keys"]:
        if pattern in key:
            if await cache.delete(key):
                removed_count += 1
    
    logger.info(f"Invalidated {removed_count} cache entries matching pattern: {pattern}")
    return removed_count


async def get_cache_info() -> Dict[str, Any]:
    """Retorna informações detalhadas sobre o cache"""
    stats = cache.get_stats()
    
    # Adiciona informações de configuração
    stats.update({
        "enabled": settings.cache_enabled,
        "ttl_geocoding": settings.cache_ttl_geocoding,
        "ttl_weather": settings.cache_ttl_weather,
        "max_size": settings.cache_max_size
    })
    
    return stats