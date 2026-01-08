# 📧 Email Assistant – Technical Test

Sistema completo para **classificação inteligente de e-mails** utilizando **FastAPI + PostgreSQL + React + OpenAI GPT-4o**.  
Permite classificar, revisar, editar e listar e-mails com interface moderna e API bem estruturada.

---

## 🎯 1. Escopo do Protótipo

### ✅ O que está dentro do escopo

- API em FastAPI para:
  - Classificar e-mails via LLM (GPT-4o).
  - Persistir e-mails, classificação, confiança, rascunho e flag de revisão humana.
  - Atualizar classificação/rascunho após revisão.
  - Listar e detalhar e-mails classificados.
- Integração com PostgreSQL usando SQLAlchemy + Alembic.
- Frontend em React (Vite + MUI) com:
  - Tela de **Classificação** de novo e-mail.
  - Tela de **Listagem** com filtros por categoria e “somente revisão humana”.
  - Modal de detalhes para revisar/editar e salvar.
  - Feedback visual (loading, snackbar ao salvar).
- Orquestração em Docker Compose (db + api + frontend).
- Documentação:
  - README detalhado.
  - Diagramas de arquitetura, sequência e atividade em PlantUML.
  - Arquivos `.envExample` para backend e frontend.

### 🚧 O que fica para depois (próximas iterações)

- Autenticação e autorização (usuários/roles).
- Integração real com IMAP/SMTP para leitura/envio de e-mails.
- Paginação e filtros avançados no backend.
- Painel de métricas e relatórios (ex.: CSV/Excel).
- Deploy em cloud (ex.: AWS/GCP/Azure).
- Fine-tuning/few-shot baseado em dados reais do cliente.

---

## 🏛️ 2. Arquitetura Técnica (alto nível)

Fluxo principal:

- Frontend React → HTTP/JSON → FastAPI Backend → SQL → PostgreSQL  
                                      ↓  
                                      OpenAI GPT-4o (LLM)

### Componentes

- **Frontend** (React + Vite + MUI, servido por Nginx)
  - Páginas:
    - Classificação de e-mail.
    - Listagem de e-mails.
    - Modal de detalhes/edição.
  - Comunicação com a API via Axios usando a variável `VITE_API_URL`.

- **Backend** (FastAPI)
  - Camada `api`: definição de rotas HTTP, validação de entrada, schemas de resposta.
  - Camada `services`: orquestra regra de negócio (chama LLM, aplica limiar de confiança, fala com repositórios).
  - Camada `domain`: entidades de domínio (ex.: `Email`, `ClassificationResult`, `EmailCategory`).
  - Camada `infrastructure`:
    - Cliente OpenAI (`OpenAILLMClient`) com prompt engineering.
    - Cliente “dummy” que simula respostas quando não há `OPENAI_API_KEY`.
    - Engine de banco (SQLAlchemy).
  - Camada `schemas`: modelos Pydantic para entrada/saída (DTOs).
  - Migrações de banco com Alembic.

- **Banco de Dados** (PostgreSQL 16)
  - Tabela principal `emails`:
    - Campos como `from_email`, `subject`, `body`, `category`, `confidence`, `draft_reply`, `requires_human_review`, `created_at`.

- **OpenAI GPT-4o**
  - Usado via API HTTP.
  - Recebe prompt estruturado com instruções e categorias.
  - Retorna JSON com classificação, confiança, rascunho de resposta e flag de revisão humana.

---

## 🧰 3. Stack Tecnológica

- **FastAPI**  
  Escolhido pela velocidade de desenvolvimento, suporte a async, tipagem forte e documentação automática com Swagger.

- **PostgreSQL**  
   Persistir e-mails e metadados.

- **SQLAlchemy + Alembic**  
  ORM flexível e com suporte a migrations via Alembic, permitindo evoluir o schema com segurança.

- **React + Vite + Material UI**  
  - React é utilizado bastante em diversos projetos.
  - Vite oferece desenvolvimento rápido e build otimizado.
  - MUI fornece componentes prontos, responsivos e visualmente agradáveis para um dashboard administrativo.

