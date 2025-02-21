FROM python:3.9-slim

WORKDIR /app

COPY voicevox_tts_api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY voicevox_tts_api/ .

# 新しいエントリーポイントを指定
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
