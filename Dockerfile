FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN useradd -m myuser
USER myuser
SHELL ["/bin/bash", "-c"]
CMD env && echo "PORT is: $PORT" && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}