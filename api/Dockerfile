FROM python:3.12-slim

WORKDIR /app

COPY COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ .

# Hot reload con flask --debug
RUN useradd -U -u 1000 appuser && chown -R 1000:1000 /app
USER 1000
CMD ["flask", "--app", "app.py", "run", "--host=0.0.0.0", "--port=5000", "--debug"]
