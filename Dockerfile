FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN useradd -m myuser
RUN chmod +x /app/start.sh
USER myuser
CMD ["/bin/bash", "/app/start.sh"]