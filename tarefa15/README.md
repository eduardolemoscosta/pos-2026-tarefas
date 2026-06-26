# Cliente SUAP Flask

Aplicacao Flask para autenticar no SUAP IFRN, exibir perfil do usuario e consultar boletim por ano e periodo.

## Como rodar

No terminal, a partir da raiz do repositorio:

```powershell
.\venv\Scripts\python.exe exemplo\exemplos\tarefaFinal2\suap_flask\app.py
```

Abra:

```text
http://127.0.0.1:5000/
```

## OAuth com redirecionamento

Se voce tiver uma aplicacao cadastrada no SUAP, crie `suap_flask/.env` com:

```env
SUAP_OAUTH_CLIENT_ID=seu_client_id
SUAP_OAUTH_CLIENT_SECRET=seu_client_secret
SUAP_OAUTH_REDIRECT_URI=http://127.0.0.1:5000/oauth/callback
FLASK_SECRET_KEY=uma_chave_qualquer
```

## Endpoints SUAP usados

- `POST /api/token/pair`
- `GET /api/rh/meus-dados/`
- `GET /api/ensino/meus-dados-aluno/`
- `GET /api/ensino/meu-boletim/{ano_letivo}/{periodo_letivo}/`
