# Frontend
FROM node:18-bullseye AS frontend
WORKDIR /app
COPY package.json vite.config.ts ./
COPY client ./client
RUN npm install --no-audit --no-fund && npx vite build --config vite.config.ts

# Backend
FROM python:3.12-slim AS backend
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./alembic.ini
COPY start.sh /usr/local/bin/start.sh
RUN sed -i 's/\r$//' /usr/local/bin/start.sh && chmod +x /usr/local/bin/start.sh
RUN mkdir -p app/static && true
COPY --from=frontend /app/dist/public/ ./app/static/
ENV PORT=8000
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --retries=5 CMD curl -fsS http://localhost:${PORT:-8000}/healthz || exit 1
CMD ["sh","-c","/usr/local/bin/start.sh"]
