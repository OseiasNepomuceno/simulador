# -*- coding: utf-8 -*-
import markdown

# Read the post
with open("post_lancamento_calendarios_01.md", "r", encoding="utf-8") as f:
    content = f.read()

# Split frontmatter (strategy section) from post body
parts = content.split("---", 2)
if len(parts) >= 3:
    header = parts[0].strip()
    body = parts[2].strip()
else:
    header = ""
    body = content

# Convert body to HTML
html_body = markdown.markdown(body, extensions=['extra'])

# Build full HTML
full_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Post COREGOV - Calendarios Regionais 2026</title>
<style>
    @page {{
        size: A4;
        margin: 0;
    }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
        font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
        background: #f0f2f5;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        padding: 20px;
    }}
    .card {{
        max-width: 595px;
        width: 100%;
        background: white;
        border-radius: 16px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.12);
        padding: 40px 36px;
        margin: 20px auto;
    }}
    /* LinkedIn-style header */
    .post-header {{
        display: flex;
        align-items: center;
        margin-bottom: 20px;
        padding-bottom: 16px;
        border-bottom: 1px solid #e0e0e0;
    }}
    .logo {{
        width: 52px;
        height: 52px;
        border-radius: 50%;
        background: linear-gradient(135deg, #0f3460, #e94560);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 22px;
        margin-right: 14px;
        flex-shrink: 0;
    }}
    .post-author h2 {{
        font-size: 16px;
        color: #0f3460;
        margin: 0;
    }}
    .post-author p {{
        font-size: 13px;
        color: #666;
        margin: 2px 0 0 0;
    }}
    /* Post content */
    .post-content {{
        font-size: 14.5px;
        line-height: 1.7;
        color: #1a1a1a;
    }}
    .post-content h1 {{
        font-size: 22px;
        color: #0f3460;
        margin: 20px 0 12px 0;
        line-height: 1.3;
    }}
    .post-content h2 {{
        font-size: 18px;
        color: #e94560;
        margin: 18px 0 10px 0;
    }}
    .post-content h3 {{
        font-size: 16px;
        color: #0f3460;
        margin: 14px 0 8px 0;
    }}
    .post-content p {{
        margin-bottom: 12px;
        text-align: left;
    }}
    .post-content ul {{
        margin: 10px 0 12px 24px;
    }}
    .post-content li {{
        margin-bottom: 6px;
        list-style: none;
    }}
    .post-content li::before {{
        content: "\\25B6";
        color: #e94560;
        margin-right: 8px;
        font-size: 11px;
    }}
    .post-content strong {{
        color: #0f3460;
    }}
    .post-content hr {{
        border: none;
        border-top: 2px solid #f0f2f5;
        margin: 20px 0;
    }}
    /* Regions box */
    .regions-box {{
        background: linear-gradient(135deg, #f8f9fc, #eef1f7);
        border-radius: 12px;
        padding: 18px 22px;
        margin: 16px 0;
        border-left: 4px solid #e94560;
    }}
    .regions-box p {{
        margin-bottom: 6px;
        font-size: 14px;
    }}
    .cta {{
        background: #0f3460;
        color: white;
        padding: 18px 22px;
        border-radius: 12px;
        margin: 20px 0;
        text-align: center;
        font-weight: bold;
        font-size: 15px;
    }}
    .hashtags {{
        margin-top: 20px;
        padding-top: 16px;
        border-top: 1px solid #e0e0e0;
        font-size: 13px;
        color: #0f3460;
    }}
    .footer-note {{
        margin-top: 24px;
        text-align: center;
        font-size: 11px;
        color: #999;
    }}
    @media print {{
        body {{ padding: 0; background: white; }}
        .card {{ box-shadow: none; margin: 0; border-radius: 0; padding: 30px; }}
    }}
</style>
</head>
<body>
<div class="card">
    <!-- LinkedIn-style header -->
    <div class="post-header">
        <div class="logo">C</div>
        <div class="post-author">
            <h2>COREGOV</h2>
            <p>Captacao de Recursos para ONGs • 28 anos de trajetoria</p>
        </div>
    </div>
    
    <!-- Post body -->
    <div class="post-content">
        {html_body}
    </div>
    
    <div class="footer-note">
        COREGOV • coregov.com.br
    </div>
</div>
</body>
</html>"""

with open("post_calendarios_01.html", "w", encoding="utf-8") as f:
    f.write(full_html)

print("OK - HTML do Post 01 gerado!")
print(f"Tamanho: {len(full_html)} bytes")
