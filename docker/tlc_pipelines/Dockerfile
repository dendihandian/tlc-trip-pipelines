FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/* .

# Tetapkan container tetap hidup di background
CMD ["tail", "-f", "/dev/null"]