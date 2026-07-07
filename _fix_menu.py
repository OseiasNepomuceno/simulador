# Add Blog link to nav menu
path = 'index.html'
content = open(path, 'r', encoding='utf-8').read()

old = '<a href="#contato">Contato</a>\n                <a href="editais/">'
new = '<a href="#contato">Contato</a>\n                <a href="blog/">📝 Blog</a>\n                <a href="editais/">'

if old in content:
    content = content.replace(old, new, 1)
    open(path, 'w', encoding='utf-8').write(content)
    print('OK - Blog link added to nav')
else:
    print('ERROR: old text not found')
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'contato' in line.lower():
            print(f'Line {i}: {repr(line)}')
        if 'editais' in line and '<a' in line:
            print(f'Line {i}: {repr(line)}')
