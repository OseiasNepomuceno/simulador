import sys
f = open('C:/Users/oseia/.picoclaw/workspace/repo_simulador/index.html', 'r', encoding='utf-8')
c = f.read()
f.close()

old = '                    <p>\n                        \U0001f50d <strong>Palavras-chave:</strong> Consultoria para ONGs | \n                        Captação de recursos federais | Transferegov | \n                        Arborização urbana | Agentes de IA | \n                        Automação de processos | Projetos para prefeituras\n                    </p>\n                </div>'

new = '                    <p>\n                        \U0001f50d <strong>Palavras-chave:</strong> Consultoria para ONGs | \n                        Captação de recursos federais | Transferegov | \n                        Arborização urbana | Agentes de IA | \n                        Automação de processos | Projetos para prefeituras\n                    </p>\n                    <p>\n                        \U0001f4d6 <strong>Novo artigo:</strong> <a href="blog/site-preparado-para-agentes-de-ia.html" style="color: var(--azul); text-decoration: underline;">Seu site está preparado para agentes de IA?</a> — \n                        O Google lançou o Agentic Browsing no Lighthouse. Entenda como preparar seu site para o futuro.\n                    </p>\n                </div>'

if old in c:
    c2 = c.replace(old, new, 1)
    f2 = open('C:/Users/oseia/.picoclaw/workspace/repo_simulador/index.html', 'w', encoding='utf-8')
    f2.write(c2)
    f2.close()
    print('SUCCESS: Replacement done!')
else:
    print('FAILED: old text not found')
    # Find the location
    idx = c.find('Palavras-chave')
    if idx >= 0:
        # Print the exact string around that area with repr
        start = max(0, idx - 80)
        end = min(len(c), idx + 280)
        snippet = c[start:end]
        # Write to debug file for inspection
        with open('C:/Users/oseia/.picoclaw/workspace/debug_match.txt', 'w', encoding='utf-8') as df:
            df.write(repr(snippet))
        print('Written to debug_match.txt')
