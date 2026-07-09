#!/usr/bin/env python3
"""
[MONITOR] Monitor de Licitações PNCP — COREGOV
========================================
Monitora o Portal Nacional de Contratações Públicas (PNCP)
em busca de licitações para serviços de:
  - Captação de recursos
  - Assessoria para ONGs/OSCs
  - Elaboração de planos municipais
  - Consultoria para terceiro setor
  - Projetos socioambientais

Uso:
  python monitorar_pncp.py              → busca única
  python monitorar_pncp.py --watch      → modo contínuo (a cada 6h)
  python monitorar_pncp.py --only-count → só contagem

Agendamento (cron):
  0 */6 * * * cd /caminho && python monitorar_pncp.py --quiet
"""

import json
import os
import re
import sys
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, timedelta

# ──────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────
TIMEOUT = 20
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) COREGOV-Monitor/1.0"
ARQUIVO_ALERTAS = "monitor_pncp_alertas.json"
ARQUIVO_HISTORICO = "monitor_pncp_historico.json"

# Palavras-chave para buscar
PALAVRAS_CHAVE = [
    "captação de recursos",
    "assessoria captação",
    "captação internacional",
    "elaboração de projetos sociais",
    "consultoria terceiro setor",
    "plano municipal arborização",
    "plano de arborização",
    "assessoria ONG",
    "estatuto social",
    "adequação estatuto",
    "elaboração estatuto",
    "projetos socioambientais",
    "consultoria OS",
    "captação recursos não reembolsáveis",
    "diálogo competitivo captação",
    "geração de emprego e renda",
    "desenvolvimento sustentável",
    "assessoria organizações sociais",
    "consultoria projetos sociais",
    "fomento projetos sociais",
]

# Palavras para EXCLUIR (falsos positivos)
EXCLUIR = [
    "material de construção",
    "medicamento",
    "equipamento hospitalar",
    "peça de veículo",
    "alimentação escolar",
    "combustível",
    "serviço de limpeza",
    "vigilância",
    "locação de veículo",
    "passagem aérea",
    "gênero alimentício",
    "pneu",
    "material de expediente",
]


# ──────────────────────────────────────────────
# FUNÇÕES
# ──────────────────────────────────────────────

