# Build context: carpeta api/ (Root Directory en Railway = api)
FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN adduser -D -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

ENV PORT=5000
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT} app:app"]
