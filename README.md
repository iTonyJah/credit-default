Сессионное задание по курсу Внедрение моделей машинного обучения

# 🏦 Сервис прогнозирования дефолта по кредитным картам (MLOps Pipeline)

##  Описание
Production-ready веб-сервис для бинарной классификации клиентов кредитных карт на вероятность дефолта в следующем месяце. Проект охватывает полный цикл внедрения ML-модели: от обучения пайплайна и сериализации до контейнеризации, оркестрации и планирования A/B-тестирования.

Домен: Финансы / Кредитный скоринг  
Датасет: [Default of Credit Card Clients (UCI)](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients)

## 🛠 Технологический стек
- **Python 3.12**, `scikit-learn`, `pandas`, `numpy`, `joblib`
- **Flask** (REST API)
- **Docker**, **Docker Compose** (контейнеризация и оркестрация)
- **pytest / requests** (тестирование API)

## 📁 Структура проекта
```text
credit-default/
── app/                       # 📂 Директория с кодом веб-сервиса
│   ├── __init__.py           # (пустой файл, делает папку пакетом Python)
│   └── main.py               # 📄 Flask-код (запуск сервера)
├── models/                   # 📂 Папка для сохраненных моделей
│   └── model_pipeline.joblib # 📦 Сериализованный пайплайн
├── notebooks/                # 📂 Папка для Jupyter Notebooks
│   └── model_training.ipynb  # 📓 Ноутбук с обучением модели
├── tests/                    # 📂 Папка для тестов/клиента
│   └── client.py             # 📄 Скрипт для проверки API
├── .gitignore                # 📄 Файл для игнорирования мусора
├── .dockerignore             # 📄 Файл для игнорирования мусора
├── Dockerfile                # 📄 Инструкция для сборки образа
├── docker-compose.yml        # 📄 Оркестрация
├── kill_5000.sh              # 📄 Скрипт для очистки порта 5000 
├── requirements.txt          # 📄 Зависимости
├── requirements-dev.txt      # 📄 Зависимости для разработчиков
├── ARCHITECTURE.md           # 📄 Обоснование архитектуры и MLOps-концепты
├── AB_TEST_PLAN.md           # 📄 План A/B-тестирования
└── README.md                 # 📄 Документация
```

# Как запустить локально:
```bash
# 1. Создать и активировать виртуальное окружение
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Запустить сервер
python app/main.py
# Сервер доступен по http://localhost:5000
```
```bash
# 4. В другом терминале запустить тесты
python tests/client.py
```

# Сборка, запуск и проверка в Docker

```bash
# Сборка образа
docker build -t credit-default-api .

# Запуск контейнера
docker run -d --name credit-api -p 5000:5000 credit-default-api

# Или через Docker Compose (оркестрация)
docker compose up -d
```

# 🌐 API Документация

**`GET /health`**

Проверка работоспособности сервиса.

**Ответ:**

```{"status": "ok", "service": "credit_default_predictor", "model_loaded": true, "timestamp": "..."}```

**`POST /predict`**

Принимает JSON с 23 признаками клиента, возвращает класс дефолта и вероятность.

**Формат запроса:**
```json
{
  "LIMIT_BAL": 50000, "SEX": 1, "EDUCATION": 2, "MARRIAGE": 1, "AGE": 35,
  "PAY_0": 0, "PAY_2": 0, "PAY_3": 0, "PAY_4": 0, "PAY_5": 0, "PAY_6": 0,
  "BILL_AMT1": 20000, "BILL_AMT2": 19000, "BILL_AMT3": 18000, "BILL_AMT4": 17000, "BILL_AMT5": 16000, "BILL_AMT6": 15000,
  "PAY_AMT1": 2000, "PAY_AMT2": 1500, "PAY_AMT3": 1000, "PAY_AMT4": 800, "PAY_AMT5": 500, "PAY_AMT6": 300
}
```

**Формат ответа:**
```json
{
  "prediction": 0,
  "probability": 0.1245,
  "class": "no_default"
}
```

**Примеры ```curl```**

```bash
# Проверка здоровья
curl -X GET http://localhost:5000/health

# Предсказание
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"LIMIT_BAL":50000,"SEX":1,"EDUCATION":2,"MARRIAGE":1,"AGE":35,"PAY_0":0,"PAY_2":0,"PAY_3":0,"PAY_4":0,"PAY_5":0,"PAY_6":0,"BILL_AMT1":20000,"BILL_AMT2":19000,"BILL_AMT3":18000,"BILL_AMT4":17000,"BILL_AMT5":16000,"BILL_AMT6":15000,"PAY_AMT1":2000,"PAY_AMT2":1500,"PAY_AMT3":1000,"PAY_AMT4":800,"PAY_AMT5":500,"PAY_AMT6":300}'
  ```

  # 🐳 Docker Hub

Образ доступен для публичного скачивания:

# 📚 Дополнительная документация
* [🏗 Архитектура и MLOps-концепты](ARCHITECTURE.md)
* [⚖️ План A/B-тестирования](AB_TEST_PLAN.md)