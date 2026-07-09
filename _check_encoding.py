"""Verifica problemas de encoding no conteudo dos artigos"""
import os
import glob

blog_dir = "repo_simulador/blog"
files = glob.glob(os.path.join(blog_dir, "*.html"))

# Try to detect encoding issues by looking for known bad byte sequences
# These bytes represent UTF-8 characters when read as Latin-1/CP-1252
bad_patterns = [
    (b'\xc3\x89', 'UTF8-E-accent'),   # This is actually correct UTF-8 for É
    (b'\xc3\x93', 'UTF8-O-accent'),   # This is actually correct UTF-8 for Ó
]

issues_found = 0
for fp in sorted(files):
    name = os.path.basename(fp)
    with open(fp, 'rb') as f:
        raw = f.read()
    
    # Check if file opens correctly in UTF-8
    try:
        text = raw.decode('utf-8')
        utf8_ok = True
    except UnicodeDecodeError:
        utf8_ok = False
    
    if not utf8_ok:
        print("[PROBLEMA-ENCODING] {}: Falha ao decodificar UTF-8".format(name))
        issues_found += 1
    else:
        # Check for mojibake patterns in the decoded text
        # Mojibake: "não" showing as "nÃ£o", "é" showing as "Ã©", etc.
        mojibake = []
        # Check for common mojibake sequences in decoded text
        for bad_seq in ['nÃ£o', 'Ã©', 'Ã£o', 'Ã§', 'Ãº', 'Ã¡', 'Ã³', 'PrestaÃ§Ã£o', 'ConvÃªnios', 'OrÃ§amento', 'Ã‰', 'Ã“']:
            if bad_seq in text:
                # Make sure it's not just part of a correct UTF-8 string
                mojibake.append(bad_seq)
        
        if mojibake:
            print("[PROBLEMA-MOJIBAKE] {}: {}".format(name, ', '.join(mojibake[:5])))
            issues_found += 1
        else:
            pass  # No issues

if issues_found == 0:
    print("Nenhum problema de encoding encontrado!")
else:
    print("\nTotal com problemas: {}".format(issues_found))
