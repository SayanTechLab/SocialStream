# Use an official, lightweight Python image
FROM python:3.11-slim

# Force Python logs to show up immediately in deployment consoles
ENV PYTHONUNBUFFERED=True

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (ffmpeg is required for yt-dlp media conversions)
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code (app.py, templates/, static/)
COPY . .

# Expose the port Gunicorn will listen on
EXPOSE 8080

# Run the web service using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "4", "--timeout", "120", "app:app"]