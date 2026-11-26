# UniMaster AI Pro v7.0 — Universal Container Image
# Tương thích 100% với: Hugging Face Spaces, Koyeb, Render, Railway, Fly.io
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    DATA_DIR=/data

WORKDIR /app

# Cài đặt dependencies siêu tốc
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn
COPY . .

# Tạo thư mục data và phân quyền ghi đầy đủ (cho phép chạy UID 1000 trên Hugging Face Spaces hoặc Koyeb non-root)
RUN mkdir -p /data && chmod -R 777 /app /data

# Mở cổng 8080 (Koyeb / Render / Cloud Run) và 7860 (Hugging Face Spaces)
EXPOSE 8080
EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s CMD python -c "import urllib.request,os;urllib.request.urlopen(f'http://127.0.0.1:{os.environ.get(\"PORT\",\"8080\")}/healthz',timeout=4)"

CMD ["python", "server.py"]
