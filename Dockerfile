# Используем стабильный базовый образ Python, совместимый с новыми библиотеками
FROM python:3.12-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения и модель
COPY app/ ./app/
COPY models/ ./models/

# Открываем порт 5000 (на котором работает Flask)
EXPOSE 5000

# Команда запуска приложения
# host=0.0.0.0 уже указан в app/main.py, поэтому контейнер будет доступен снаружи
CMD ["python", "app/main.py"]
