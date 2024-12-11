FROM python:3.9-slim

WORKDIR /app

# Install dependencies first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create non-root user for security
RUN useradd -m myuser
USER myuser

# Command is now in docker-compose.yml for flexibility
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]