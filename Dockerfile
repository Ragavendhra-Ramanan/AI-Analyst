# Use Python 3.11 slim
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend and frontend code
COPY backend/ ./backend
COPY frontend/ ./frontend

# Create a startup script
RUN echo '#!/bin/bash\n\
export PORT=${PORT:-8080}\n\
export API_BASE_URL="http://localhost:8000"\n\
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 &\n\
streamlit run frontend/app_interface.py --server.port $PORT --server.address 0.0.0.0\n\
' > /app/start.sh && chmod +x /app/start.sh

# Expose the port that Cloud Run expects
EXPOSE $PORT

# Use the startup script
CMD ["/app/start.sh"]
