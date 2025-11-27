# Backend - Clima Cana

API FastAPI para fornecer informações climáticas relevantes para produtores de cana-de-açúcar.

## Tecnologias

- **Framework**: FastAPI
- **Linguagem**: Python 3.11+
- **Validação**: Pydantic
- **HTTP Client**: httpx

## Estrutura

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Configuração do FastAPI
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── weather.py   # Rotas de clima
│   ├── services/
│   │   ├── __init__.py
│   │   └── weather_service.py # Integração Open-Meteo
│   ├── models/
│   │   ├── __init__.py
│   │   └── weather.py       # Modelos Pydantic
│   └── utils/
│       ├── __init__.py
│       └── exceptions.py    # Exceções customizadas
├── requirements.txt
└── Dockerfile
```

## Endpoints

### GET /weather
Retorna informações climáticas atuais para uma cidade.

**Parâmetros:**
- `city` (query): Nome da cidade

**Resposta:**
```json
{
  "location": {
    "name": "São Paulo",
    "latitude": -23.5505,
    "longitude": -46.6333
  },
  "current": {
    "temperature": 25.3,
    "humidity": 70,
    "precipitation": 0.0,
    "wind_speed": 12.5,
    "pressure": 1013.2,
    "cloud_cover": 40,
    "last_updated": "2023-11-26T14:30:00Z"
  },
  "agricultural_insights": {
    "risk_level": "low",
    "recommendations": [
      "Condições favoráveis para colheita",
      "Monitorar umidade nas próximas 48h"
    ]
  }
}
```

## Execução Local

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Acesse `http://localhost:8000/docs` para documentação interativa.