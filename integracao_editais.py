#!/usr/bin/env python3
"""
🦞 Integração Editais → Revisor de Estatuto COREGOV
====================================================
Usado pelo Revisor de Estatuto PRÓ para incluir no
resultado da análise uma seção de oportunidades de captação.

Uso:
  from integracao_editais import gerar_secao_oportunidades
  secao = gerar_secao_oportunidades()
"""

import json
import os
from datetime import datetime
from pathlib import Path


# ══════════════════════════════════════════════════
# CAMINHOS
# ══════════════════════════════════════════════════

DIR_ATUAL = Path(__file__).parent
CAMINHO_JSON = DIR_ATUAL / "editais" / "dados_editais.json"


# ══════════════════════════════════════════════════
# CARREGAR DADOS
# ══════════════════════════════════════════════════

def carregar_editais():
    """Carrega o banco de editais do JSON."""
    if not CAMINHO_JSON.exists():
        return None
    try:
        with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


# ══════════════════════════════════════════════════
# GERAR SEÇÃO PARA O REVISOR DE ESTATUTO
# ══════════════════════════════════════════════════

def gerar_secao_oportunidades():
    """
    Gera um dicionário com a seção de oportunidades que será
    incluída no resultado da Análise de Estatuto.

    Retorna dict com:
      - editais_abertos: int
      - total_disponivel: str (ex: "R$ 584 milhões")
      - editais_proximos: list (5 editais com prazo mais curto)
      - mensagem_urgencia: str
      - html_bloco: str (pronto pra colar no resultado)
    """
    dados = carregar_editais()
    if not dados:
        return {
            "erro": True,
            "mensagem": "Banco de editais não encontrado. Execute 'raspar_editais.py' primeiro.",
            "html_bloco": "<p style='color:#e94560;'>⚠️ Dados de editais indisponíveis no momento.</p>"
        }

    resumo = dados.get("resumo_estrategico", {})
    editais = dados.get("editais", [])

    # Filtra apenas editais ABERTOS (não encerrados)
    abertos = [e for e in editais if e.get("prazo") != "encerrado" and
               e.get("status") != "encerrado"]

    # Ordena por prazo mais próximo (editais urgentes)
    def dias_prazo(e):
        d = e.get("dias_restantes")
        if d is None:
            return 999
        return d

    abertos.sort(key=dias_prazo)
    top5 = abertos[:5]

    # Monta HTML
    linhas = ""
    for e in top5:
        prazo = e.get("prazo", "Aberto")
        dias = e.get("dias_restantes")
        badge_urgencia = ""
        if dias is not None and dias <= 15:
            badge_urgencia = " 🔴 URGENTE"
        elif dias is not None and dias <= 30:
            badge_urgencia = " 🟡 ATENÇÃO"

        valor = e.get("valor_str", "Consultar")
        linhas += f"""
        <tr>
            <td style="padding:8px;border-bottom:1px solid #eee;">{e['titulo']}</td>
            <td style="padding:8px;border-bottom:1px solid #eee;text-align:center;">{valor}</td>
            <td style="padding:8px;border-bottom:1px solid #eee;text-align:center;">{prazo}{badge_urgencia}</td>
        </tr>"""

    editais_abertos = len(abertos)
    total_humano = resumo.get("soma_valores_humano", "R$ 0")

    html_bloco = f"""
    <div style="background:#fff9e6;border:2px solid #f5c518;border-radius:12px;padding:20px;margin:20px 0;">
        <h3 style="color:#0f3460;margin-top:0;">🔥 Oportunidades de Captação Disponível</h3>
        <p style="font-size:16px;">
            <strong style="color:#e94560;font-size:24px;">{editais_abertos} editais abertos</strong><br>
            <strong style="font-size:20px;">{total_humano} em recursos disponíveis</strong>
        </p>
        <p style="background:#e94560;color:white;padding:10px;border-radius:8px;text-align:center;font-weight:bold;font-size:15px;">
            ⚠️ Com o estatuto social inadequado, sua organização NÃO pode acessar esses recursos.
        </p>
        <p style="font-size:14px;color:#333;">
            Após a adequação do estatuto, sua ONG estará apta a concorrer a <strong>todos os {editais_abertos} editais</strong> listados abaixo.
        </p>
        <table style="width:100%;border-collapse:collapse;margin-top:15px;font-size:14px;">
            <thead>
                <tr style="background:#0f3460;color:white;">
                    <th style="padding:8px;text-align:left;">Edital</th>
                    <th style="padding:8px;text-align:center;">Valor</th>
                    <th style="padding:8px;text-align:center;">Prazo</th>
                </tr>
            </thead>
            <tbody>
                {linhas}
            </tbody>
        </table>
        <p style="margin-top:15px;font-size:13px;color:#666;font-style:italic;">
            Dados atualizados em {datetime.now().strftime('%d/%m/%Y às %H:%M')}.
            Fontes: capitaai.com.br, editalong.com, capta.org.br
        </p>
        <div style="text-align:center;margin-top:15px;">
            <a href="https://coregov.com.br/editais" target="_blank"
               style="display:inline-block;background:#e94560;color:white;padding:12px 25px;border-radius:8px;text-decoration:none;font-weight:bold;">
                📋 Ver todos os {editais_abertos} editais →
            </a>
        </div>
    </div>
    """

    return {
        "erro": False,
        "editais_abertos": editais_abertos,
        "total_disponivel": total_humano,
        "total_numerico": resumo.get("soma_valores_total", 0),
        "editais_para_ong": resumo.get("editais_para_ong", 0),
        "soma_valores_ong": resumo.get("soma_valores_ong_humano", "R$ 0"),
        "editais_urgentes": top5[:3],
        "mensagem_urgencia": resumo.get("mensagem_urgencia", ""),
        "mensagem_vendas": (
            f"Sua ONG está perdendo {editais_abertos} editais abertos "
            f"que somam {total_humano}. "
            f"Após a adequação do estatuto, você estará apto a captar "
            f"esses recursos AGORA."
        ),
        "html_bloco": html_bloco
    }


# ══════════════════════════════════════════════════
# TESTE RÁPIDO
# ══════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    resultado = gerar_secao_oportunidades()

    if resultado.get("erro"):
        print(f"❌ {resultado['mensagem']}")
        sys.exit(1)

    print("=" * 60)
    print("📊 SEÇÃO DE OPORTUNIDADES - REVISOR DE ESTATUTO")
    print("=" * 60)
    print(f"📋 Editais abertos:      {resultado['editais_abertos']}")
    print(f"💰 Total disponível:     {resultado['total_disponivel']}")
    print(f"🏛️  Para ONGs/OSCs:      {resultado['editais_para_ong']}")
    print(f"💰 Valor p/ ONGs:        {resultado['soma_valores_ong']}")
    print(f"\n📢 Mensagem de vendas:")
    print(f"   {resultado['mensagem_vendas']}")
    print(f"\n📝 HTML gerado: {len(resultado['html_bloco'])} caracteres")
    print(f"\n✅ Pronto para integrar ao Revisor de Estatuto!")
