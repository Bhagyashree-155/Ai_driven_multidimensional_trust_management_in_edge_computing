FROM python:3.10-slim
WORKDIR /app

COPY . .

RUN pip install --no-cache-dir flask requests psutil

CMD ["python", "app.py"]