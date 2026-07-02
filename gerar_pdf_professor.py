"""
ProfessorPRO - Conversor TXT para PDF com fonte Unicode (DejaVu Sans)
Suporta acentos, simbolos e caracteres especiais.
"""

import os, re, textwrap, json, sys
from pathlib import Path
from fpdf import FPDF

CORES = {
    "azul": (15, 52, 96),
    "vermelho": (233, 69, 96),
    "dourado": (245, 197, 24),
    "branco": (255, 255, 255),
    "cinza_claro": (240, 240, 240),
    "cinza": (180, 180, 180),
    "preto": (30, 30, 30),
    "verde": (0, 200, 100),
}

FONTE = "DejaVu"

class PDFprof(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)
        self.add_font(FONTE, "", "DejaVuSans.ttf", uni=True)
        self.add_font(FONTE, "B", "DejaVuSans.ttf", uni=True)
        self.add_font(FONTE, "I", "DejaVuSans.ttf", uni=True)

    def header(self):
        if self.page_no() > 1:
            self.set_font(FONTE, "I", 8)
            self.set_text_color(*CORES["cinza"])
            self.cell(0, 8, "ProfessorPRO - coregov.com.br/professorpro", align="C")
            self.ln(4)
            self.set_draw_color(*CORES["dourado"])
            self.set_line_width(0.3)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font(FONTE, "I", 8)
        self.set_text_color(*CORES["cinza"])
        self.cell(0, 10, f"Pagina {self.page_no()}/{{nb}}", align="C")


