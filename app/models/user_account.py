"""Modelo User_account: usuarios, senhas com hash e sessoes revogaveis."""
import base64
import hashlib
import hmac
import re
import secrets
import sqlite3
import time

from app.models.database import conexao

ITERACOES = 260_000
DURACAO_SESSAO = 8 * 60 * 60


class User_account:
    @staticmethod
    def _hash_senha(senha):
        salt = secrets.token_bytes(16)
        derivada = hashlib.pbkdf2_hmac("sha256", senha.encode(), salt, ITERACOES)
        return "pbkdf2_sha256${}${}${}".format(
            ITERACOES,
            base64.b64encode(salt).decode(),
            base64.b64encode(derivada).decode(),
        )

    @staticmethod
    def _confere_senha(senha, armazenada):
        try:
            algoritmo, repeticoes, salt, original = armazenada.split("$")
            if algoritmo != "pbkdf2_sha256":
                return False
            derivada = hashlib.pbkdf2_hmac(
                "sha256", senha.encode(), base64.b64decode(salt), int(repeticoes)
            )
            return hmac.compare_digest(derivada, base64.b64decode(original))
        except (ValueError, TypeError):
            return False

    @staticmethod
    def criar(usuario, senha):
        usuario = (usuario or "").strip()
        if not re.fullmatch(r"[A-Za-z0-9_.-]{3,32}", usuario):
            raise ValueError("O usuário deve ter 3 a 32 caracteres: letras, números, _, . ou -.")
        if len(senha or "") < 8:
            raise ValueError("A senha precisa ter pelo menos 8 caracteres.")
        try:
            with conexao() as db:
                cursor = db.execute(
                    "INSERT INTO user_account (usuario, senha_hash) VALUES (?, ?)",
                    (usuario, User_account._hash_senha(senha)),
                )
                return cursor.lastrowid
        except sqlite3.IntegrityError as erro:
            raise ValueError("Este nome de usuário já está cadastrado.") from erro

    @staticmethod
    def autenticar(usuario, senha):
        with conexao() as db:
            registro = db.execute(
                "SELECT id, usuario, senha_hash FROM user_account WHERE usuario = ?",
                ((usuario or "").strip(),),
            ).fetchone()
        if registro and User_account._confere_senha(senha or "", registro["senha_hash"]):
            return {"id": registro["id"], "usuario": registro["usuario"]}
        return None

    @staticmethod
    def iniciar_sessao(usuario_id):
        token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        agora = int(time.time())
        with conexao() as db:
            db.execute("DELETE FROM sessoes WHERE expira_em <= ?", (agora,))
            db.execute(
                "INSERT INTO sessoes(token_hash, usuario_id, expira_em) VALUES (?, ?, ?)",
                (token_hash, usuario_id, agora + DURACAO_SESSAO),
            )
        return token

    @staticmethod
    def obter_por_sessao(token):
        if not token:
            return None
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        with conexao() as db:
            registro = db.execute("""
                SELECT user_account.id, user_account.usuario
                FROM sessoes JOIN user_account ON user_account.id = sessoes.usuario_id
                WHERE sessoes.token_hash = ? AND sessoes.expira_em > ?
            """, (token_hash, int(time.time()))).fetchone()
        return dict(registro) if registro else None

    @staticmethod
    def encerrar_sessao(token):
        if token:
            token_hash = hashlib.sha256(token.encode()).hexdigest()
            with conexao() as db:
                db.execute("DELETE FROM sessoes WHERE token_hash = ?", (token_hash,))