- **OpenAI GPT-4o (API)**  
  - Dispensa treinamento e manutenção de modelos.
  - Focado em linguagem natural, ideal para interpretação de e-mails.
  - Permite prototipar rapidamente sem custo de infraestrutura de IA.

- **Docker Compose**  
  - Facilita subir todo o ambiente com um comando.
  - Garante que avaliadores rodem o sistema de forma previsível e isolada.

---

## 🧠 4. Estratégia de IA

### Abordagem escolhida

- **LLM API (GPT-4o) + Prompt Engineering + Regras de Negócio.**

O backend envia para a OpenAI:

- Um **system prompt** explicando:
  - As categorias possíveis (FEEDBACK_NEGATIVO, FEEDBACK_POSITIVO, GARANTIA, ARREPENDIMENTO_REEMBOLSO, DUVIDAS_GERAIS, INCONCLUSIVO).
  - Regras para confiança (0 a 1).
  - Quando marcar `requires_human_review`.
  - Formato de resposta em JSON.

- Um **user prompt** contendo:
  - Remetente.
  - Assunto.
  - Corpo do e-mail.

O modelo retorna um JSON com:

- `classification`
- `confidence`
- `draft_reply`
- `requires_human_review`

No backend:

- Se `confidence < 0.7`, o sistema força `requires_human_review = true`.
- Se o JSON vier inválido, o sistema aplica um **fallback seguro**:
  - Classificação `INCONCLUSIVO`.
  - Confiança 0.0.
  - Rascunho padrão pedindo que a equipe avalie.

### Por que NÃO usar fine-tuning/RAG neste MVP?

- **Fine-tuning**:
  - Exige dataset rotulado significativo.
  - Eleva custo e complexidade sem ganho proporcional em um protótipo inicial.
- **RAG**:
  - Faz mais sentido quando há uma base documental extensa (FAQ, políticas, contratos).
  - Para classificação de e-mails curtos e bem delimitados, o prompt engineering é suficiente.

A abordagem atual maximiza **velocidade de entrega**, **simplicidade** e **manutenibilidade**.

---

## ⚠️ 5. Riscos e Mitigação

| Risco | Impacto | Mitigação |
|------|---------|-----------|
| Falta de `OPENAI_API_KEY` | IA não funciona | Cliente LLM “dummy” que retorna classificações simuladas para fins de teste |
| JSON inválido do modelo | Quebra na API | Tratamento de exceção, `try/except` e fallback para `INCONCLUSIVO` com mensagem padrão |
| Latência alta da API OpenAI | UX ruim no frontend | Exibição de loading no botão e na listagem, possibilidade futura de cache/local queue |
| Custos da OpenAI | Limitação de uso | Uso controlado, apenas em ambiente de teste/demonstração; log por request no backend |
| Crescimento de volume no banco | Consultas lentas | Estrutura já preparada para receber paginação e índices; pode ser adicionado futuramente |
| E-mails ambíguos/sensíveis | Risco de resposta inadequada | Regra de confiança + flag de revisão humana para forçar análise manual |

---

## 📏 6. Métricas de Sucesso do Protótipo

Algumas métricas sugeridas para avaliar a viabilidade:

- **Acurácia percebida**:  
  Percentual de e-mails cuja classificação foi aceita sem alteração manual.

- **Taxa de revisão humana**:  
  Percentual de e-mails marcados com `requires_human_review = true`.

- **Tempo médio de resposta**:  
  Tempo entre envio da requisição `/emails/classify` e resposta concluída.

- **Volume processado**:  
  Quantidade de e-mails classificados automaticamente em um período de teste.

- **Feedback qualitativo do time**:  
  Impressão dos usuários sobre:
  - Qualidade dos rascunhos.
  - Utilidade dos filtros.
  - Facilidade de revisar e editar.

---

