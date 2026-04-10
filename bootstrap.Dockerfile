# builds the container image for the bootstrap node
# run bootstrap py
# port 5000
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY bootstrap.py .
CMD ["python", "bootstrap.py"]
