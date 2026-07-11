#!/usr/bin/env python3
"""Check encoding of calendar files"""
for fn in ['produtos/calendario-norte.html', 'produtos/calendario-sudeste.html', 'produtos/calendario-sul.html']:
    with open(fn, 'rb') as f:
        raw = f.read()
    idx = raw.find(b'<title>')
    title_bytes = raw[idx:idx+100]
    print(f'{fn}:')
    print(f'  Hex: {title_bytes.hex()}')
    print(f'  Raw text: {title_bytes}')
    print()
