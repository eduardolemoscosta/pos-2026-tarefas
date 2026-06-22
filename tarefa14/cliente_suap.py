import requests
from getpass import getpass

api_url = "https://suap.ifrn.edu.br/api"

user = input("user: ")
password = getpass()

data = {"username": user, "password": password}

response = requests.post(f"{api_url}/token/pair", json=data)

token_data = response.json()

token = token_data["access"]

headers = {"Authorization": f"Bearer {token}"}

response = requests.get(f"{api_url}/v2/minhas-informacoes/meus-dados/", headers=headers)
response = requests.get(f"{api_url}/ensino/meus-dados-aluno/", headers=headers)
response = requests.get(f"{api_url}/ensino/meu-boletim/2025/1", headers=headers)
print(response.text)
print(response)