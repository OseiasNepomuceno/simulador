#!/usr/bin/env python3
"""Corrige encoding mojibake nos artigos do blog COREGOV"""
import os
import glob

BLOG_DIR = "repo_simulador/blog"

# Mapa de correcao: sequencias de caracteres mojibake -> caractere correto
# Quando texto UTF-8 e lido como Latin-1/CP-1252, os bytes viram chars errados
MOJIBAKE_FIXES = {
    # Em dash — (UTF-8: E2 80 94) lido como Latin1
    '\u00e2\u20ac\u201c': '\u2014',  # â€“ -> — (en dash, U+2013)
    '\u00e2\u20ac\u201d': '\u2014',  # â€" -> — (em dash, U+2014) 
    '\u00e2\u20ac\u2122': '\u2019',  # â€™ -> ' (right single quote)
    '\u00e2\u20ac\u02dc': '\u2018',  # â€˜ -> ' (left single quote)
    '\u00e2\u20ac\u0153': '\u201c',  # â€œ -> " (left double quote)
    '\u00e2\u20ac\u009d': '\u201d',  # â€� -> " (right double quote)
    '\u00e2\u20ac\u00a6': '\u2026',  # â€¦ -> … (ellipsis)
    '\u00c3\u0081': '\u00c1',  # Ã� -> Á
    '\u00c3\u0089': '\u00c9',  # Ã‰ -> É
    '\u00c3\u0093': '\u00d3',  # Ã“ -> Ó
    '\u00c3\u0094': '\u00d4',  # Ã” -> Ô
    '\u00c3\u008d': '\u00cd',  # Ã� -> Í
    '\u00c3\u009a': '\u00da',  # Ãš -> Ú
    '\u00c3\u00a1': '\u00e1',  # Ã¡ -> á
    '\u00c3\u00a9': '\u00e9',  # Ã© -> é
    '\u00c3\u00ad': '\u00ed',  # Ã­ -> í
    '\u00c3\u00b3': '\u00f3',  # Ã³ -> ó
    '\u00c3\u00ba': '\u00fa',  # Ãº -> ú
    '\u00c3\u00a3': '\u00e3',  # Ã£ -> ã
    '\u00c3\u00b5': '\u00f5',  # Ãµ -> õ
    '\u00c3\u00a7': '\u00e7',  # Ã§ -> ç
    '\u00c3\u00aa': '\u00ea',  # Ãª -> ê
    '\u00c3\u00a0': '\u00e0',  # Ã -> à
    '\u00c3\u00a2': '\u00e2',  # Ã¢ -> â
    '\u00c3\u00b4': '\u00f4',  # Ã´ -> ô
    '\u00c3\u00bc': '\u00fc',  # Ã¼ -> ü
    '\u00c3\u008a': '\u00ca',  # ÃŠ -> Ê
    '\u00c3\u0087': '\u00c7',  # Ã‡ -> Ç
    '\u00c3\u0083': '\u00c3',  # Ãƒ -> Ã
    '\u00c3\u0095': '\u00d5',  # Ã• -> Õ
    '\u00c3\u0082': '\u00c2',  # Ã‚ -> Â
}

def fix_mojibake(text):
    """Fix mojibake (wrongly decoded UTF-8 as Latin-1)."""
    for wrong, correct in MOJIBAKE_FIXES.items():
        if wrong in text:
            text = text.replace(wrong, correct)
    return text

def main():
    files = glob.glob(os.path.join(BLOG_DIR, "*.html"))
    fixed_count = 0
    
    for fp in sorted(files):
        name = os.path.basename(fp)
        
        with open(fp, 'rb') as f:
            raw = f.read()
        
        # Decode as UTF-8
        try:
            text = raw.decode('utf-8')
        except UnicodeDecodeError:
            text = raw.decode('utf-8', errors='replace')
        
        original = text
        
        # Fix mojibake
        text = fix_mojibake(text)
        
        if text != original:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(text)
            print("[FIXED] {}".format(name))
            fixed_count += 1
        else:
            print("[OK] {}".format(name))
    
    print("\nTotal corrigidos: {}".format(fixed_count))

if __name__ == "__main__":
    main()
