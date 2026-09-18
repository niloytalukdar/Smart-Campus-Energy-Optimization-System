FROM python:3.11-slim

WORKDIR /app
COPY GridWise-AI/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY GridWise-AI .

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]