"""Modelo para a entidade Aluno(nome, idade)."""
from app.models.database import conexao


class Aluno:
    @staticmethod
    def validar(nome, idade):
        nome = (nome or "").strip()
        if len(nome) < 2 or len(nome) > 100:
            raise ValueError("O nome deve ter entre 2 e 100 caracteres.")
        try:
            if isinstance(idade, bool):
                raise ValueError
            idade_num = int(idade)
        except (TypeError, ValueError) as erro:
            raise ValueError("A idade deve ser um número inteiro.") from erro
        if not 0 <= idade_num <= 120 or str(idade_num) != str(idade).strip():
            raise ValueError("Informe uma idade inteira entre 0 e 120.")
        return nome, idade_num

    @staticmethod
    def listar():
        with conexao() as db:
            linhas = db.execute("SELECT id, nome, idade FROM alunos ORDER BY id").fetchall()
        return [dict(item) for item in linhas]

    @staticmethod
    def buscar(aluno_id):
        with conexao() as db:
            item = db.execute("SELECT id, nome, idade FROM alunos WHERE id = ?", (aluno_id,)).fetchone()
        return dict(item) if item else None

    @staticmethod
    def criar(nome, idade):
        nome, idade = Aluno.validar(nome, idade)
        with conexao() as db:
            cursor = db.execute("INSERT INTO alunos(nome, idade) VALUES (?, ?)", (nome, idade))
            aluno_id = cursor.lastrowid
        return Aluno.buscar(aluno_id)

    @staticmethod
    def atualizar(aluno_id, nome, idade):
        nome, idade = Aluno.validar(nome, idade)
        with conexao() as db:
            cursor = db.execute(
                "UPDATE alunos SET nome = ?, idade = ? WHERE id = ?", (nome, idade, aluno_id)
            )
            alterado = cursor.rowcount > 0
        return Aluno.buscar(aluno_id) if alterado else None

    @staticmethod
    def excluir(aluno_id):
        with conexao() as db:
            cursor = db.execute("DELETE FROM alunos WHERE id = ?", (aluno_id,))
            return cursor.rowcount > 0