def fetch(url):
    """Baixa conteúdo de URL."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  [AVISO]  Erro: {e}", file=sys.stderr)
        return ""


def buscar_no_pncp(palavra):
    """Busca uma palavra-chave no PNCP via web scraping."""
    palavra_encoded = urllib.parse.quote(palavra)
    url = f"https://pncp.gov.br/app/editais?q={palavra_encoded}&status=todos&pagina=1"
    html = fetch(url)
    return html, url


def buscar_duckduckgo(query):
    """Fallback: busca no DuckDuckGo Lite."""
    query_encoded = urllib.parse.quote(f"site:pncp.gov.br {query}")
    url = f"https://lite.duckduckgo.com/lite/?q={query_encoded}"
    html = fetch(url)
    # Extrair resultados do HTML simplificado
    resultados = []
    if html:
        # DuckDuckGo Lite retorna resultados em linhas numeradas
        linhas = html.split("\n")
        i = 0
        while i < len(linhas):
            linha = linhas[i].strip()
            if re.match(r'^\d+\.\s', linha):
                titulo = re.sub(r'^\d+\.\s+', '', linha)
                # Próxima linha é descrição
                descricao = ""
                if i + 1 < len(linhas):
                    descricao = linhas[i + 1].strip()
                # Linha seguinte geralmente é URL
                url_resultado = ""
                if i + 2 < len(linhas):
                    url_resultado = linhas[i + 2].strip()
                resultados.append({
                    "titulo": titulo,
                    "descricao": descricao,
                    "url": url_resultado,
                    "fonte": "duckduckgo"
                })
                i += 3
            else:
                i += 1
    return resultados


def buscar_google(query):
    """Fallback: busca no Google."""
    query_encoded = urllib.parse.quote(f"site:pncp.gov.br {query}")
    url = f"https://www.google.com/search?q={query_encoded}&hl=pt-BR"
    html = fetch(url)
    resultados = []
    if html:
        # Extrair resultados do Google (formato simples)
        resultados_brutos = re.findall(
            r'<a href="/url\?q=(https?://[^&]+)[^>]*>(.*?)</a>',
            html
        )
        for url_res, titulo in resultados_brutos[:5]:
            resultados.append({
                "titulo": titulo,
                "url": url_res,
                "fonte": "google"
            })
    return resultados


def buscar_oportunidades_governo():
    """Busca oportunidades em sites governamentais."""
    resultados = []
    fontes = [
        "https://www.gov.br/mds/pt-br/acesso-a-informacao/licitacoes-e-contratos/editais-abertos",
        "https://www.gov.br/cidades/pt-br/acesso-a-informacao/licitacoes-e-contratos",
        "https://www.gov.br/mma/pt-br/acesso-a-informacao/licitacoes-e-contratos",
    ]
    
    for fonte_url in fontes:
        html = fetch(fonte_url)
        if html and len(html) > 100:
            resultados.append({
                "fonte": fonte_url,
                "status": "acessado",
                "tamanho": len(html)
            })
        else:
            resultados.append({
                "fonte": fonte_url,
                "status": "indisponivel",
                "tamanho": 0
            })
    return resultados


def verificar_relevancia(titulo, descricao=""):
    """Verifica se um resultado é relevante para COREGOV."""
    texto = f"{titulo} {descricao}".lower()
    
    # Verificar exclusão primeiro
    for excluir in EXCLUIR:
        if excluir in texto:
            return False, f"excluído por: {excluir}"
    
    # Verificar relevância
    Palavras_relevantes = [
        "captação", "capta", "recursos", "estatuto", "ong", "osc",
        "terceiro setor", "ongs", "organização social", "projeto social",
        "socioambiental", "arborização", "meio ambiente", "sustentável",
        "desenvolvimento social", "assistência social", "geração de renda",
        "emprego e renda", "consórcio", "consórcios", "convênio",
        "transferegov", "fundo nacional", "chamamento público",
        "credenciamento consultor", "consultoria",
    ]
    
    for p in Palavras_relevantes:
        if p in texto:
            return True, f"match: {p}"
    
    return False, "baixa relevância"


def carregar_historico():
    """Carrega histórico de alertas."""
    if os.path.exists(ARQUIVO_HISTORICO):
        try:
            with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"alertas_emitidos": [], "ultima_verificacao": None}


def salvar_historico(historico):
    """Salva histórico de alertas."""
    with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)


def registrar_alerta(alerta):
    """Registra um alerta no arquivo."""
    if os.path.exists(ARQUIVO_ALERTAS):
        try:
            with open(ARQUIVO_ALERTAS, "r", encoding="utf-8") as f:
                alertas = json.load(f)
        except (json.JSONDecodeError, IOError):
            alertas = []
    else:
        alertas = []
    
    alertas.append(alerta)
    
    # Manter só últimos 100 alertas
    if len(alertas) > 100:
        alertas = alertas[-100:]
    
    with open(ARQUIVO_ALERTAS, "w", encoding="utf-8") as f:
        json.dump(alertas, f, ensure_ascii=False, indent=2)


def gerar_relatorio(resultados_por_palavra, oportunidades_gov=None):
    """Gera relatório formatado."""
    linhas = []
    linhas.append("=" * 55)
    linhas.append("  [MONITOR] MONITOR DE LICITAÇÕES PNCP — COREGOV")
    linhas.append(f"  [DATA] {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    linhas.append("=" * 55)
    linhas.append("")
    
    total_relevantes = 0
    
    for palavra, resultados in sorted(resultados_por_palavra.items()):
        relevantes = [r for r in resultados if r.get("relevante")]
        if relevantes:
            total_relevantes += len(relevantes)
            linhas.append(f"\n[BUSCAR] '{palavra}' — {len(relevantes)} resultado(s)")
            linhas.append("-" * 45)
            for r in relevantes[:5]:  # Top 5
                linhas.append(f"  [PIN] {r.get('titulo', 'Sem título')}")
                if r.get("descricao"):
                    desc = r["descricao"][:120]
                    linhas.append(f"     {desc}")
                if r.get("url"):
                    linhas.append(f"     🔗 {r['url']}")
                linhas.append("")
    
    if total_relevantes == 0:
        linhas.append("  [CAIXA] Nenhum resultado relevante encontrado nesta rodada.")
    
    if oportunidades_gov:
        linhas.append(f"\n  [GOV]  Fontes governamentais verificadas: {len(oportunidades_gov)}")
        for og in oportunidades_gov:
            status_icone = "[OK]" if og.get("status") == "acessado" else "[AVISO]"
            linhas.append(f"     {status_icone} {og.get('fonte', '')}")
    
    linhas.append("")
    linhas.append("=" * 55)
    linhas.append(f"  Total de resultados relevantes: {total_relevantes}")
    linhas.append(f"  Palavras-chave monitoradas: {len(PALAVRAS_CHAVE)}")
    linhas.append("=" * 55)
    
    return "\n".join(linhas), total_relevantes


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Monitor PNCP COREGOV")
    parser.add_argument("--watch", action="store_true", help="Modo contínuo")
    parser.add_argument("--quiet", action="store_true", help="Modo silencioso")
    parser.add_argument("--only-count", action="store_true", help="Só contagem")
    parser.add_argument("--interval", type=int, default=21600, help="Intervalo em segundos (padrão: 6h)")
    args = parser.parse_args()
    
    if args.watch:
        print(f"[MONITOR] Monitor contínuo iniciado (intervalo: {args.interval//3600}h)")
        print(f"   Pressione Ctrl+C para parar\n")
        import time
        while True:
            print(f"\n[ALARME] {datetime.now().strftime('%d/%m/%Y %H:%M')} — Verificando...")
            try:
                verificar_agora(args.quiet)
            except KeyboardInterrupt:
                print("\n[PARAR]  Monitor parado.")
                break
            except Exception as e:
                print(f"  [AVISO]  Erro: {e}", file=sys.stderr)
            print(f"  [Zzz] Próxima verificação em {args.interval//3600}h...")
            time.sleep(args.interval)
    else:
        verificar_agora(args.quiet, args.only_count)


def verificar_agora(quiet=False, only_count=False):
    """Executa uma rodada de verificação."""
    historico = carregar_historico()
    historico["ultima_verificacao"] = datetime.now().isoformat()
    
    resultados_por_palavra = {}
    total_geral = 0
    
    if not quiet:
        print(f"  [BUSCA] Verificando {len(PALAVRAS_CHAVE)} palavras-chave...")
    
    for i, palavra in enumerate(PALAVRAS_CHAVE):
        if not quiet:
            print(f"     [{i+1}/{len(PALAVRAS_CHAVE)}] {palavra[:40]}...", end=" ")
        
        # Tenta DuckDuckGo (mais leve)
        resultados = buscar_duckduckgo(palavra)
        
        # Se DuckDuckGo falhar, tenta buscar no Google
        if not resultados:
            if not quiet:
                print("->  Google...", end=" ")
            resultados = buscar_google(palavra)
        
        # Classificar relevância
        for r in resultados:
            relevante, motivo = verificar_relevancia(
                r.get("titulo", ""),
                r.get("descricao", "")
            )
            r["relevante"] = relevante
            r["motivo_relevancia"] = motivo
            r["palavra_chave"] = palavra
            if relevante:
                total_geral += 1
        
        resultados_por_palavra[palavra] = resultados
        
        if not quiet:
            relevantes = sum(1 for r in resultados if r.get("relevante"))
            print(f"{len(resultados)} resultados ({relevantes} relevantes)")
    
    # Verificar fontes governamentais
    if not quiet:
        print("  [GOV]  Verificando fontes governamentais...")
    oportunidades_gov = buscar_oportunidades_governo()
    
    # Gerar relatório
    relatorio, total_relevantes = gerar_relatorio(
        resultados_por_palavra,
        oportunidades_gov
    )
    
    if only_count:
        print(f"🔢 {total_relevantes}")
        return
    
    if not quiet:
        print()
        print(relatorio)
    
    # Salvar histórico
    salvar_historico(historico)
    
    # Se encontrou algo relevante, registrar alerta
    if total_relevantes > 0:
        alerta = {
            "timestamp": datetime.now().isoformat(),
            "total_resultados": total_relevantes,
            "palavras_com_match": [
                p for p, rs in resultados_por_palavra.items()
                if any(r.get("relevante") for r in rs)
            ],
            "resumo": relatorio
        }
        registrar_alerta(alerta)
        if not quiet:
            print(f"\n  [ALERTA] {total_relevantes} resultado(s) relevante(s) encontrado(s)! Alerta salvo.")
    
    return total_relevantes


if __name__ == "__main__":
    main()
