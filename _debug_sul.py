#!/usr/bin/env python3
"""Debug sul file encoding"""
with open('produtos/calendario-sul.html', 'rb') as f:
    raw = f.read()
title_start = raw.find(b'<title>')
print(f'Title hex: {raw[title_start:title_start+60].hex()}')
text = raw.decode('utf-8', errors='replace')
print(f'Contains Ã¡: {"Ã¡" in text}')
print(f'Contains Calend: {"Calend" in text}')
idx = text.find('Calend')
if idx >= 0:
    print(f'Context: [{text[idx:idx+30]}]')
