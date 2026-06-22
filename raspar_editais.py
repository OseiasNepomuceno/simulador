#!/usr/bin/env python3
"""
🦞 Raspador de Editais COREGOV
==============================
Raspa editais de 3 fontes gratuitas e gera JSON para
usar na Análise de Estatuto e outros produtos COREGOV.

Fontes:
  1. capitaai.com.br   → Principal (mais completo)
  2. editalong.com     → HTML simples, backup
  3. capta.org.br      → Descrições detalhadas

Uso:
  python raspar_editais.py                    → gera editais.json
  python raspar_editais.py --json-pretty      → identado
  python raspar_editais.py --only-count       → só contagem
"""

import json
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime
from html.parser import HTMLParser

# ──────────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────────
TIMEOUT = 15
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) PicoClaw-COREGOV/1.0"

def fetch(url):
    """Baixa HTML de uma URL."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  ⚠️  Erro ao acessar {url}: {e}", file=sys.stderr)
        return ""


# ══════════════════════════════════════════════════
# FONTE 1: capitaai.com.br
# ══════════════════════════════════════════════════

def raspar_capitaai():
    """Raspa página inicial do capitaai.com.br."""
    html = fetch("https://capitaai.com.br")
    if not html:
        return []

    editais = []
    blocos = re.split(r'(?=🌱 ONGs|🔬 Pesquisadores|🎓 Universidades|🚀 Startups|🏛️ Prefeituras|🤝 Assoc|✊ Coletivos|🏢 Institutos|🏥 Hospitais|🏫 Escolas|🎨 Pessoa)', html)

    for bloco in blocos:
        # Tipo de organização
        tipo_match = re.search(r'([🌱🔬🎓🚀🏛️🤝✊🏢🏥🏫🎨])\s*(.+?)(?:\n|$)', bloco)
        tipo = tipo_match.group(2).strip() if tipo_match else "Geral"

        # Editais individuais neste bloco
        # Cada edital começa com o nome e termina em valor
        items = re.findall(
            r'(?:^|\n)\s*([^\n]+?)\s*\n'                         # Nome do edital
            r'.*?CERVEJARIA|FAPEMIG|FINEP|CEMIG|Facepe|Fundo Casa|Itaú Social|Zayed|CNPq|CAPES|Prefeitura|Companhia|Instituto|Fundação|Secretaria'
            r'.*?\n'                                               # Fonte
            r'.*?Valor disponível\s*R\$\s*([\d.,]+\s*(?:mil|mi[llhão]*|bilhão)?)',
            bloco, re.DOTALL
        )

        # Segundo padrão: mais genérico
        items2 = re.findall(
            r'([A-Z][A-Za-zÀ-ü0-9\s\-–—,!?]+?)\s*\n'             # Título
            r'(.*?)\n'                                             # Fonte/descrição
            r'Valor disponível\s*R\$\s*([\d.,]+\s*(?:mil|milhão|milhões|bi|bilhão)?)',
            bloco
        )

        for item in items2:
            titulo = item[0].strip()
            valor_str = item[2].strip()
            valor_numerico = converter_valor(valor_str)

            editais.append({
                "fonte": "capitaai.com.br",
                "titulo": titulo,
                "valor_str": f"R$ {valor_str}",
                "valor_numerico": valor_numerico,
                "tipo_organizacao": tipo,
                "categoria": extrair_categoria(titulo),
                "data_coleta": datetime.now().isoformat()
            })

    return editais


# ══════════════════════════════════════════════════
# FONTE 2: editalong.com/editais
# ══════════════════════════════════════════════════

def raspar_editalong():
    """Raspa editalong.com/editais."""
    html = fetch("https://www.editalong.com/editais")
    if not html:
        return []

    editais = []
    # Padrão: título + valor + prazo
    # Ex: "Instituto Neoenergia — Programa de Editais 2025-2026 ... Variável"
    #     "Fundo Brasil DH — Edital Geral 2026 ... R$ 1.000.000,00"

    blocos = re.split(r'(?=\d+[d]\s+restantes|encerrado)', html)

    for bloco in blocos:
        # Título (até quebra de linha ou traço)
        titulo_match = re.search(r'([A-Z][A-Za-zÀ-ü0-9\s\-–—]+?)', bloco)
        titulo = titulo_match.group(1).strip() if titulo_match else "Sem título"

        # Valor
        valor_match = re.search(r'R\$\s*([\d.]+\s*[\d.,]*)', bloco)
        valor_str = f"R$ {valor_match.group(1)}" if valor_match else "Variável"
        valor_numerico = converter_valor(valor_match.group(1)) if valor_match else 0

        # Prazo
        prazo_match = re.search(r'(\d+)[d]\s+restantes', bloco)
        prazo_dias = int(prazo_match.group(1)) if prazo_match else None

        # Status
        status = "encerrado" if "encerrado" in bloco.lower() else "aberto"

        if status == "aberto" and titulo not in ["Editais para ONGs Abertos", "Editais"]:
            editais.append({
                "fonte": "editalong.com",
                "titulo": titulo,
                "valor_str": valor_str,
                "valor_numerico": valor_numerico,
                "prazo_dias": prazo_dias,
                "status": status,
                "data_coleta": datetime.now().isoformat()
            })

    return editais


# ══════════════════════════════════════════════════
# FONTE 3: capta.org.br
# ══════════════════════════════════════════════════

def raspar_capta():
    """Raspa capta.org.br/fontes-de-financiamento/oportunidades/"""
    html = fetch("https://capta.org.br/fontes-de-financiamento/oportunidades/")
    if not html:
        return []

    editais = []
    # Cada edital é separado por data
    blocos = re.split(r'\d{2}/\d{2}/\d{4}--\u003e', html)

    for bloco in blocos[1:]:  # Pula cabeçalho
        titulo_match = re.search(r'([A-Z][A-Za-zÀ-ü0-9\s\-–,—!?]+)', bloco)
        titulo = titulo_match.group(1).strip() if titulo_match else "Sem título"

        # Valor
        valor_match = re.search(r'(?:entre\s*)?R\$\s*([\d.]+\s*[\d.,]*(?:\s*(?:mil|milhão|milhões|bi|bilhão))?)', bloco)
        valor_str = f"R$ {valor_match.group(1)}" if valor_match else "Consultar edital"
        valor_numerico = converter_valor(valor_match.group(1)) if valor_match else 0

        # Região
        regiao_match = re.search(r'Região:\s*(.+?)(?:\n|$)', bloco)
        regiao = regiao_match.group(1).strip() if regiao_match else "Nacional"

        # Prazo
        prazo_match = re.search(r'Inscrições até:\s*(\d{2}/\d{2}/\d{4})', bloco)
        prazo = prazo_match.group(1) if prazo_match else None

        # Área de atuação
        areas = []
        for area in ["educação", "cultura", "saúde", "meio ambiente", "esporte",
                       "geração de renda", "assistência social", "direitos humanos",
                       "juventude", "mulheres", "inclusão", "sustentabilidade"]:
            if area in bloco.lower():
                areas.append(area.title())

        if len(titulo) > 10 and "Editais" not in titulo and "Oportunidades" not in titulo:
            editais.append({
                "fonte": "capta.org.br",
                "titulo": titulo,
                "valor_str": valor_str,
                "valor_numerico": valor_numerico,
                "regiao": regiao,
                "prazo": prazo,
                "areas_atuacao": areas,
                "data_coleta": datetime.now().isoformat()
            })

    return editais


# ══════════════════════════════════════════════════
# UTILITÁRIOS
# ══════════════════════════════════════════════════

def converter_valor(valor_str):
    """Converte string '67 milhões', '1.000.000,00' para float."""
    if not valor_str:
        return 0.0
    valor_str = valor_str.strip().lower()

    multiplicador = 1
    if "bilhão" in valor_str or "bilhões" in valor_str or "bi" in valor_str:
        multiplicador = 1_000_000_000
    elif "milhão" in valor_str or "milhões" in valor_str or "mi" in valor_str:
        multiplicador = 1_000_000
    elif "mil" in valor_str:
        multiplicador = 1_000

    # Limpa o número
    numero = re.sub(r'[^0-9.,]', '', valor_str)
    numero = numero.replace('.', '').replace(',', '.') if multiplicador > 1 else numero.replace(',', '.')

    try:
        return float(numero) * multiplicador
    except ValueError:
        return 0.0


def extrair_categoria(titulo):
    """Tenta extrair categoria do título do edital."""
    categorias = {
        "educação": ["educação", "escola", "universidade", "bolsa", "científico", "pesquisa"],
        "cultura": ["cultura", "arte", "patrimônio", "museu", "music"],
        "saúde": ["saúde", "hospital", "filantropia"],
        "meio ambiente": ["ambiental", "sustentável", "clima", "energia", "socioambiental"],
        "social": ["social", "comunitário", "assistência", "direitos humanos"],
        "empreendedorismo": ["startup", "inovação", "empreendedor", "negócio"],
    }
    titulo_lower = titulo.lower()
    for cat, keywords in categorias.items():
        if any(kw in titulo_lower for kw in keywords):
            return cat
    return "geral"


# ══════════════════════════════════════════════════
# RESUMO E RELATÓRIO
# ══════════════════════════════════════════════════

def gerar_resumo(editais):
    """Gera resumo estratégico dos editais."""
    abertos = [e for e in editais if e.get("status") != "encerrado"]
    total = len(editais)
    soma_valores = sum(e.get("valor_numerico", 0) for e in editais if e.get("valor_numerico"))

    # Filtra só de ONGs/OSCs
    ong_keywords = ["ong", "osc", "social", "comunitário", "terceiro setor",
                    "associação", "fundação", "instituto", "filantropia"]
    editais_ong = [e for e in editais if any(kw in e.get("titulo", "").lower() or
                   kw in e.get("tipo_organizacao", "").lower() for kw in ong_keywords)]
    soma_ong = sum(e.get("valor_numerico", 0) for e in editais_ong if e.get("valor_numerico"))

    return {
        "total_editais": total,
        "editais_abertos": len(abertos),
        "soma_valores_total": soma_valores,
        "soma_valores_humano": formatar_valor(soma_valores),
        "editais_para_ong": len(editais_ong),
        "soma_valores_ong": soma_ong,
        "soma_valores_ong_humano": formatar_valor(soma_ong),
        "fontes_monitoradas": 3,
        "data_atualizacao": datetime.now().isoformat(),
        "mensagem_urgencia": (
            f"🔥 Existem {total} editais ativos hoje com mais de "
            f"{formatar_valor(soma_valores)} disponíveis. "
            f"Desses, {len(editais_ong)} são diretamente para ONGs/OSCs, "
            f"totalizando {formatar_valor(soma_ong)}. "
            f"Sua organização pode estar perdendo essas oportunidades."
        )
    }


def formatar_valor(valor):
    """Formata valor numérico para exibição."""
    if valor >= 1_000_000_000:
        return f"R$ {valor/1_000_000_000:.1f} bilhão"
    elif valor >= 1_000_000:
        return f"R$ {valor/1_000_000:.1f} milhões"
    elif valor >= 1_000:
        return f"R$ {valor/1_000:.0f} mil"
    else:
        return f"R$ {valor:.0f}"


# ══════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════

def main():
    print("🦞 Raspador de Editais COREGOV")
    print("=" * 45)
    print(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")

    # Raspar todas as fontes
    todos_editais = []

    print("📡 [1/3] capitaai.com.br...")
    e1 = raspar_capitaai()
    print(f"   → {len(e1)} editais encontrados")
    todos_editais.extend(e1)

    print("📡 [2/3] editalong.com...")
    e2 = raspar_editalong()
    print(f"   → {len(e2)} editais encontrados")
    todos_editais.extend(e2)

    print("📡 [3/3] capta.org.br...")
    e3 = raspar_capta()
    print(f"   → {len(e3)} editais encontrados")
    todos_editais.extend(e3)

    # Gerar resumo
    resumo = gerar_resumo(todos_editais)

    print(f"\n{'=' * 45}")
    print(f"📊 RESUMO ESTRATÉGICO")
    print(f"{'=' * 45}")
    print(f"📋 Total de editais:      {resumo['total_editais']}")
    print(f"✅ Editais abertos:       {resumo['editais_abertos']}")
    print(f"💰 Total disponível:      {resumo['soma_valores_humano']}")
    print(f"🏛️  Editais p/ ONGs:      {resumo['editais_para_ong']}")
    print(f"💰 Valor p/ ONGs:         {resumo['soma_valores_ong_humano']}")
    print(f"\n{resumo['mensagem_urgencia']}")

    # Preparar saída
    saida = {
        "metadata": {
            "versao": "1.0",
            "data_coleta": datetime.now().isoformat(),
            "fontes": ["capitaai.com.br", "editalong.com", "capta.org.br"],
            "total_editais": len(todos_editais)
        },
        "resumo_estrategico": resumo,
        "editais": todos_editais
    }

    # Salvar JSON
    indent = 2 if "--json-pretty" in sys.argv else None
    caminho = "editais/dados_editais.json"

    import os
    os.makedirs("editais", exist_ok=True)

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(saida, f, ensure_ascii=False, indent=indent)

    print(f"\n💾 Salvo em: {caminho}")

    # Modo only-count
    if "--only-count" in sys.argv:
        print(f"\n🔢 Apenas contagem solicitada:")
        print(f"   Total: {resumo['total_editais']}")
        print(f"   Abertos: {resumo['editais_abertos']}")
        print(f"   Soma: {resumo['soma_valores_humano']}")
        return

    print("\n✅ Coleta concluída!")


if __name__ == "__main__":
    main()
