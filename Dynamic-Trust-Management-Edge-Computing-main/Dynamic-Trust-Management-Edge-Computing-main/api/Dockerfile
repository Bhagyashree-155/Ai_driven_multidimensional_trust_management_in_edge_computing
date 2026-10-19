# FROM python:3.10

# WORKDIR /app

# COPY . .

# RUN pip install --no-cache-dir fastapi uvicorn redis requests

# CMD ["python", "-u", "api/main.py"]

FROM python:3.10-slim
WORKDIR /app

COPY . .

RUN pip install --no-cache-dir fastapi uvicorn redis requests

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]