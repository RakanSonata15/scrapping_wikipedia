# Gunakan image Python versi terbaru
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Salin file requirements.txt ke container
COPY requirements.txt .

# Install dependencies dari requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file dari proyek ke direktori /app di dalam container
COPY . .

# Expose port yang digunakan FastAPI
EXPOSE 8000

# Jalankan aplikasi menggunakan Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
