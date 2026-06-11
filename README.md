# credit-default
Сессионное задание по курсу Внедрение моделей МЛ

# Структура проекта
```text
credit-default/
── app/                       # 📂 Директория с кодом веб-сервиса
│   ├── __init__.py           # (пустой файл, делает папку пакетом Python)
│   └── main.py               # 📄 Flask-код (server.py)
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
venv\Scripts\activate     # Windows

# 2. Установите зависимости
pip install -r requirements.txt
```
```bash
# 3. Запустите сервер
python app/main.py
```
```bash
# 4. В другом терминале запустите тесты
python tests/client.py
```