## 📁 Estrutura do Projeto

    /
    ├── system/                # Backend (FastAPI)
    │   ├── app/
    │   │   ├── api/
    │   │   ├── core/
    │   │   ├── domain/
    │   │   ├── infrastructure/
    │   │   ├── services/
    │   │   ├── schemas/
    │   │   ├── .envExample
    │   │   └── main.py
    │   ├── migrations/
    │   ├── alembic.ini
    │   └── Dockerfile
    │
    ├── frontend/              # React App
    │   ├── src/
    │   ├── public/
    │   ├── nginx.conf
    │   ├── Dockerfile
    │   ├── .envExample
    │   └── vite.config.js
    │
    └── docker-compose.yml

---

## ⚙️ Configuração

### 🔒 Backend – arquivo `.env` (system/app/.env)

1. Copiar arquivo de exemplo:

       cp system/app/.envExample system/app/.env

2. Preencher com algo como:

       ENV=DEV
       APP_NAME=Email Classification API
       APP_VERSION=1.0.0

       DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/email_db

       OPENAI_API_KEY=sua-chave-aqui
       OPENAI_MODEL=gpt-4o-mini

> Sem `OPENAI_API_KEY`, o backend usa automaticamente um cliente de classificação “dummy” apenas para testes (sem chamada real na OpenAI).

---

### 🎨 Frontend – arquivo `.env` (frontend/.env)

1. Copiar arquivo de exemplo:

       cp frontend/.envExample frontend/.env

2. Conteúdo esperado:

       VITE_API_URL=http://localhost:8000

---

## 🐳 Como rodar com Docker (recomendado)

Na raiz do projeto:

    docker compose up --build

Acessos:

- API: http://localhost:8000  
- Swagger: http://localhost:8000/docs  
- Frontend: http://localhost:3000  
- PostgreSQL: localhost:5432

---

## 🧪 Rodar localmente (sem Docker)

### Backend

    python -m venv venv
    source venv/bin/activate
    pip install -r system/requirements.txt
    cp system/app/.envExample system/app/.env   # e ajustar variáveis
    alembic -c system/alembic.ini upgrade head
    uvicorn system.app.main:app --reload

### Frontend

    cd frontend
    cp .envExample .env
    npm install
    npm run dev

---

## 📚 Endpoints principais

| Método | Rota                | Descrição                                     |
|--------|---------------------|-----------------------------------------------|
| GET    | `/health/ping`      | Healthcheck da API                           |
| POST   | `/emails/classify`  | Classifica e persiste um novo e-mail         |
| GET    | `/emails`           | Lista e-mails classificados                   |
| GET    | `/emails/{id}`      | Detalhes de um e-mail específico             |
| PUT    | `/emails/{id}`      | Atualiza categoria/rascunho/revisão humana   |

---

## 🧬 Diagramas (PlantUML)

![Arquitetura](PlantUML/out/comp.png) 

![Sequência](PlantUML/out/sequence.png) 

![Atividade](PlantUML/out/activity.png)

---

## 📨 Exemplo de JSON para testes

    {
      "from_email": "cliente@exemplo.com",
      "subject": "Meu produto chegou quebrado",
      "body": "Recebi hoje e está danificado. Gostaria de solicitar troca."
    }

---

## 🖼️ Prints do Sistema

### 📌 Tela de Classificação 
![Classificação](screenshots/classify_page.png)

 ### 📌 Listagem de E-mails 
 ![Lista](screenshots/list_page.png) 
 
 ### 📌 Modal de Detalhes 
 ![Detalhes](screenshots/details_modal.png) 
 
 ### 🎥 Demonstração (GIF) 
 ![Demo](screenshots/demo.gif)

---

## 💡 Possíveis melhorias futuras

- Autenticação (JWT, OAuth2, etc.).  
- Paginação e filtros avançados no endpoint `/emails`.  
- Integração direta com IMAP/SMTP (entrada e saída reais).  
- Exportação de relatórios (CSV/Excel).  
- Métricas e dashboard em tempo real (ex.: Grafana).  

---

## 📄 Licença

Projeto desenvolvido para **avaliação técnica**.  
Uso livre para estudo e referência.

---

## 👤 Autor

João Victor Dias Távora