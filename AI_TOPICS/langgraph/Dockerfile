# --- Stage 1: Build dependencies ---
FROM ubuntu/python:3.12-24.04_stable

WORKDIR /app

# Install system dependencies needed to compile certain Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements to leverage Docker layer caching
COPY requirements.txt .

# Install dependencies into a localized wheels/virtual directory
RUN pip install --no-cache-dir --user -r requirements.txt


# --- Stage 2: Final lightweight runtime ---
FROM python:3.11-slim AS runner

WORKDIR /app

# Install runtime dependencies (e.g., git if using LangGraph remote sources)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy installed python dependencies from builder stage
COPY --from=builder /root/.local /root/.local
COPY . .

# Ensure the local pip binaries are accessible via PATH
ENV PATH=/root/.local/bin:$PATH

# Expose port (adjust if your LangChain/LangGraph API uses a different port like 8000 or 8080)
EXPOSE 8000

# Run application (Assuming Uvicorn/FastAPI serves your LangGraph application)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
