"""
Клиентский скрипт для тестирования Flask-сервиса.
Использует библиотеку requests для отправки HTTP-запросов.
"""

import requests
import json

BASE_URL = "http://localhost:5000"

# Пример данных клиента из датасета (первая строка, без ID и target)
sample_client = {
    "LIMIT_BAL": 20000,
    "SEX": 2,
    "EDUCATION": 2,
    "MARRIAGE": 1,
    "AGE": 24,
    "PAY_0": 2,
    "PAY_2": 2,
    "PAY_3": -1,
    "PAY_4": -1,
    "PAY_5": -2,
    "PAY_6": -2,
    "BILL_AMT1": 3913,
    "BILL_AMT2": 3102,
    "BILL_AMT3": 689,
    "BILL_AMT4": 0,
    "BILL_AMT5": 0,
    "BILL_AMT6": 0,
    "PAY_AMT1": 0,
    "PAY_AMT2": 689,
    "PAY_AMT3": 0,
    "PAY_AMT4": 0,
    "PAY_AMT5": 0,
    "PAY_AMT6": 0
}


def test_health():
    """Тестирование эндпоинта /health"""
    print("=" * 50)
    print("Тест GET /health")
    print("=" * 50)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_predict():
    """Тестирование эндпоинта /predict"""
    print("=" * 50)
    print("Тест POST /predict")
    print("=" * 50)
    
    response = requests.post(
        f"{BASE_URL}/predict",
        json=sample_client,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_invalid_request():
    """Тестирование невалидного запроса (отсутствуют признаки)"""
    print("=" * 50)
    print("Тест POST /predict с невалидными данными")
    print("=" * 50)
    
    invalid_data = {"LIMIT_BAL": 50000}  #缺少其他特征
    
    response = requests.post(
        f"{BASE_URL}/predict",
        json=invalid_data
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


if __name__ == '__main__':
    print("Запуск тестов API...\n")
    
    try:
        test_health()
        test_predict()
        test_invalid_request()
        print("✅ Все тесты завершены!")
    except requests.exceptions.ConnectionError:
        print("❌ Ошибка подключения. Убедитесь, что сервер запущен:")
        print("   python app/main.py")


# ==============================================================================
# Примеры curl-команд (для README.md)
# ==============================================================================
#
# Проверка работоспособности:
# curl -X GET http://localhost:5000/health
#
# Предсказание:
# curl -X POST http://localhost:5000/predict \
#      -H "Content-Type: application/json" \
#      -d '{
#        "LIMIT_BAL": 50000,
#        "SEX": 1,
#        "EDUCATION": 2,
#        "MARRIAGE": 1,
#        "AGE": 35,
#        "PAY_0": 0,
#        "PAY_2": 0,
#        "PAY_3": 0,
#        "PAY_4": 0,
#        "PAY_5": 0,
#        "PAY_6": 0,
#        "BILL_AMT1": 20000,
#        "BILL_AMT2": 19000,
#        "BILL_AMT3": 18000,
#        "BILL_AMT4": 17000,
#        "BILL_AMT5": 16000,
#        "BILL_AMT6": 15000,
#        "PAY_AMT1": 2000,
#        "PAY_AMT2": 1500,
#        "PAY_AMT3": 1000,
#        "PAY_AMT4": 800,
#        "PAY_AMT5": 500,
#        "PAY_AMT6": 300
#      }'