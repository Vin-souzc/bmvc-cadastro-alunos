"""Testes HTTP locais, sem bibliotecas adicionais para testes."""
import http.cookiejar
import json
import os
import tempfile
import threading
import unittest
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, Request, build_opener
from wsgiref.simple_server import WSGIRequestHandler, make_server

_TEMP_DIR = tempfile.TemporaryDirectory()
os.environ['BMVC_DB_PATH'] = os.path.join(_TEMP_DIR.name, 'teste.sqlite3')
from main import app  # noqa: E402 (configurar banco antes de importar)


class QuietHandler(WSGIRequestHandler):
    def log_message(self, fmt, *args):
        pass


class TestePortal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.servidor = make_server('127.0.0.1', 0, app, handler_class=QuietHandler)
        cls.base = 'http://127.0.0.1:' + str(cls.servidor.server_port)
        cls.thread = threading.Thread(target=cls.servidor.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.servidor.shutdown()
        cls.thread.join(timeout=5)
        cls.servidor.server_close()
        _TEMP_DIR.cleanup()

    def setUp(self):
        self.client = build_opener(HTTPCookieProcessor(http.cookiejar.CookieJar()))

    def enviar(self, rota, metodo='GET', dados=None, json_body=False):
        headers = {}
        if dados is not None:
            if json_body:
                dados = json.dumps(dados).encode()
                headers['Content-Type'] = 'application/json'
            else:
                dados = urlencode(dados).encode()
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
        req = Request(self.base + rota, data=dados, headers=headers, method=metodo)
        return self.client.open(req)

    def test_fluxo_completo(self):
        with self.assertRaises(HTTPError) as negado:
            self.enviar('/api/alunos')
        self.assertEqual(negado.exception.code, 401)

        with self.enviar('/banco') as tela:
            self.assertIn(b'Entrar', tela.read())

        self.enviar('/registrar', 'POST', {'usuario': 'aluno_teste', 'senha': 'senha-supersegura'})
        with self.enviar('/login', 'POST', {'usuario': 'aluno_teste', 'senha': 'senha-supersegura'}) as pagina:
            self.assertIn(b'Cadastro de alunos', pagina.read())

        with self.enviar('/api/alunos', 'POST', {'nome': 'Ana Silva', 'idade': 19}, True) as resp:
            self.assertEqual(resp.status, 201)
            aluno = json.load(resp)['aluno']
        with self.enviar('/api/alunos') as resp:
            self.assertTrue(any(a['id'] == aluno['id'] for a in json.load(resp)['alunos']))
        with self.enviar('/api/alunos/' + str(aluno['id']), 'PUT', {'nome': 'Ana Souza', 'idade': 20}, True) as resp:
            self.assertEqual(json.load(resp)['aluno']['idade'], 20)
        with self.enviar('/api/alunos/' + str(aluno['id']), 'DELETE') as resp:
            self.assertIn('excluído', json.load(resp)['mensagem'])
        with self.enviar('/api/alunos') as resp:
            self.assertEqual(json.load(resp)['alunos'], [])

        with self.assertRaises(HTTPError) as invalido:
            self.enviar('/api/alunos', 'POST', {'nome': 'A', 'idade': 130}, True)
        self.assertEqual(invalido.exception.code, 400)


if __name__ == '__main__':
    unittest.main()
