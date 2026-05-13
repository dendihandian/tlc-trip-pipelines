FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/* .

# Gabungkan inisialisasi dan perintah penjaga agar container tetap aktif
CMD ["sh", "-c", "python init_datalake.py && tail -f /dev/null"]