# Frontend - Clima Cana

Aplicação web Next.js para exibir informações climáticas relevantes para produtores de cana-de-açúcar.

## Tecnologias

- **Framework**: Next.js 14 (App Router)
- **Linguagem**: TypeScript
- **Estilização**: Tailwind CSS
- **HTTP Client**: Fetch API
- **Gerenciamento de Estado**: React hooks

## Estrutura

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx       # Layout principal
│   │   ├── page.tsx         # Página inicial
│   │   └── globals.css      # Estilos globais
│   ├── components/
│   │   ├── WeatherSearch.tsx # Formulário de busca
│   │   ├── WeatherCard.tsx  # Card com dados climáticos
│   │   ├── LoadingSpinner.tsx # Indicador de carregamento
│   │   └── ErrorMessage.tsx # Mensagens de erro
│   ├── services/
│   │   └── api.ts           # Cliente HTTP
│   ├── types/
│   │   └── weather.ts       # Tipos TypeScript
│   └── utils/
│       └── agricultural.ts  # Funções de análise agrícola
├── public/
├── package.json
├── tailwind.config.js
└── Dockerfile
```

## Componentes Principais

### WeatherSearch
Formulário para busca de cidade com:
- Campo de texto para nome da cidade
- Botão de busca
- Tratamento de erros de validação

### WeatherCard
Exibição dos dados climáticos com:
- Informações de localização
- Dados climáticos atuais
- Insights agrícolas
- Recomendações para o produtor

### LoadingSpinner
Indicador de carregamento durante requisições à API.

### ErrorMessage
Componente para exibir mensagens de erro de forma amigável.

## Estados da Aplicação

1. **Inicial**: Formulário de busca vazio
2. **Carregando**: Buscando dados da API
3. **Sucesso**: Exibindo informações climáticas
4. **Erro**: Mensagem de falha na busca

## Execução Local

```bash
# Instalar dependências
npm install

# Executar servidor de desenvolvimento
npm run dev

# Acessar aplicação
http://localhost:3000
```

## Build para Produção

```bash
# Criar build otimizado
npm run build

# Iniciar servidor de produção
npm start
```

## Design System

### Cores
- Primário: Verde (#2E7D32)
- Secundário: Azul (#1976D2)
- Fundo: Branco (#FFFFFF)
- Texto: Cinza escuro (#212121)

### Tipografia
- Títulos: Roboto, 24px, negrito
- Texto: Roboto, 16px, normal
- Dados: Roboto Mono, 20px, normal

### Responsividade
- Mobile: Layout em coluna única
- Tablet: Conteúdo centralizado
- Desktop: Largura máxima fixa

## Acessibilidade

- Navegação por teclado
- Contraste adequado
- Leitores de tela compatíveis
- Tamanhos de toque otimizados