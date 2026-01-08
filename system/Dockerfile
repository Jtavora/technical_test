FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho
WORKDIR /app

# Dependências de sistema (psycopg2 etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# 👇 Aqui é a parte importante:
# Em vez de copiar o conteúdo de system direto pra /app,
# vamos copiar para /app/system, preservando o pacote "system".
COPY . /app/system

# Instalar requirements (agora dentro de /app/system)
RUN pip install --no-cache-dir -r /app/system/requirements.txt

EXPOSE 8000

# Alembic agora está em /app/system/alembic.ini
# e migrations em /app/system/migrations
CMD ["sh", "-c", "alembic -c /app/system/alembic.ini upgrade head && uvicorn system.app.main:app --host 0.0.0.0 --port 8000"]