def criar_pdf(conteudo_txt, dados, caminho_saida):
    """Gera PDF bonito a partir do TXT."""
    
    pdf = PDFprof()
    pdf.alias_nb_pages()
    
    tema = dados.get("tema", "Material")
    serie = dados.get("serie", "")
    disciplina = dados.get("disciplina", "")
    
    # ============ CAPA ============
    pdf.add_page()
    pdf.set_fill_color(*CORES["azul"])
    pdf.rect(0, 0, 210, 297, "F")
    
    # Faixa dourada
    pdf.set_fill_color(*CORES["dourado"])
    pdf.rect(0, 85, 210, 3, "F")
    
    pdf.set_y(50)
    pdf.set_font(FONTE, "B", 36)
    pdf.set_text_color(*CORES["dourado"])
    pdf.cell(0, 20, "PROFESSORPRO", align="C", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font(FONTE, "", 16)
    pdf.set_text_color(*CORES["branco"])
    pdf.cell(0, 12, "Material Didatico com IA", align="C", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_fill_color(*CORES["dourado"])
    pdf.rect(0, 105, 210, 3, "F")
    
    # Tema
    pdf.set_y(125)
    pdf.set_font(FONTE, "B", 24)
    pdf.set_text_color(*CORES["branco"])
    for linha in textwrap.wrap(tema, width=30):
        pdf.cell(0, 14, linha, align="C", new_x="LMARGIN", new_y="NEXT")
    
    # Info
    pdf.set_y(175)
    pdf.set_font(FONTE, "", 13)
    pdf.set_text_color(*CORES["cinza"])
    pdf.cell(0, 10, f"Serie: {serie}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, f"Disciplina: {disciplina}", align="C", new_x="LMARGIN", new_y="NEXT")
    
    # Rodape da capa
    pdf.set_y(260)
    pdf.set_font(FONTE, "I", 10)
    pdf.cell(0, 8, "by COREGOV - coregov.com.br/professorpro", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "WhatsApp: (18) 9 9188-8698", align="C")
    
    # ============ CONTEUDO ============
    linhas = conteudo_txt.split("\n")
    
    for linha in linhas:
        s = linha.strip()
        if not s:
            pdf.ln(3)
            continue
        
        # Ignorar bordas e linhas decorativas
        if s.startswith(("╔", "╚", "╗", "╝")):
            continue
        if s.startswith(("─", "═")):
            pdf.set_draw_color(*CORES["dourado"])
            pdf.set_line_width(0.2)
            pdf.line(15, pdf.get_y(), 195, pdf.get_y())
            pdf.ln(4)
            continue
        
        # TITULOS (#)
        if s.startswith("# ") and not s.startswith("##"):
            pdf.ln(4)
            pdf.set_font(FONTE, "B", 16)
            pdf.set_text_color(*CORES["azul"])
            texto = s.replace("# ", "").strip()
            pdf.cell(0, 11, texto, new_x="LMARGIN", new_y="NEXT")
            pdf.set_draw_color(*CORES["dourado"])
            pdf.set_line_width(0.4)
            pdf.line(15, pdf.get_y(), 195, pdf.get_y())
            pdf.ln(4)
            continue
        
        # SUBTITULOS (##)
        if s.startswith("## "):
            pdf.ln(2)
            pdf.set_font(FONTE, "B", 13)
            pdf.set_text_color(*CORES["vermelho"])
            pdf.cell(0, 9, s.replace("## ", "").strip(), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
            continue
        
        # SUB-SUBTITULOS (###)
        if s.startswith("### "):
            pdf.ln(2)
            pdf.set_font(FONTE, "B", 11)
            pdf.set_text_color(*CORES["azul"])
            pdf.cell(0, 8, s.replace("### ", "").strip(), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
            continue
        
        # Tabelas com |
        if s.count("|") >= 2 and not "---" in s:
            colunas = [c.strip() for c in s.split("|") if c.strip()]
            if len(colunas) >= 2:
                eh_cabecalho = any(p in s for p in ["Tempo", "Atividade", "Ser", "Classif", "Resposta"])
                larg = min(170 // len(colunas), 50)
                pdf.set_font(FONTE, "B" if eh_cabecalho else "", 9)
                if eh_cabecalho:
                    pdf.set_fill_color(*CORES["azul"])
                    pdf.set_text_color(*CORES["branco"])
                else:
                    pdf.set_fill_color(*CORES["cinza_claro"])
                    pdf.set_text_color(*CORES["preto"])
                for col in colunas:
                    pdf.cell(larg, 7, col[:20], border=1, fill=True)
                pdf.ln()
                pdf.ln(2)
                continue
        
        # Texto comum
        pdf.set_font(FONTE, "", 10)
        pdf.set_text_color(*CORES["preto"])
        
        # Numeracao de questoes
        if re.match(r"^Questao\s*\d", s):
            pdf.set_font(FONTE, "B", 10)
            pdf.set_text_color(*CORES["vermelho"])
        
        # Opcoes a) b) c) d)
        if re.match(r"^[a-dA-D][\)\.]\s*\(", s):
            pdf.set_font(FONTE, "", 9)
            pdf.set_text_color(*CORES["preto"])
            pdf.set_x(25)
        
        # Gabarito
        if s.startswith("|") and "Q" in s:
            pdf.set_font(FONTE, "B", 9)
            pdf.set_text_color(*CORES["azul"])
        if s.startswith("|") and any(p in s for p in ["Q", "Resposta"]):
            pdf.set_font(FONTE, "B", 9)
            pdf.set_text_color(*CORES["azul"])
        
        pdf.multi_cell(0, 6, s)
        pdf.ln(1)
    
    pdf.output(str(caminho_saida))
    print(f"PDF GERADO: {caminho_saida}")
    return str(caminho_saida)


if __name__ == "__main__":
    base = Path(__file__).parent
    materiais = base / "materiais_gerados"
    
    # Usar o exemplo de Matematica
    txt_path = materiais / "exemplo_fracao_matematica.txt"
    
    if txt_path.exists():
        conteudo = txt_path.read_text(encoding="utf-8")
        dados = {"tema": "Fracao", "serie": "6o ano EF", "disciplina": "Matematica"}
        pdf_path = materiais / "exemplo_fracao_matematica.pdf"
        criar_pdf(conteudo, dados, pdf_path)
        print(f"Tamanho: {pdf_path.stat().st_size / 1024:.1f} KB")
    else:
        print(f"Arquivo nao encontrado: {txt_path}")
