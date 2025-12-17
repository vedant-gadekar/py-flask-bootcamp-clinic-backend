# 1. Base image
FROM python:3.10-slim

# 2. Set working directory
WORKDIR /app

# 3. Install system dependencies (needed for psycopg2, bcrypt, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy dependency files first (better caching)
COPY pyproject.toml poetry.lock* ./

# 5. Install Poetry
RUN pip install --no-cache-dir poetry

# 6. Configure Poetry
RUN poetry config virtualenvs.create false

# 7. Install dependencies
RUN poetry install --no-root

# 8. Copy rest of the application
COPY . .

# 9. Expose Flask port
EXPOSE 5000

# 10. Run the app
CMD ["python", "run.py"]
