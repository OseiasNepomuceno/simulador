import markdown
import re

# Read the markdown file
with open("01_curso_musica.md", "r", encoding="utf-8") as f:
    md_content = f.read()

# Convert markdown to HTML
html_body = markdown.markdown(md_content, extensions=['extra', 'toc'])

# Clean up excess whitespace
html_body = re.sub(r'\n{3,}', '\n\n', html_body)

# Full HTML with CSS styling for book-like appearance
full_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Curso de Iniciação Musical</title>
<style>
    @page {{
        size: A4;
        margin: 2.5cm 2cm 2.5cm 2cm;
    }}
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    body {{
        font-family: 'Georgia', 'Times New Roman', serif;
        font-size: 12pt;
        line-height: 1.6;
        color: #1a1a1a;
        max-width: 210mm;
        margin: 0 auto;
        padding: 20mm 15mm;
    }}
    /* Cover page */
    .cover-page {{
        text-align: center;
        padding: 80mm 20mm 40mm 20mm;
        page-break-after: always;
    }}
    .cover-page h1 {{
        font-size: 28pt;
        color: #1a3a5c;
        margin-bottom: 20pt;
        line-height: 1.3;
    }}
    .cover-page .subtitle {{
        font-size: 16pt;
        color: #555;
        margin-bottom: 40pt;
        font-style: italic;
    }}
    .cover-page .info {{
        font-size: 11pt;
        color: #777;
        margin-top: 60pt;
        line-height: 2;
    }}
    .cover-page .separator {{
        width: 60%;
        height: 3px;
        background: #1a3a5c;
        margin: 30pt auto;
    }}
    /* Typography */
    h1 {{
        font-size: 20pt;
        color: #1a3a5c;
        margin-top: 30pt;
        margin-bottom: 15pt;
        page-break-before: always;
        border-bottom: 2px solid #1a3a5c;
        padding-bottom: 8pt;
    }}
    h1:first-of-type {{
        page-break-before: auto;
    }}
    h2 {{
        font-size: 16pt;
        color: #2a5a8c;
        margin-top: 25pt;
        margin-bottom: 10pt;
    }}
    h3 {{
        font-size: 13pt;
        color: #3a6a9c;
        margin-top: 20pt;
        margin-bottom: 8pt;
    }}
    h4 {{
        font-size: 12pt;
        color: #4a7aac;
        margin-top: 15pt;
        margin-bottom: 6pt;
    }}
    p {{
        margin-bottom: 10pt;
        text-align: justify;
    }}
    ul, ol {{
        margin: 8pt 0 10pt 25pt;
    }}
    li {{
        margin-bottom: 4pt;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 15pt 0;
        font-size: 11pt;
    }}
    th {{
        background: #1a3a5c;
        color: white;
        padding: 8pt 10pt;
        text-align: left;
        font-weight: bold;
    }}
    td {{
        padding: 6pt 10pt;
        border: 1px solid #ccc;
    }}
    tr:nth-child(even) {{
        background: #f5f8fc;
    }}
    blockquote {{
        margin: 15pt 20pt;
        padding: 10pt 15pt;
        background: #f0f4f8;
        border-left: 4px solid #1a3a5c;
        font-style: italic;
    }}
    strong {{
        color: #1a3a5c;
    }}
    code {{
        font-family: 'Courier New', monospace;
        background: #f0f0f0;
        padding: 1pt 4pt;
        font-size: 11pt;
    }}
    hr {{
        border: none;
        border-top: 1px solid #ccc;
        margin: 20pt 0;
    }}
    /* Sumário / TOC */
    .toc {{
        margin: 20pt 0;
    }}
    .toc ul {{
        list-style: none;
        margin-left: 0;
    }}
    .toc li {{
        margin-bottom: 6pt;
        font-size: 12pt;
    }}
    .toc a {{
        color: #1a3a5c;
        text-decoration: none;
    }}
    .toc a:hover {{
        text-decoration: underline;
    }}
    /* Footer */
    .footer {{
        text-align: center;
        color: #999;
        font-size: 10pt;
        margin-top: 40pt;
        padding-top: 20pt;
        border-top: 1px solid #ddd;
    }}
    @media print {{
        body {{
            padding: 0;
        }}
        .cover-page {{
            padding-top: 100mm;
        }}
        h1 {{
            page-break-before: always;
        }}
        h1:first-of-type {{
            page-break-before: auto;
        }}
        h2 {{
            page-break-after: avoid;
        }}
    }}
</style>
</head>
<body>

<!-- COVER PAGE (generated from content) -->
<div class="cover-page">
    <h1>🎵 CURSO DE INICIAÇÃO MUSICAL<br>PARA ASSOCIAÇÕES COMUNITÁRIAS</h1>
    <div class="separator"></div>
    <p class="subtitle">Apostila do Aluno</p>
    <div class="info">
        <strong>Realização:</strong> [Nome da Associação]<br>
        <strong>Carga Horária:</strong> 40 horas<br>
        <strong>Público-Alvo:</strong> Jovens e adultos a partir de 12 anos<br>
        <strong>Ano:</strong> 2026
    </div>
</div>

{html_body}

<div class="footer">
    <p><em>Material produzido para uso gratuito em associações comunitárias. Distribuição livre e permitida.</em></p>
</div>

</body>
</html>"""

with open("01_curso_musica.html", "w", encoding="utf-8") as f:
    f.write(full_html)

print("OK - HTML gerado com sucesso!")
print(f"Tamanho: {len(full_html)} bytes")
