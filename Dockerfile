# Imagem base pequena com Python
FROM python:3.11-slim

# Evita buffers em logs
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential default-libmysqlclient-dev pkg-config python3-dev \
    && rm -rf /var/lib/apt/lists/*

# instalar dependências de compilação necessárias para mysqlclient
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential default-libmysqlclient-dev gcc \
    && rm -rf /var/lib/apt/lists/*


# Copia dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia a aplicação
COPY . .

# Expõe a porta usada pela app
EXPOSE 5001

# Comando de inicialização
CMD ["python", "app_mysql.py"]