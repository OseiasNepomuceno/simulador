#!/usr/bin/env python3
"""Fix mojibake at byte level in blog HTML files."""
import glob

BLOG_DIR = "blog"

# Byte-level replacements: wrong UTF-8 byte sequence -> correct UTF-8 byte sequence
# The file has â (c3 a2) + â‚¬ (e2 82 ac) + " (e2 80 9d) which is the mojibake for em dash
# The correct em dash — is e2 80 94
BYTE_FIXES = [
    # â€" -> — (em dash)
    (b'\xc3\xa2\xe2\x82\xac\xe2\x80\x9d', b'\xe2\x80\x94'),
    # â€¢ -> • (bullet)
    (b'\xc3\xa2\xe2\x82\xac\xe2\x80\xa2', b'\xe2\x80\xa2'),
    # â€“ -> – (en dash)  
    (b'\xc3\xa2\xe2\x82\xac\xe2\x80\x9c', b'\xe2\x80\x93'),
    # â€˜ -> ' (left single quote)
    (b'\xc3\xa2\xe2\x82\xac\xe2\x80\x98', b'\xe2\x80\x98'),
    # â€™ -> ' (right single quote)
    (b'\xc3\xa2\xe2\x82\xac\xe2\x84\xa2', b'\xe2\x80\x99'),
    # â€œ -> " (left double quote)
    (b'\xc3\xa2\xe2\x82\xac\xe2\x80\x9c', b'\xe2\x80\x9c'),
    # â€� -> " (right double quote)
    (b'\xc3\xa2\xe2\x82\xac\xe2\x80\x9d', b'\xe2\x80\x9d'),
    # â€¦ -> … (ellipsis)
    (b'\xc3\xa2\xe2\x82\xac\xe2\x80\xa6', b'\xe2\x80\xa6'),
]

def main():
    files = glob.glob(BLOG_DIR + "/*.html")
    fixed_count = 0
    
    for fp in sorted(files):
        name = fp.split('/')[-1].split('\\')[-1]
        with open(fp, 'rb') as f:
            raw = f.read()
        
        original = raw
        for wrong, correct in BYTE_FIXES:
            raw = raw.replace(wrong, correct)
        
        if raw != original:
            with open(fp, 'wb') as f:
                f.write(raw)
            print("[FIXED] {}".format(name))
            fixed_count += 1
        else:
            print("[OK] {}".format(name))
    
    print("\nTotal corrigidos: {}".format(fixed_count))

if __name__ == "__main__":
    main()
