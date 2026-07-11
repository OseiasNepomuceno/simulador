#!/usr/bin/env python3
"""Corrige mojibake usando cp1252 (Windows) em vez de Latin-1"""
import re
import os

files = {
    'norte': 'produtos/calendario-norte.html',
    'sudeste': 'produtos/calendario-sudeste.html',
    'sul': 'produtos/calendario-sul.html',
}

for name, path in files.items():
    with open(path, 'rb') as f:
        raw = f.read()
    
    # Step 1: Read bytes as UTF-8 to get the mojibake string
    wrong_str = raw.decode('utf-8', errors='replace')
    
    # Step 2: Encode as cp1252 to get back the original raw bytes
    # cp1252 correctly maps bytes 0x80-0x9F to printable chars
    try:
        fixed_bytes = wrong_str.encode('cp1252')
    except UnicodeEncodeError as e:
        print(f'[ERROR] {path}: {e}')
        # Fallback: replace problematic chars
        fixed_bytes = wrong_str.encode('cp1252', errors='replace')
    
    # Step 3: Decode as UTF-8
    try:
        fixed_text = fixed_bytes.decode('utf-8')
    except UnicodeDecodeError:
        fixed_text = fixed_bytes.decode('utf-8', errors='replace')
    
    # Check if it improved
    title_before = re.search(r'<title>(.*?)</title>', wrong_str)
    title_after = re.search(r'<title>(.*?)</title>', fixed_text)
    
    if title_before and title_after:
        print(f'[{name.upper()}]')
        print(f'  Before: {title_before.group(1)[:70]}')
        print(f'  After:  {title_after.group(1)[:70]}')
    
    # Save if fixed
    with open(path, 'w', encoding='utf-8') as f:
        f.write(fixed_text)
    print(f'  → Saved ({len(raw)} → {len(fixed_bytes)} bytes)')
    print()
