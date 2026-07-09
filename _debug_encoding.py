"""Debug: check actual hex of mojibake chars in article body"""
with open('blog/captacao-de-recursos-para-ongs-guia-completo.html', 'rb') as f:
    raw = f.read()

# Find the article body
idx = raw.find(b'Principais fontes')
if idx >= 0:
    print("Found 'Principais fontes' at byte", idx)
    snippet = raw[idx:idx+400]
    print("\nHex:")
    for i, b in enumerate(snippet):
        if i % 25 == 0:
            print("\n{:06d}: ".format(idx + i), end='')
        print('{:02x}'.format(b), end=' ')
    print()
    
    text = snippet.decode('utf-8', errors='replace')
    print("\nAs text:", repr(text))
