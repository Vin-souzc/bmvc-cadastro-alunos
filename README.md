# BMVC — Portal e Banco de Alunos

Projeto acadêmico em **Python**, com **Bottle**, separação em controllers, models e views e persistência em **SQLite**, baseado no código inicial disponibilizado na atividade.

## Requisitos atendidos

- **Portal**: cadastro e autenticação de usuários (`User_account`), sessão e saída.
- **Banco**: alunos com pelo menos dois atributos: **nome** e **idade**.
- **READ**: lista de alunos dentro do sistema, na rota protegida `/banco`.
- **CREATE** e **DELETE**: operações HTTP disponíveis via **cURL**, também acessíveis no portal.
- **UPDATE**: operação extra, disponível na API.
- Banco persistente SQLite, com instruções para execução em Linux.

## Estrutura do projeto

```text
main.py                        # Rotas Bottle (base da atividade)
app/controllers/application.py  # Controller Application + render
app/models/database.py         # Inicialização SQLite
app/models/user_account.py     # Modelo User_account e sessões
app/models/aluno.py            # Modelo Aluno
app/views/                    # Login, registro, banco e ajuda
app/static/style.css           # Estilos do portal
requirements.txt
```

## Como executar (terminal Linux)

É necessário Python 3.8 ou superior.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Acesse **http://localhost:8080/**, clique em **Criar usuário** e cadastre uma conta com senha de no mínimo 8 caracteres. Depois entre e acesse **http://localhost:8080/banco** para visualizar a lista (READ). O arquivo SQLite é criado automaticamente em `data/bmvc.sqlite3` (ignorado pelo Git).

## Operações usando cURL (Linux)

**1. Login e armazenamento do cookie de sessão** (troque pelas credenciais que você cadastrou):

```bash
curl -i -c cookies.txt -d 'usuario=SEU_USUARIO' -d 'senha=SUA_SENHA' http://localhost:8080/login
```

**2. READ — consultar alunos por API** (também existe no site em `/banco`):

```bash
curl -b cookies.txt http://localhost:8080/api/alunos
```

**3. CREATE — cadastrar aluno:**

```bash
curl -b cookies.txt -X POST http://localhost:8080/api/alunos \
  -H 'Content-Type: application/json' \
  -d '{"nome":"Ana Silva","idade":19}'
```

**4. UPDATE — atualizar aluno (extra):**

```bash
curl -b cookies.txt -X PUT http://localhost:8080/api/alunos/1 \
  -H 'Content-Type: application/json' \
  -d '{"nome":"Ana Souza","idade":20}'
```

**5. DELETE — excluir aluno:**

```bash
curl -b cookies.txt -X DELETE http://localhost:8080/api/alunos/1
```

Os IDs começam em 1 e podem mudar conforme os registros. Consulte o READ antes de apagar. O arquivo `cookies.txt` contém uma sessão; não publique nem compartilhe. A API responde em JSON e retorna `401` se não houver autenticação.

## Testes

```bash
python -m unittest discover -s tests -v
```

## Observações

- O portal também oferece formulário para cadastrar/excluir com proteção CSRF.
- Senhas usam PBKDF2-HMAC-SHA256 com salt; sessões ficam no banco e podem ser revogadas ao sair.
- A aplicação é um exemplo de **desenvolvimento local/atividade acadêmica**, não um serviço público pronto para produção. Para publicar online, é preciso HTTPS, configuração de servidor de produção e outras medidas de segurança.
- **Importante:** foi preservada a organização e a classe `Application` do trecho fornecido, mas não foram recebidos os demais arquivos originais do BMVC do professor. Por isso, esta é uma implementação compatível com o código informado, não uma cópia verificada de uma versão específica do BMVC.

## Texto explicativo para a entrega

> Desenvolvi um sistema em Python com Bottle, estruturado em controllers, models e views, com dois recursos: portal e banco. O portal permite cadastrar usuários e realizar login por meio do modelo User_account. Após a autenticação, o usuário acessa a página `/banco`, onde é mostrada a lista de alunos cadastrados (READ). Cada aluno possui nome e idade. Implementei também as operações CREATE e DELETE por cURL no terminal Linux, além da opção de UPDATE. Os registros são armazenados em SQLite e o projeto contém instruções para instalação, execução e testes.
