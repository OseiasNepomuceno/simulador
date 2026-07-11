#!/usr/bin/env python3
"""Corrige mojibake usando cp1252 - versão robusta"""
import re, os, sys

files = [
    'produtos/calendario-norte.html',
    'produtos/calendario-sudeste.html',
    'produtos/calendario-sul.html',
]

for path in files:
    if not os.path.exists(path):
        print(f'[NOT FOUND] {path}')
        continue
    
    with open(path, 'rb') as f:
        raw = f.read()
    
    # Decode as UTF-8
    wrong = raw.decode('utf-8', errors='replace')
    
    # Check if there's mojibake
    has_mojibake = 'Ã¡' in wrong or 'Ã£' in wrong or 'Ã©' in wrong or 'Ã³' in wrong or 'Ãº' in wrong
    
    if not has_mojibake and 'Calendário' in wrong:
        print(f'[OK] {path} - no mojibake detected')
        continue
    
    # Try cp1252 roundtrip
    try:
        fixed_bytes = wrong.encode('cp1252')
        fixed = fixed_bytes.decode('utf-8')
        print(f'[FIXED] {path} - cp1252 roundtrip')
    except (UnicodeEncodeError, UnicodeDecodeError) as e:
        print(f'[FAIL] {path} - {e}')
        # Try byte-by-byte approach
        fixed_bytes = bytearray()
        for ch in wrong:
            code = ord(ch)
            if code < 0x80:
                fixed_bytes.append(code)
            elif code < 0x100:
                fixed_bytes.append(code)
            elif code in range(0x2018, 0x201D):
                # Smart quotes: map to cp1252
                fixed_bytes.append({0x2018: 0x91, 0x2019: 0x92, 0x201C: 0x93, 0x201D: 0x94}[code])
            elif code == 0x2026:
                fixed_bytes.append(0x85)  # ellipsis
            elif code == 0x0178:
                fixed_bytes.append(0x9F)  # Ÿ
            elif code == 0x20AC:
                fixed_bytes.append(0x80)  # €
            else:
                fixed_bytes.append(ord('?'))
        try:
            fixed = fixed_bytes.decode('utf-8')
            print(f'[FIXED] {path} - byte-by-byte fallback')
        except:
            print(f'[FAIL] {path} - could not decode after byte fix')
            continue
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(fixed)
    
    # Show result
    m = re.search(r'<title>(.*?)</title>', fixed)
    if m:
        print(f'  Title: {m.group(1)[:70]}')
    print()
