import requests

BASE_URL = "https://jsonplaceholder.typicode.com/users"

def list():
    """Lista todos os usuários."""
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        return response.json()
    return []

def create(user_data):
    """Cria um novo usuário (simulado pela API)."""
    response = requests.post(BASE_URL, json=user_data)
    if response.status_code == 201:
        return response.json()
    return None

def read(user_id):
    """Busca um usuário pelo ID."""
    response = requests.get(f"{BASE_URL}/{user_id}")
    if response.status_code == 200:
        return response.json()
    return None

def update(user_id, user_data):
    """Atualiza os dados de um usuário pelo ID."""
    response = requests.put(f"{BASE_URL}/{user_id}", json=user_data)
    if response.status_code == 200:
        return response.json()
    return None

def delete(user_id):
    """Deleta um usuário pelo ID."""
    response = requests.delete(f"{BASE_URL}/{user_id}")
    # O JSONPlaceholder retorna 200 OK para remoções bem-sucedidas
    return response.status_code in [200, 204]