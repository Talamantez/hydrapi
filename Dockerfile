FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN useradd -m myuser
USER myuser
# Print actual command being executed
ENTRYPOINT ["sh", "-c", "echo 'Command being run:' $0 $@; exec $0 $@"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]