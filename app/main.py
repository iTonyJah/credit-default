"""
Flask-сервис для прогнозирования дефолта по кредитным картам.
Реализует REST API с эндпоинтами /health и /predict.
"""

import os
import json
import logging
from datetime import datetime

import numpy as np
import pandas as pd
import joblib
from flask import Flask, request, jsonify

# ==============================================================================
# 1. Инициализация приложения и логирования
# ==============================================================================
app = Flask(__name__)

# Настраиваем JSON-логирование (как требуется в задании, Часть 3)
# В production такие логи собираются ELK-стеком (Elasticsearch + Logstash + Kibana)
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
)
logger = logging.getLogger(__name__)

# ==============================================================================
# 2. Загрузка модели ОДИН РАЗ при старте приложения
# ==============================================================================
# Согласно лекциям (Модуль 1), модель загружается вне функций-обработчиков,
# чтобы не тратить ресурсы на каждый запрос.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '..', 'models', 'model_pipeline.joblib')

try:
    pipeline = joblib.load(MODEL_PATH)
    logger.info(f"Модель успешно загружена из {MODEL_PATH}")
except FileNotFoundError:
    logger.error(f"Файл модели не найден: {MODEL_PATH}")
    raise RuntimeError("Модель не загружена. Проверьте путь к model_pipeline.joblib")

# Список признаков, которые ожидает модель (без ID и без target)
EXPECTED_FEATURES = [
    'LIMIT_BAL', 'SEX', 'EDUCATION', 'MARRIAGE', 'AGE',
    'PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6',
    'BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6',
    'PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6'
]


# ==============================================================================
# 3. Эндпоинт GET /health — проверка работоспособности
# ==============================================================================
@app.route('/health', methods=['GET'])
def health_check():
    """
    Проверка работоспособности сервиса.
    Возвращает статус OK и информацию о загруженной модели.
    """
    return jsonify({
        "status": "ok",
        "service": "credit_default_predictor",
        "model_loaded": pipeline is not None,
        "timestamp": datetime.utcnow().isoformat()
    }), 200


# ==============================================================================
# 4. Эндпоинт POST /predict — предсказание дефолта
# ==============================================================================
@app.route('/predict', methods=['POST'])
def predict():
    """
    Принимает JSON с признаками клиента и возвращает прогноз дефолта.
    
    Формат запроса (JSON):
    {
        "LIMIT_BAL": 50000,
        "SEX": 1,
        "EDUCATION": 2,
        "MARRIAGE": 1,
        "AGE": 35,
        "PAY_0": 0,
        "PAY_2": 0,
        "PAY_3": 0,
        "PAY_4": 0,
        "PAY_5": 0,
        "PAY_6": 0,
        "BILL_AMT1": 20000,
        "BILL_AMT2": 19000,
        "BILL_AMT3": 18000,
        "BILL_AMT4": 17000,
        "BILL_AMT5": 16000,
        "BILL_AMT6": 15000,
        "PAY_AMT1": 2000,
        "PAY_AMT2": 1500,
        "PAY_AMT3": 1000,
        "PAY_AMT4": 800,
        "PAY_AMT5": 500,
        "PAY_AMT6": 300
    }
    
    Формат ответа (JSON):
    {
        "prediction": 0,
        "probability": 0.15,
        "class": "no_default"
    }
    """
    try:
        # Получаем JSON из запроса
        data = request.get_json()
        
        if data is None:
            logger.warning("Получен запрос без JSON-тела")
            return jsonify({"error": "Request body must be JSON"}), 400
        
        # Валидация: проверяем наличие всех необходимых признаков
        missing_features = [f for f in EXPECTED_FEATURES if f not in data]
        if missing_features:
            logger.warning(f"Отсутствуют признаки: {missing_features}")
            return jsonify({
                "error": "Missing features",
                "missing": missing_features
            }), 400
        
        # Преобразуем JSON в DataFrame (важно для ColumnTransformer с именами столбцов!)
        # Пайплайн ожидает DataFrame с правильными именами столбцов
        df_input = pd.DataFrame([data])[EXPECTED_FEATURES]
        
        # Делаем предсказание класса
        prediction = pipeline.predict(df_input)[0]
        
        # Получаем вероятность (predict_proba возвращает массив [prob_0, prob_1])
        probabilities = pipeline.predict_proba(df_input)[0]
        probability_default = float(probabilities[1])  # вероятность класса 1 (дефолт)
        
        # Формируем ответ
        result = {
            "prediction": int(prediction),
            "probability": round(probability_default, 4),
            "class": "default" if prediction == 1 else "no_default"
        }
        
        # Логируем запрос и ответ в JSON-формате (для ELK-стека в production)
        logger.info(f"Request: {json.dumps(data)}, Response: {json.dumps(result)}")
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Ошибка при обработке запроса: {str(e)}")
        return jsonify({"error": str(e)}), 500


# ==============================================================================
# 5. Запуск приложения
# ==============================================================================
if __name__ == '__main__':
    # host='0.0.0.0' необходим для доступа из Docker-контейнера
    # (широковещательный адрес, как указано в лекциях, Модуль 2)
    app.run(host='0.0.0.0', port=5000, debug=False)