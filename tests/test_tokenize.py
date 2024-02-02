import requests
from openai import OpenAI

openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

models = client.models.list()
model = models.data[0].id


def test_tokenize():
    url = "http://localhost:8000/tokenize"
    data = {"prompt": "What is the weather today?", "model": model}
    response = requests.post(url, json=data)

    print(response.json())

    assert response.status_code == 200


def test_tokenize_sagemaker():
    url = "http://localhost:8000/invocations"
    data = {"prompt": "What is the weather today?", "model": model}
    response = requests.post(url, json={"endpoint": "/tokenize", "payload": data})

    print(response.json())

    assert response.status_code == 200


def test_chat_tokenize():
    url = "http://localhost:8000/tokenize"
    data = {
        "messages": [{"role": "user", "content": "What is the weather today?"}],
        "model": model,
    }
    response = requests.post(url, json=data)

    print(response.json())

    assert response.status_code == 200


def test_chat_tokenize_sagemaker():
    url = "http://localhost:8000/invocations"
    data = {
        "messages": [{"role": "user", "content": "What is the weather today?"}],
        "model": model,
    }
    response = requests.post(url, json={"endpoint": "/tokenize", "payload": data})

    print(response.json())

    assert response.status_code == 200


def test_invalid_payload_1():
    url = "http://localhost:8000/tokenize"
    data = {
        "prompt": "What is the weather today?",
        "messages": [{"role": "user", "content": "What is the weather today?"}],
        "model": model,
    }
    response = requests.post(url, json=data)

    print(response.json())

    assert response.status_code == 400


def test_invalid_payload_2():
    url = "http://localhost:8000/tokenize"
    data = {"model": model}
    response = requests.post(url, json=data)

    print(response.json())

    assert response.status_code == 400


def test_invalid_model():
    url = "http://localhost:8000/tokenize"
    data = {"prompt": "What is the weather today?", "model": "invalid_model"}
    response = requests.post(url, json=data)

    print(response.json())

    assert response.status_code == 404
