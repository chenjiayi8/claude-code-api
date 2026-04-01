FROM python:3.12-slim

WORKDIR /app

# Install Claude Code CLI
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g @anthropic-ai/claude-code && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml setup.py ./
RUN pip install --no-cache-dir -e .

# Copy application code
COPY claude_code_api/ ./claude_code_api/

EXPOSE 8000

CMD ["uvicorn", "claude_code_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
