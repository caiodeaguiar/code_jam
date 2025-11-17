import pytest
from fastapi.testclient import TestClient
from pytest_bdd import scenario, scenarios, given, when, then, parsers

# Importe seu App FastAPI
# O PYTHONPATH no seu ci.yml (PYTHONPATH=.:) garante que isso funcione
from backend.app.main import app 

# --- Configuração (Fixtures) ---

@pytest.fixture
def client():
    """Fixture para o TestClient do FastAPI."""
    return TestClient(app)

@pytest.fixture
def context():
    """
    Fixture para compartilhar estado (ex: a resposta da API) 
    entre os passos 'when' e 'then'.
    """
    return {}

# --- Conexão com o arquivo .feature ---

# Isso diz ao pytest-bdd para procurar por arquivos .feature
# na pasta 'features' e implementar os cenários encontrados.
scenarios('features/mod2.feature')


# --- Implementação dos Passos (Step Definitions) ---

# CENÁRIO: Scenario Outline: Verificar números

@when(parsers.parse('Eu chamo a API /mod2/ com o número {numero}'))
def call_api_with_number(client, context, numero):
    """Implementa o passo 'When' para números."""
    context['numero'] = numero # Salva o número para a asserção
    context['response'] = client.get(f"/mod2/{numero}")

@then(parsers.parse('O resultado deve ser "{resultado}"'))
def check_numeric_result(context, resultado):
    """Implementa o passo 'Then' para resultados corretos."""
    response = context['response']
    numero_int = int(context['numero'])
    
    assert response.status_code == 200
    assert response.json() == {"number": numero_int, "result": resultado}

# CENÁRIO: Scenario: Verificar entrada inválida

@when(parsers.parse('Eu chamo a API /mod2/ com o texto "{texto}"'))
def call_api_with_text(client, context, texto):
    """Implementa o passo 'When' para texto inválido."""
    context['response'] = client.get(f"/mod2/{texto}")

@then('A API deve retornar um erro 422')
def check_422_error(context):
    """Implementa o passo 'Then' para o erro 422."""
    response = context['response']
    assert response.status_code == 422
