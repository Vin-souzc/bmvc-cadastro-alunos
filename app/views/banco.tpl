<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Banco de alunos | Portal BMVC</title><link rel="stylesheet" href="/static/style.css"></head>
<body><main class="container"><header class="topbar"><div><div class="eyebrow">PORTAL · BANCO</div><h1>Cadastro de alunos</h1><p class="muted">Bem-vindo(a), <strong>{{usuario['usuario']}}</strong>. Somente usuários autenticados acessam esta página.</p></div>
<form method="post" action="/sair"><input type="hidden" name="csrf" value="{{csrf}}"><button type="submit" class="outline">Sair</button></form></header>
<div class="layout"><section class="panel"><h2>Novo aluno</h2><p class="muted">Crie um registro com dois atributos: nome e idade.</p>
% if erro:
<p class="error" role="alert">{{erro}}</p>
% end
<form method="post" action="/banco"><input type="hidden" name="csrf" value="{{csrf}}">
<label for="nome">Nome</label><input id="nome" name="nome" required minlength="2" maxlength="100" placeholder="Ex.: Maria Santos">
<label for="idade">Idade</label><input id="idade" name="idade" type="number" min="0" max="120" required placeholder="Ex.: 20">
<button type="submit">Cadastrar aluno</button></form></section>
<section class="panel"><div class="section-head"><h2>Alunos cadastrados</h2><span class="count">{{len(alunos)}} registro(s)</span></div>
% if alunos:
<div class="table-wrap"><table><thead><tr><th>ID</th><th>Nome</th><th>Idade</th><th>Ação</th></tr></thead><tbody>
% for aluno in alunos:
<tr><td>{{aluno['id']}}</td><td>{{aluno['nome']}}</td><td>{{aluno['idade']}}</td><td><form method="post" action="/banco/{{aluno['id']}}/excluir"><input type="hidden" name="csrf" value="{{csrf}}"><button class="danger" type="submit">Excluir</button></form></td></tr>
% end
</tbody></table></div>
% else:
<p class="empty">Nenhum aluno cadastrado. Use o formulário ou a API com cURL.</p>
% end
</section></div><p class="footnote">O recurso <code>/banco</code> realiza o READ na interface. A API <code>/api/alunos</code> permite operações com cURL. <a href="/helper">Ver exemplos</a>.</p>
</main></body></html>
