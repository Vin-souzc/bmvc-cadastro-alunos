"""Rotas do sistema BMVC. Execute: python main.py"""
from pathlib import Path

from app.controllers.application import Application
from app.models.aluno import Aluno
from app.models.user_account import DURACAO_SESSAO, User_account
from bottle import Bottle, request, static_file, redirect, response, run

app = Bottle()
ctl = Application()


# -----------------------------------------------------------------------------
# Rotas originais do codigo-base
@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root=str(Path(__file__).resolve().parent / 'app' / 'static'))


@app.route('/helper')
def helper(info=None):
    return ctl.render('helper')


# -----------------------------------------------------------------------------
# Portal (login de usuarios: modelo User_account)
@app.get('/')
def inicio():
    return redirect('/banco' if ctl.usuario_atual() else '/login')


@app.get('/login')
def tela_login():
    if ctl.usuario_atual():
        return redirect('/banco')
    return ctl.render('login', erro=None)


@app.post('/login')
def efetuar_login():
    usuario = User_account.autenticar(request.forms.get('usuario'), request.forms.get('senha'))
    if not usuario:
        response.status = 401
        return ctl.render('login', erro='Usuário ou senha incorretos.')
    token = User_account.iniciar_sessao(usuario['id'])
    response.set_cookie(
        'session', token, path='/', httponly=True, samesite='Lax',
        max_age=DURACAO_SESSAO, secure=(request.urlparts.scheme == 'https')
    )
    return redirect('/banco')


@app.get('/registrar')
def tela_registro():
    return ctl.render('registrar', erro=None)


@app.post('/registrar')
def efetuar_registro():
    try:
        User_account.criar(request.forms.get('usuario'), request.forms.get('senha'))
    except ValueError as erro:
        response.status = 400
        return ctl.render('registrar', erro=str(erro))
    return redirect('/login')


@app.post('/sair')
def sair():
    if ctl.usuario_atual() and not ctl.csrf_valido():
        response.status = 403
        return 'Ação não autorizada: token CSRF inválido.'
    User_account.encerrar_sessao(request.get_cookie('session'))
    response.delete_cookie('session', path='/')
    return redirect('/login')


# -----------------------------------------------------------------------------
# Banco: READ (obrigatorio) apresentado dentro do sistema
@app.get('/banco')
def banco():
    usuario = ctl.usuario_atual()
    if not usuario:
        return redirect('/login')
    return ctl.render('banco', usuario=usuario, alunos=Aluno.listar(),
                      csrf=ctl.csrf_token(), erro=None)


@app.post('/banco')
def cadastrar_pelo_site():
    usuario = ctl.usuario_atual()
    if not usuario:
        return redirect('/login')
    if not ctl.csrf_valido():
        response.status = 403
        return 'Ação não autorizada: token CSRF inválido.'
    try:
        Aluno.criar(request.forms.get('nome'), request.forms.get('idade'))
    except ValueError as erro:
        response.status = 400
        return ctl.render('banco', usuario=usuario, alunos=Aluno.listar(),
                          csrf=ctl.csrf_token(), erro=str(erro))
    return redirect('/banco')


@app.post('/banco/<aluno_id:int>/excluir')
def excluir_pelo_site(aluno_id):
    if not ctl.usuario_atual():
        return redirect('/login')
    if not ctl.csrf_valido():
        response.status = 403
        return 'Ação não autorizada: token CSRF inválido.'
    Aluno.excluir(aluno_id)
    return redirect('/banco')


# -----------------------------------------------------------------------------
# API: operacoes CREATE / READ / UPDATE / DELETE para cURL
# Use um cookie de sessao salvo com curl -c cookies.txt no POST /login.
def exigir_api():
    if not ctl.usuario_atual():
        response.status = 401
        return {'erro': 'Faça login antes de acessar o banco.'}
    return None


def dados_api():
    if request.content_type and 'application/json' in request.content_type:
        dados = request.json
    else:
        dados = dict(request.forms)
    if not isinstance(dados, dict):
        raise ValueError('Envie um objeto JSON ou dados de formulário.')
    return dados


@app.get('/api/alunos')
def listar_api():
    falha = exigir_api()
    if falha is not None:
        return falha
    return {'alunos': Aluno.listar()}


@app.post('/api/alunos')
def criar_api():
    falha = exigir_api()
    if falha is not None:
        return falha
    try:
        dados = dados_api()
        novo = Aluno.criar(dados.get('nome'), dados.get('idade'))
    except ValueError as erro:
        response.status = 400
        return {'erro': str(erro)}
    response.status = 201
    return {'mensagem': 'Aluno cadastrado com sucesso.', 'aluno': novo}


@app.put('/api/alunos/<aluno_id:int>')
def atualizar_api(aluno_id):
    falha = exigir_api()
    if falha is not None:
        return falha
    try:
        dados = dados_api()
        alterado = Aluno.atualizar(aluno_id, dados.get('nome'), dados.get('idade'))
    except ValueError as erro:
        response.status = 400
        return {'erro': str(erro)}
    if alterado is None:
        response.status = 404
        return {'erro': 'Aluno não encontrado.'}
    return {'mensagem': 'Aluno atualizado com sucesso.', 'aluno': alterado}


@app.delete('/api/alunos/<aluno_id:int>')
def excluir_api(aluno_id):
    falha = exigir_api()
    if falha is not None:
        return falha
    if not Aluno.excluir(aluno_id):
        response.status = 404
        return {'erro': 'Aluno não encontrado.'}
    return {'mensagem': 'Aluno excluído com sucesso.'}


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8080, debug=True)
