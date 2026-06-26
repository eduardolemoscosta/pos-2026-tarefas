import os
from datetime import datetime
from functools import wraps
from pathlib import Path
from urllib.parse import urlparse
 
from dotenv import load_dotenv
import requests
from flask import Flask, flash, redirect, render_template, request, session, url_for
from authlib.integrations.flask_client import OAuth


load_dotenv(Path(__file__).with_name(".env"))

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

oauth.register(
    name="suap",
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    access_token_url="https://suap.ifrn.edu.br/o/token/",
    authorize_url="https://suap.ifrn.edu.br/o/authorize/",
    api_base_url="https://suap.ifrn.edu.br/api/",
)



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "access_token" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function



def load_env():
    env_path = Path(__file__).with_name(".env")
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())





def suap_request(method, path, token=None, **kwargs):
    headers = kwargs.pop("headers", {})
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.request(
        method,
        f"{oauth.suap.api_base_url}{path}",
        headers=headers,
        timeout=20,
        **kwargs,
    )
    response.raise_for_status()
    return response.json()


def first_present(*values, default=""):
    for value in values:
        if value not in (None, ""):
            return value
    return default

def get_user_context():
    profile = session.get("profile") or {}
    student = session.get("student") or {}
    username = session.get("username", "")
    name = first_present(profile.get("nome"), student.get("nome"), username, default="Aluno")

    return {
        "name": name,
        "username": username,
        "email": first_present(profile.get("email"), student.get("email_academico"), student.get("email_escolar")),
        "avatar_url": first_present(profile.get("url_foto_75x100"), profile.get("url_foto"), student.get("url_foto")),
    }


def fetch_user_data():
    token = session["access_token"]
    profile = suap_request("GET", "/rh/meus-dados/", token=token)
    student = suap_request("GET", "/ensino/meus-dados-aluno/", token=token)
    session["profile"] = profile
    session["student"] = student


def save_token_session(token_data, username=""):
    access_token = token_data.get("access") or token_data.get("access_token")
    refresh_token = token_data.get("refresh") or token_data.get("refresh_token")

    if not access_token:
        raise KeyError("access_token")

    session.clear()
    session["username"] = username or token_data.get("username", "")
    session["access_token"] = access_token
    session["refresh_token"] = refresh_token
    fetch_user_data()


def fetch_report_card(year, period):
    page = 1
    results = []
    payload = {"count": 0, "next": None, "previous": None, "results": []}

    while True:
        payload = suap_request(
            "GET",
            f"/ensino/meu-boletim/{year}/{period}/",
            token=session["access_token"],
            params={"page": page},
        )
        results.extend(payload.get("results", []))
        if not payload.get("next"):
            break
        page += 1

    payload["results"] = results
    return payload


@app.context_processor
def inject_user():
    return {
        "current_user": get_user_context() if "access_token" in session else None,
        "current_year": datetime.now().year,
    }


@app.template_filter("label")
def label(value):
    return str(value).replace("_", " ").title()


@app.template_filter("pretty")
def pretty(value):
    if value is True:
        return "Sim"
    if value is False:
        return "Nao"
    if value in (None, ""):
        return "-"
    return value

@app.route("/")
def index():
    return render_template("index.html")

# Garante que a função se chama exatamente 'login'
@app.route("/login")
def login():
    redirect_uri = os.getenv("REDIRECT_URI", "http://localhost:8000/login/authorized")
    redirect_base = urlparse(redirect_uri)
    expected_host_url = f"{redirect_base.scheme}://{redirect_base.netloc}/"

    if request.host_url != expected_host_url:
        return redirect(f"{expected_host_url.rstrip('/')}{url_for('login')}")

    return oauth.suap.authorize_redirect(redirect_uri)

@app.route("/login/authorized", methods=["GET", "POST"])
def authorized():
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logging.debug(">>> authorized chamado")
    logging.debug(f">>> args: {request.args}")
    
    try:
        error = request.args.get("error")
        if error:
            return f"Erro no login: {error}", 400

        token = oauth.suap.authorize_access_token()
        logging.debug(f">>> token: {token}")
        session["access_token"] = token.get("access_token")
        session["refresh_token"] = token.get("refresh_token")
        fetch_user_data()
        return redirect(url_for("profile"))
    except Exception as e:
        logging.debug(f">>> ERRO: {str(e)}")
        return f"Erro: {str(e)}", 500


@app.route("/logout")
def logout():
    session.clear()
    flash("Voce saiu da sessao.", "info")
    return redirect(url_for("index"))


@app.route("/perfil")
@login_required
def profile():    
    try:
        if not session.get("profile") or not session.get("student"):
            fetch_user_data()
    except requests.RequestException:
        flash("Nao foi possivel atualizar seus dados agora.", "warning")

    return render_template(
        "profile.html",
        profile=session.get("profile", {}),
        student=session.get("student", {}),
    )


@app.route("/boletim")
@login_required
def report_card():
    year = request.args.get("ano", str(datetime.now().year), type=int)
    period = request.args.get("periodo", 1, type=int)
    years = list(range(datetime.now().year, datetime.now().year - 6, -1))
    boletim = {"count": 0, "results": []}

    try:
        boletim = fetch_report_card(year, period)
    except requests.HTTPError as error:
        status = error.response.status_code if error.response else "?"
        flash(f"Nao foi possivel carregar o boletim. Status {status}.", "danger")
    except requests.RequestException:
        flash("Nao foi possivel conectar ao SUAP para carregar o boletim.", "danger")

    return render_template(
        "boletim.html",
        boletim=boletim,
        selected_year=year,
        selected_period=period,
        years=years,
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=False, use_reloader=False)

