# builds the container image for a P2P node
# Python base image, installs dependencies, and runs node.py
# container runs one node instance on port 5000 internally
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY node.py .
ENV PORT=5000
ENV PYTHONUNBUFFERED=1
# Scaled Compose sets HOSTNAME; manual runs can pass -e NODE_URL=http://node1:5000
# Default NODE_URL uses the same port the app listens on (needed when PORT=5001, 5002, …).
ENTRYPOINT ["sh", "-c", "export NODE_URL=\"${NODE_URL:-http://$HOSTNAME:${PORT:-5000}}\"; exec python node.py"]

