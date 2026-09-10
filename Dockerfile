# 1. Base Image: Python 3.11 slim (lightweight, secure)
FROM python:3.11-slim

# 2. Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# 3. Set working directory inside the container
WORKDIR /app

# 4. Install essential build tools & PostgreSQL client libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 5. Copy dependency definitions first for Docker layer caching
COPY requirements.txt .

# 6. Upgrade packaging tools & install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel msgpack && \
    pip install --no-cache-dir -r requirements.txt

# 7. Create a dedicated non-root user and group for security
RUN groupadd -r appgroup && useradd -r -g appgroup -d /app -s /sbin/nologin appuser

# 8. Copy only required application files
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini .

# 9. Change file ownership to the non-root user
RUN chown -R appuser:appgroup /app

# 10. Switch to the non-root user
USER appuser

# 11. Expose FastAPI default port
EXPOSE 8000

# 12. Command to run the application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
