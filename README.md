# Clima Cana - Informações Climáticas para Produtores de Cana-de-Açúcar

Aplicação fullstack que fornece informações climáticas atuais e insights agrícolas relevantes para produtores de cana-de-açúcar.

## 🌾 Sobre o Projeto

Esta aplicação foi desenvolvida como parte do desafio técnico para Engenheiro(a) de Software Fullstack. O objetivo é criar uma ferramenta simples e eficaz que ajude produtores rurais a monitorar condições climáticas que impactam diretamente o cultivo de cana-de-açúcar.

### Funcionalidades

- ✅ Busca de informações climáticas por nome de cidade
- ✅ Dados atuais: temperatura, umidade, precipitação, vento, pressão
- ✅ Insights agrícolas personalizados para cana-de-açúcar
- ✅ Sistema de análise de risco (baixo, médio, alto)
- ✅ Recomendações baseadas nas condições climáticas
- ✅ Interface responsiva e acessível
- ✅ Deploy simplificado com Docker Compose

## 🏗️ Arquitetura da Solução

### Stack Tecnológico

#### Backend
- **Framework**: FastAPI (Python)
- **Validação**: Pydantic
- **HTTP Client**: httpx
- **API Externa**: Open-Meteo (sem autenticação)

### Entradas do Cache
Cada entrada contém:
- Dados serializados
- Timestamp de criação
- Timestamp de expiração

### TTLs Padrão

- **Geocodificação**: 24 horas (dados mudam raramente)
- **Clima**: 5 minutos (dados mudam frequentemente)
- **Padrão**: 5 minutos para outras funções


#### Frontend
- **Framework**: Next.js 14 (App Router)
- **Linguagem**: TypeScript
- **Estilização**: Tailwind CSS
- **Gerenciamento de Estado**: React hooks

#### Infraestrutura
- **Containerização**: Docker
- **Orquestração**: Docker Compose
- **Comunicação**: HTTP/HTTPS

### Estrutura do Projeto

```
/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── main.py         # Configuração do FastAPI
│   │   ├── api/routes/     # Rotas da API
│   │   ├── services/       # Lógica de negócio
│   │   ├── models/         # Modelos Pydantic
│   │   └── utils/          # Utilitários
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # Aplicação Next.js
│   ├── src/
│   │   ├── app/            # Páginas e layout
│   │   ├── components/     # Componentes React
│   │   ├── services/       # Cliente HTTP
│   │   ├── types/          # Tipos TypeScript
│   │   └── utils/          # Funções utilitárias
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yaml     # Orquestração dos serviços
└── README.md               # Este arquivo
```

## 🚀 Como Executar o Projeto

### Pré-requisitos

- Docker e Docker Compose instalados
- Git para clonar o repositório

### Passo a Passo

1. **Clonar o repositório**
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd fullstack-job
   ```

2. **Criar o arquivo docker-compose.yaml**
   ```bash
   # Copie o conteúdo de docker-compose-content.md para docker-compose.yaml
   ```

3. **Iniciar os serviços**
   ```bash
   docker compose up
   ```

4. **Acessar a aplicação**
   - Frontend: http://localhost:3000
   - API Documentation: http://localhost:8000/docs

### Comandos Úteis

```bash
# Iniciar em modo detached
docker compose up -d

# Parar os serviços
docker compose down

# Ver logs
docker compose logs -f

# Reconstruir imagens
docker compose up --build
```

## 📊 Funcionamento da Aplicação

### Fluxo de Dados

1. **Usuário** digita o nome da cidade no frontend
2. **Frontend** envia requisição para `/weather?city=NomeCidade`
3. **Backend** usa Geocoding API para obter coordenadas
4. **Backend** consulta Weather API com as coordenadas
5. **Backend** processa dados e gera insights agrícolas
6. **Frontend** exibe informações de forma clara e objetiva

### Dados Climáticos Fornecidos

- **Temperatura**: Impacta crescimento da cana
- **Umidade**: Influencia doenças e pragas
- **Precipitação**: Crucial para irrigação
- **Vento**: Afeta pulverização e evapotranspiração
- **Pressão**: Indicador de mudanças climáticas
- **Cobertura de nuvens**: Afeta radiação solar

### Análise de Risco Agrícola

#### Risco Alto
- Temperatura > 35°C ou < 10°C
- Precipitação > 50mm em 24h
- Vento > 40km/h
- Umidade < 30% ou > 90%

#### Risco Médio
- Temperatura entre 30-35°C ou 10-15°C
- Precipitação entre 20-50mm
- Vento entre 25-40km/h
- Umidade entre 30-40% ou 80-90%

#### Risco Baixo
- Temperatura entre 15-30°C
- Precipitação < 20mm
- Vento < 25km/h
- Umidade entre 40-80%

## 🎨 Decisões de Design e Arquitetura

### Frontend
- **Next.js**: Escolhido pela simplicidade de deploy e performance
- **Tailwind CSS**: Desenvolvimento rápido e design consistente
- **TypeScript**: Segurança de tipos e melhor DX
- **Design responsivo**: Foco em dispositivos móveis (público rural)

### Backend
- **FastAPI**: Alta performance e documentação automática
- **Pydantic**: Validação robusta de dados
- **httpx**: Cliente HTTP assíncrono moderno
- **Estrutura em camadas**: Separação clara de responsabilidades

### Integração
- **Open-Meteo**: API gratuita e sem autenticação
- **Wrapper pattern**: Backend abstrai complexidade da API externa
- **Tratamento de erros**: Respostas amigáveis para o usuário
- **Cache simples**: Melhora performance e reduz chamadas

## 📄 Licença

Este projeto foi desenvolvido exclusivamente para o processo seletivo e demonstração técnica.
