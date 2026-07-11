#!/usr/bin/env python3
"""Corrige mojibake usando cp1252 - sem Unicode no print"""
import re, os, sys

sys.stdout.reconfigure(errors='replace')

files = [
    'produtos/calendario-sudeste.html',
    'produtos/calendario-sul.html',
]

for path in files:
    with open(path, 'rb') as f:
        raw = f.read()
    
    wrong = raw.decode('utf-8', errors='replace')
    
    try:
        fixed_bytes = wrong.encode('cp1252')
    except UnicodeEncodeError:
        fixed_bytes = wrong.encode('cp1252', errors='replace')
    
    try:
        fixed = fixed_bytes.decode('utf-8')
    except UnicodeDecodeError:
        fixed = fixed_bytes.decode('utf-8', errors='replace')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(fixed)
    
    m = re.search(r'<title>(.*?)</title>', fixed)
    title = m.group(1)[:70] if m else '?'
    print(f'[OK] {path}')
    print(f'  Title: {title}')
    print()
