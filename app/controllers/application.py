"""Controller da aplicacao, preservando a classe Application do codigo-base."""
import hashlib
import hmac
import secrets
from pathlib import Path

from bottle import request, template
from app.models.database import inicializar
from app.models.user_account import User_account

VIEWS = str(Path(__file__).resolve().parents[1] / "views")
_CHAVE_CSRF = secrets.token_bytes(32)


class Application:
    def __init__(self):
        inicializar()

    def render(self, view, **dados):
        return template(view, template_lookup=[VIEWS], **dados)

    def usuario_atual(self):
        return User_account.obter_por_sessao(request.get_cookie("session"))

    def csrf_token(self):
        token = request.get_cookie("session") or ""
        return hmac.new(_CHAVE_CSRF, token.encode(), hashlib.sha256).hexdigest()

    def csrf_valido(self):
        enviado = request.forms.get("csrf", "")
        return bool(request.get_cookie("session")) and hmac.compare_digest(
            enviado, self.csrf_token()
        )
