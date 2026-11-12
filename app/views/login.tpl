<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Entrar | Portal BMVC</title><link rel="stylesheet" href="/static/style.css"></head>
<body><main class="container narrow"><div class="eyebrow">PROJETO BMVC</div><h1>Portal de alunos</h1><p class="muted">Acesse o banco de dados com sua conta.</p>
% if erro:
<p class="error" role="alert">{{erro}}</p>
% end
<form method="post" action="/login" class="panel">
<label for="usuario">Usuário</label><input id="usuario" name="usuario" maxlength="32" required autocomplete="username">
<label for="senha">Senha</label><input id="senha" name="senha" type="password" required autocomplete="current-password">
<button type="submit">Entrar</button></form><p>Primeiro acesso? <a href="/registrar">Criar usuário</a></p>
<p class="muted"><a href="/helper">Ver comandos cURL</a></p></main></body></html>
