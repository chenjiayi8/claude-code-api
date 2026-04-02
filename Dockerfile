FROM python:3.12-slim

WORKDIR /app

# Install Claude Code CLI
RUN apt-get update && apt-get install -y curl git && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g @anthropic-ai/claude-code && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create non-root user (Claude CLI refuses --dangerously-skip-permissions as root)
RUN useradd -m -s /bin/bash appuser && \
    chown -R appuser:appuser /app

# Install Python dependencies as root (pip needs write access)
COPY pyproject.toml setup.py ./
RUN pip install --no-cache-dir -e .

# Copy application code
COPY claude_code_api/ ./claude_code_api/

# Create directories the app needs — .claude must be writable for session persistence
RUN mkdir -p /tmp/claude_projects /home/appuser/.claude/projects /home/appuser/.claude/sessions && \
    chown -R appuser:appuser /tmp/claude_projects /home/appuser/.claude

USER appuser

EXPOSE 8000

CMD ["uvicorn", "claude_code_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
