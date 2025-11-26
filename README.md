# Atividade técnica – Engenheiro(a) de Software Fullstack

Construção de uma aplicação onde o usuário informa o nome de uma cidade e recebe como resposta **as informações do clima atual** da região.

A aplicação será composta de:

- **Frontend** (web ou mobile) que permita inserir uma cidade e exibir os dados de clima atual.
- **Backend** com **uma rota obrigatória**, que receberá a cidade enviada pelo frontend e retornará o clima atual.
- **Docker Compose** orquestrando frontend e backend, garantindo que se comuniquem corretamente.

## O que será avaliado?

- Estruturação clara de frontend (web ou mobile) e backend
- Organização do código e arquitetura geral da solução
- Tratamento de estados assíncronos (carregando, erro, sucesso)
- Consumo e composição de dados da API externa
- Decisões técnicas adotadas e clareza na documentação
- Coerência da solução com o objetivo do produto
- Otimização e simplicidade da implementação

---

## Contexto

Você deve criar uma aplicação de página única que permita ao usuário buscar informações do **clima atual** informando o nome de uma cidade.

Esses dados devem ajudar produtores de cana-de-açúcar a monitorar fatores relevantes para o desenvolvimento saudável do canavial (ex.: temperatura, chuva, vento, umidade).  
A definição de quais dados destacar fica a seu critério.

**Não existe um formato predefinido de resposta** — a interpretação da API e a forma de expor os dados fazem parte da avaliação.

---

## Implementação backend

- Desenvolva uma rota que retorna as informações do clima dado o nome de uma cidade.
- Essa rota deve funcionar como um **wrapper** da API do Open-Meteo.
- Utilize apenas HTTPS.
- Estruturas adicionais (serviços, validações, tratamento de erro, cache etc.) são bem-vindas se fizerem sentido à sua solução.

O backend deve ser implementado em **Python com [FastAPI](https://fastapi.tiangolo.com/)**.

> A API Open-Meteo não exige autenticação.  
> Consulte a documentação oficial e utilize conforme seu entendimento:
> <https://open-meteo.com>/

---

## Implementação frontend

- Desenvolva uma página única onde o usuário digita uma cidade.
- O frontend deve se comunicar com o backend para obter os dados climáticos.
- A apresentação deve ser clara, objetiva e alinhada ao contexto do produtor rural.

O frontend deve ser feito com **Next.js (web)** ou **React Native (Expo - mobile)**.

---

## Deploy

- No caso da aplicação web, utilize **docker-compose** para subir frontend e backend e permitir a comunicação entre eles.
- A aplicação deve funcionar com um único comando:

```bash
docker compose up
```

- Para interfaces mobile, adicione as instruções de como acessar a aplicação no README do projeto

## Estrutura sugerida do projeto

```markdown
backend/
frontend/
docker-compose.yaml
README.md
```

## Entregas

- Link para o repositório GitHub contendo frontend, backend e docker-compose
- Aplicação funcionando de forma integrada
- README explicando:
  - como rodar o projeto
  - decisões de arquitetura e design adotadas
  - (opcional) sugestões de melhorias futuras

O envio deve ser feito para **<contato@canac.com.br>**, com o assunto: Desafio Fullstack – {Seu nome}, até o prazo descrito no e-mail
