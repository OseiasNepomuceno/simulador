#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
sys.stdout.reconfigure(encoding='utf-8')

# Absolute path
base = r"C:\Users\oseia\.picoclaw\workspace"
path = os.path.join(base, "repo_simulador", "vagas", "index.html")

with open(path, "r", encoding="utf-8") as f:
    html = f.read()

# Fix plan buttons - single line format
replacements = [
    ('<a href="https://mpago.la/2UmiPMV" target="_blank" class="btn-plano btn-prata" onclick="event.stopPropagation();">\U0001f949 Assinar Bronze</a>',
     '<a href="#" class="btn-plano btn-prata" onclick="event.preventDefault();abrirModalEmail(\'bronze\')">\U0001f949 Assinar Bronze</a>'),
    ('<a href="https://mpago.la/1XWEeC6" target="_blank" class="btn-plano btn-prata" onclick="event.stopPropagation();">\U0001f3af Assinar Prata</a>',
     '<a href="#" class="btn-plano btn-prata" onclick="event.preventDefault();abrirModalEmail(\'prata\')">\U0001f3af Assinar Prata</a>'),
    ('<a href="https://mpago.la/2mSYs6U" target="_blank" class="btn-plano btn-ouro" onclick="event.stopPropagation();">\U0001f48e Assinar Ouro</a>',
     '<a href="#" class="btn-plano btn-ouro" onclick="event.preventDefault();abrirModalEmail(\'ouro\')">\U0001f48e Assinar Ouro</a>'),
    ('<a href="https://mpago.la/2fCg4C2" target="_blank" class="btn-plano btn-diamante" onclick="event.stopPropagation();">\U0001f451 Assinar Diamante</a>',
     '<a href="#" class="btn-plano btn-diamante" onclick="event.preventDefault();abrirModalEmail(\'diamante\')">\U0001f451 Assinar Diamante</a>'),
]

count = 0
for old, new in replacements:
    if old in html:
        html = html.replace(old, new)
        count += 1
        print(f"  Replaced: {new[:60]}...")

print(f"\nTotal replacements: {count}")
print(f"abrirModalEmail count: {html.count('abrirModalEmail')}")
print(f"mpago.la left: {html.count('mpago.la')}")

with open(path, "w", encoding="utf-8") as f:
    f.write(html)
print("Done!")
