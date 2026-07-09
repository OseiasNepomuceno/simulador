#!/usr/bin/env python3
"""Corrige encoding, erros de portugues e emojis no blog COREGOV"""
import os
import re
import glob

BLOG_DIR = os.path.join(os.path.dirname(__file__), "blog")

# Mapeamento de correcoes de encoding UTF-8 mal interpretado
ENCODING_FIXES = {
    # Em dash (â€” -> —)
    '\xe2\x80\x94': '\u2014',  # —
    # Acentos comuns (UTF-8 bytes lidos como Latin1)
    '\xc3\x81': '\u00c1',  # Á
    '\xc3\x89': '\u00c9',  # É
    '\xc3\x93': '\u00d3',  # Ó
    '\xc3\x94': '\u00d4',  # Ô
    '\xc3\x8d': '\u00cd',  # Í
    '\xc3\x9a': '\u00da',  # Ú
    '\xc3\xa1': '\u00e1',  # á
    '\xc3\xa9': '\u00e9',  # é
    '\xc3\xad': '\u00ed',  # í
    '\xc3\xb3': '\u00f3',  # ó
    '\xc3\xba': '\u00fa',  # ú
    '\xc3\xa3': '\u00e3',  # ã
    '\xc3\xb5': '\u00f5',  # õ
    '\xc3\xa7': '\u00e7',  # ç
    '\xc3\xaa': '\u00ea',  # ê
    '\xc3\xa0': '\u00e0',  # à
    '\xc3\xa2': '\u00e2',  # â
    '\xc3\xb4': '\u00f4',  # ô
    '\xc3\xbc': '\u00fc',  # ü
    '\xc3\x8a': '\u00ca',  # Ê
    '\xc3\x87': '\u00c7',  # Ç
    '\xc3\x83': '\u00c3',  # Ã
    '\xc3\x95': '\u00d5',  # Õ
    '\xc3\x82': '\u00c2',  # Â
}

# Correcoes de texto simples
TEXT_FIXES = {
    'Ola!%20Gostaria%20de%20saber%20mais%20sobre%20os%20servicos%20da%20CoreGov.': 'Ol%C3%A1!%20Gostaria%20de%20saber%20mais%20sobre%20os%20servi%C3%A7os%20da%20CoreGov.',
    'href="/blog/" class="active">📝 Blog': 'href="/blog/" class="active"><i class="fas fa-pencil-alt"></i> Blog',
    'href="/blog/">📝 Blog': 'href="/blog/"><i class="fas fa-pencil-alt"></i> Blog',
    'href="/editais/">📋 Editais': 'href="/editais/"><i class="fas fa-clipboard-list"></i> Editais',
    'href="/produtos/">🛒 Produtos': 'href="/produtos/"><i class="fas fa-shopping-cart"></i> Produtos',
    'href="blog/" class="active">📝 Blog': 'href="blog/" class="active"><i class="fas fa-pencil-alt"></i> Blog',
    'href="blog/">📝 Blog': 'href="blog/"><i class="fas fa-pencil-alt"></i> Blog',
    'href="editais/">📋 Editais': 'href="editais/"><i class="fas fa-clipboard-list"></i> Editais',
    'href="produtos/">🛒 Produtos': 'href="produtos/"><i class="fas fa-shopping-cart"></i> Produtos',
    'class="menu-toggle" id="menuToggle" aria-label="Abrir menu"><i class="fas fa-bars">': 'class="menu-toggle" id="menuToggle" aria-label="Abrir menu"><i class="fas fa-bars"></i>',
}

def fix_encoding(text):
    """Fixes encoding issues in text content."""
    for wrong, correct in ENCODING_FIXES.items():
        text = text.replace(wrong, correct)
    return text

def apply_text_fixes(text):
    """Applies simple text replacements."""
    for old, new in TEXT_FIXES.items():
        text = text.replace(old, new)
    return text

def fix_nav_emoji_line(line):
    """Fix emoji in nav links to use Font Awesome icons instead."""
    # Fix the menu-toggle missing closing tag
    line = line.replace(
        'class="menu-toggle" id="menuToggle" aria-label="Abrir menu"><i class="fas fa-bars">',
        'class="menu-toggle" id="menuToggle" aria-label="Abrir menu"><i class="fas fa-bars"></i>'
    )
    return line

def process_file(filepath):
    """Process a single HTML file."""
    with open(filepath, 'rb') as f:
        raw = f.read()
    
    # Try UTF-8 first
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        # Try Latin-1 as fallback
        text = raw.decode('latin-1')
    
    original = text
    
    # Fix encoding issues
    text = fix_encoding(text)
    
    # Fix text replacements
    text = apply_text_fixes(text)
    
    # Fix menu-toggle missing closing tag
    text = fix_nav_emoji_line(text)
    
    if text != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        return True
    return False

def main():
    """Main function."""
    # Get all HTML files in blog directory
    html_files = glob.glob(os.path.join(BLOG_DIR, "*.html"))
    html_files.sort()
    
    print(f"Encontrados {len(html_files)} arquivos HTML no blog")
    
    fixed_count = 0
    for filepath in html_files:
        filename = os.path.basename(filepath)
        if process_file(filepath):
            print(f"  [OK] {filename}")
            fixed_count += 1
        else:
            print(f"  [-] {filename} (sem alteracoes)")
    
    print(f"\nTotal: {fixed_count} arquivos corrigidos de {len(html_files)}")

if __name__ == "__main__":
    main()
