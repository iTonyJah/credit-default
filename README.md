# credit-default
Сессионное задание по курсу Внедрение моделей машинного обучения

# Структура проекта
```text
credit-default/
── app/                       # 📂 Директория с кодом веб-сервиса
│   ├── __init__.py           # (пустой файл, делает папку пакетом Python)
│   └── main.py               # 📄 Flask-код (запуск сервера)
├── models/                   # 📂 Папка для сохраненных моделей
│   └── model_pipeline.joblib # 📦 Сериализованный пайплайн
├── notebooks/                # 📂 Папка для Jupyter Notebooks
│   └── model_training.ipynb  # 📓 Ноутбук с обучением модели
├── tests/                    #  Папка для тестов/клиента
│   └── client.py             # 📄 Скрипт для проверки API
├── .gitignore                # 📄 Файл для игнорирования мусора
├── Dockerfile                #  Инструкция для сборки образа
├── docker-compose.yml        # 📄 Оркестрация
├── requirements.txt          # 📄 Зависимости
└── README.md                 # 📄 Документация
```

# Как запустить локально:
```bash
# 1. Активируйте виртуальное окружение
source venv/bin/activate  # Linux/Mac
# или
# venv\Scripts\activate     # Windows

# 2. Установите зависимости
pip install -r requirements.txt

# 3. Запустите сервер
python app/main.py
```
```bash
# 4. В другом терминале запустите тесты
python tests/client.py
```

# Сборка, запуск и проверка в Docker
```bash
# 1. Собираем образ
docker build -t credit_default_api .

# 2. Запускаем контейнер (вариант 1: через docker run)
# docker run -d --name credit_default_test -p 5000:5000 credit_default_api

# ИЛИ вариант 2: через docker compose (рекомендуется)
docker compose up -d

# 3. Проверяем, что контейнер работает
docker ps

# 4. Смотрим логи контейнера
docker logs credit_default_test
# или
docker compose logs -f credit_default_api
```
