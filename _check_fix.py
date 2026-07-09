"""Verifica problemas restantes no blog"""
import os
import glob

blog_dir = "repo_simulador/blog"
files = glob.glob(os.path.join(blog_dir, "*.html"))

issues_found = 0
for fp in sorted(files):
    name = os.path.basename(fp)
    with open(fp, 'rb') as f:
        raw = f.read()
    
    issues = []
    if b'Ola!' in raw: issues.append('Ola!-sem-acento')
    if b'\xf0\x9f\x93\x9d' in raw: issues.append('emoji-emoji-pencil-no-nav')
    if b'\xf0\x9f\x93\x8b' in raw: issues.append('emoji-clipboard-no-nav')
    if b'\xf0\x9f\x9b\x92' in raw: issues.append('emoji-cart-no-nav')
    if b'servicos da CoreGov' in raw: issues.append('servicos-sem-acento')
    if b'<i class="fas fa-bars">' in raw and b'<i class="fas fa-bars"></i>' not in raw: issues.append('menu-toggle-sem-fechar')
    
    if issues:
        print("[PROBLEMA] {}: {}".format(name, ', '.join(issues)))
        issues_found += 1
    else:
        print("[OK] {}".format(name))

print("\nTotal com problemas: {}".format(issues_found))
