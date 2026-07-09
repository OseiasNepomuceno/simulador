import os
with open('repo_simulador/blog/captacao-de-recursos-para-ongs-guia-completo.html', 'r', encoding='utf-8') as f:
    content = f.read()

checks = ['Ola!', 'servicos da CoreGov', '\U0001f4dd', '\U0001f4cb', '\U0001f6d2']
for c in checks:
    if c in content:
        print('ENCONTRADO: ' + repr(c))
    else:
        print('OK: removido')

idx = content.find('Editais')
if idx >= 0:
    snippet = content[idx:idx+300]
    print('\nTrecho de exemplo:')
    print(snippet)

# Check nav links
if '<i class="fas fa-pencil-alt">' in content:
    print('\nNav link Blog: Font Awesome OK')
if '<i class="fas fa-clipboard-list">' in content:
    print('Nav link Editais: Font Awesome OK')
if '<i class="fas fa-shopping-cart">' in content:
    print('Nav link Produtos: Font Awesome OK')

# Check menu-toggle
if '<i class="fas fa-bars"></i>' in content:
    print('Menu toggle: fechamento OK')
