FROM python:3.10-slim

WORKDIR /app

COPY server.py .

CMD ["python3", "server.py"]
