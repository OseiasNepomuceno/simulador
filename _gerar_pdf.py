"""
Gera o PDF do exemplo de Matematica - Fracoes
Usa DejaVuSans.ttf para suporte a acentos
"""

from fpdf import FPDF
from pathlib import Path
import textwrap

base = Path(__file__).parent
txt_path = base / "materiais_gerados" / "exemplo_fracao_matematica.txt"
pdf_path = base / "materiais_gerados" / "exemplo_fracao_matematica.pdf"
fonte_path = base / "DejaVuSans.ttf"

CORES = {
    "azul": (15, 52, 96),
    "vermelho": (233, 69, 96),
    "dourado": (245, 197, 24),
    "branco": (255, 255, 255),
    "cinza": (180, 180, 180),
    "preto": (30, 30, 30),
}

F = "D"

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_font(F, "", str(fonte_path))
pdf.add_font(F, "B", str(fonte_path))
pdf.add_font(F, "I", str(fonte_path))
pdf.alias_nb_pages()

# Ler conteudo
conteudo = txt_path.read_text(encoding="utf-8")

# ===== CAPA =====
pdf.add_page()
pdf.set_fill_color(*CORES["azul"])
pdf.rect(0, 0, 210, 297, "F")
pdf.set_fill_color(*CORES["dourado"])
pdf.rect(0, 85, 210, 3, "F")

pdf.set_y(50)
pdf.set_font(F, "B", 36)
pdf.set_text_color(*CORES["dourado"])
pdf.cell(0, 20, "PROFESSORPRO", align="C", new_x="LMARGIN", new_y="NEXT")

pdf.set_font(F, "", 16)
pdf.set_text_color(*CORES["branco"])
pdf.cell(0, 12, "Material Didatico com IA", align="C", new_x="LMARGIN", new_y="NEXT")

pdf.set_fill_color(*CORES["dourado"])
pdf.rect(0, 105, 210, 3, "F")

pdf.set_y(125)
pdf.set_font(F, "B", 24)
pdf.set_text_color(*CORES["branco"])
for linha in textwrap.wrap("Fracao", width=30):
    pdf.cell(0, 14, linha, align="C", new_x="LMARGIN", new_y="NEXT")

pdf.set_y(175)
pdf.set_font(F, "", 13)
pdf.set_text_color(*CORES["cinza"])
pdf.cell(0, 10, "Serie: 6o ano EF", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 10, "Disciplina: Matematica", align="C", new_x="LMARGIN", new_y="NEXT")

pdf.set_y(260)
pdf.set_font(F, "I", 10)
pdf.set_text_color(*CORES["cinza"])
pdf.cell(0, 8, "by COREGOV - coregov.com.br/professorpro", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 8, "WhatsApp: (18) 9 9188-8698", align="C")

# ===== CONTEUDO =====
linhas = conteudo.split("\n")

for linha in linhas:
    s = linha.strip()
    if not s:
        pdf.ln(3)
        continue
    if s.startswith(("╔", "╚", "╗", "╝")):
        continue
    if s.startswith(("─", "═")):
        pdf.set_draw_color(*CORES["dourado"])
        pdf.set_line_width(0.2)
        pdf.line(15, pdf.get_y(), 195, pdf.get_y())
        pdf.ln(4)
        continue
    
    # Titulo principal
    if s.startswith("# ") and not s.startswith("##"):
        pdf.ln(4)
        pdf.set_font(F, "B", 16)
        pdf.set_text_color(*CORES["azul"])
        pdf.cell(0, 11, s.replace("# ", "").strip(), new_x="LMARGIN", new_y="NEXT")
        pdf.set_draw_color(*CORES["dourado"])
        pdf.set_line_width(0.4)
        pdf.line(15, pdf.get_y(), 195, pdf.get_y())
        pdf.ln(4)
        continue
    
    # Subtitulo
    if s.startswith("## "):
        pdf.ln(2)
        pdf.set_font(F, "B", 13)
        pdf.set_text_color(*CORES["vermelho"])
        pdf.cell(0, 9, s.replace("## ", "").strip(), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        continue
    
    if s.startswith("### "):
        pdf.ln(2)
        pdf.set_font(F, "B", 11)
        pdf.set_text_color(*CORES["azul"])
        pdf.cell(0, 8, s.replace("### ", "").strip(), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        continue
    
    # Tabelas
    if s.count("|") >= 2 and "---" not in s:
        cols = [c.strip() for c in s.split("|") if c.strip()]
        if len(cols) >= 2:
            eh_cab = any(p in s for p in ["Tempo", "Atividad", "Ser", "Classif", "Resposta", "Q "])
            largs = []
            total = 170
            if len(cols) == 3:
                largs = [22, 32, total - 22 - 32]
            elif len(cols) == 2:
                largs = [40, total - 40]
            else:
                largs = [total // len(cols)] * len(cols)
            # Limite de chars proporcional
            limites = [int(l / 5) for l in largs]  # ~5px por char na fonte 9
            pdf.set_font(F, "B" if eh_cab else "", 9)
            if eh_cab:
                pdf.set_fill_color(*CORES["azul"])
                pdf.set_text_color(*CORES["branco"])
            else:
                pdf.set_fill_color(240, 240, 240)
                pdf.set_text_color(*CORES["preto"])
            for i, col in enumerate(cols):
                cortado = col[:limites[i]] if len(col) > limites[i] else col
                pdf.cell(largs[i], 7, cortado, border=1, fill=True)
            pdf.ln()
            if not eh_cab:
                pdf.ln(2)
            continue
    
    # Texto
    pdf.set_font(F, "", 10)
    pdf.set_text_color(*CORES["preto"])
    if s.startswith("Questao") and any(c.isdigit() for c in s[:10]):
        pdf.set_font(F, "B", 10)
        pdf.set_text_color(*CORES["vermelho"])
    if s.startswith(("a)", "b)", "c)", "d)", "a.", "b.", "c.", "d.")):
        pdf.set_font(F, "", 9)
    if s.startswith("|") and "Q" in s:
        pdf.set_font(F, "B", 9)
        pdf.set_text_color(*CORES["azul"])
    
    try:
        pdf.multi_cell(0, 6, s)
    except:
        pdf.set_font(F, "", 8)
        try:
            pdf.multi_cell(0, 5, s)
        except:
            pass
    pdf.ln(1)

pdf.output(str(pdf_path))
print(f"PDF gerado: {pdf_path}")
print(f"Tamanho: {pdf_path.stat().st_size / 1024:.1f} KB")
