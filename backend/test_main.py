from fastapi.testclient import TestClient
from main import app  # Importa o app do seu arquivo main.py

client = TestClient(app)

# Testes para a nova rota /mod2/
def test_mod2_par():
    """
    Testa se um número par (10) é corretamente identificado.
    """
    response = client.get("/mod2/10")
    assert response.status_code == 200
    assert response.json() == {"number": 10, "result": "par"}

def test_mod2_impar():
    """
    Testa se um número ímpar (7) é corretamente identificado.
    """
    response = client.get("/mod2/7")
    assert response.status_code == 200
    assert response.json() == {"number": 7, "result": "impar"}

def test_mod2_zero():
    """
    Testa o caso especial do número zero.
    """
    response = client.get("/mod2/0")
    assert response.status_code == 200
    assert response.json() == {"number": 0, "result": "par"}

def test_mod2_entrada_invalida():
    """
    Testa se o FastAPI trata corretamente uma entrada que não é um inteiro.
    """
    response = client.get("/mod2/abc")
    # O FastAPI deve retornar 422 Unprocessable Entity para erro de validação de tipo
    assert response.status_code == 422
