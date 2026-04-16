# Використовуємо базовий образ Python
FROM python:3.10-slim

# Встановлюємо робочу директорію в контейнері
WORKDIR /app

# Спочатку копіюємо requirements.txt (це пришвидшує білд)
COPY requirements.txt .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо ваш перейменований скрипт app.py
COPY app.py .

# Запускаємо застосунок
CMD ["python", "app.py"]