#!/usr/bin/env python3
"""Corrige encoding mojibake nos calendarios Norte, Sudeste e Sul"""
import os

FILES = [
    "produtos/calendario-norte.html",
    "produtos/calendario-sudeste.html",
    "produtos/calendario-sul.html",
]

def fix_mojibake(text):
    """Fix mojibake: decode UTF-8 bytes that were stored as Latin-1 chars."""
    try:
        # Encode back to the original (corrupted) bytes, then decode properly
        return text.encode('latin-1', errors='replace').decode('utf-8', errors='replace')
    except Exception as e:
        print(f"  Erro no metodo principal: {e}")
        return text

def main():
    for fp in FILES:
        name = os.path.basename(fp)
        if not os.path.exists(fp):
            print(f"[NOT FOUND] {fp}")
            continue
        
        with open(fp, 'rb') as f:
            raw = f.read()
        
        try:
            text = raw.decode('utf-8')
        except UnicodeDecodeError:
            text = raw.decode('utf-8', errors='replace')
        
        original = text
        text = fix_mojibake(text)
        
        if text != original:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"[FIXED] {name} ({len(original)} -> {len(text)} chars)")
        else:
            print(f"[OK] {name} — sem alteracoes (ou nao foi possivel corrigir)")
        
        # Show a sample of the fix
        if text != original:
            print(f"  Antes: {original[100:250]}")
            print(f"  Depois: {text[100:250]}")

if __name__ == "__main__":
    main()
