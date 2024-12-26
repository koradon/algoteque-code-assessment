FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt ./

RUN echo "requirements.txt"

RUN cat requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./service ./service

# Command to run the application
CMD ["uvicorn", "service.main:app", "--host", "0.0.0.0", "--port", "8000"]
