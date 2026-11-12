<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ajuda cURL | Portal BMVC</title><link rel="stylesheet" href="/static/style.css"></head>
<body><main class="container"><div class="eyebrow">GUIA DE UTILIZAÇÃO</div><h1>Comandos cURL</h1><p>1. Crie um usuário pelo <a href="/registrar">portal</a>. 2. Faça login e salve o cookie. 3. Execute os comandos abaixo no terminal Linux.</p>
<pre><code>curl -i -c cookies.txt -d 'usuario=SEU_USUARIO' -d 'senha=SUA_SENHA' http://localhost:8080/login

curl -b cookies.txt http://localhost:8080/api/alunos

curl -b cookies.txt -X POST http://localhost:8080/api/alunos \
  -H 'Content-Type: application/json' -d '{"nome":"Ana","idade":19}'

curl -b cookies.txt -X DELETE http://localhost:8080/api/alunos/1</code></pre><p class="muted">Substitua o usuário, a senha e o ID pelos valores que você realmente utiliza. Para mais detalhes, leia o README do projeto.</p>
<p><a href="/">Voltar ao portal</a></p></main></body></html>
