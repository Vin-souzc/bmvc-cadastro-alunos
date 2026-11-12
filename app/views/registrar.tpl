<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cadastro | Portal BMVC</title><link rel="stylesheet" href="/static/style.css"></head>
<body><main class="container narrow"><div class="eyebrow">PROJETO BMVC</div><h1>Criar usuário</h1><p class="muted">Cadastre-se para acessar a lista de alunos.</p>
% if erro:
<p class="error" role="alert">{{erro}}</p>
% end
<form method="post" action="/registrar" class="panel">
<label for="usuario">Usuário (3 a 32 caracteres)</label><input id="usuario" name="usuario" minlength="3" maxlength="32" required autocomplete="username">
<label for="senha">Senha (mínimo 8 caracteres)</label><input id="senha" name="senha" type="password" minlength="8" required autocomplete="new-password">
<button type="submit">Criar conta</button></form><p><a href="/login">Voltar ao login</a></p></main></body></html>
