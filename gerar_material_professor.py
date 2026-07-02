"""
🎯 ProfessorPro — Gerador de Material Didático com IA + Pixabay
Uso: python gerar_material_professor.py

Fluxo:
1. Recebe dados do formulário (ou parametros via linha de comando)
2. PicoClaw monta prompt e chama DeepSeek
3. Busca imagem no Pixabay (gratuita)
4. Gera PDF com emojis + imagem + design moderno
5. Salva em /materiais_gerados/
"""

import json
import subprocess
import os
import re
import requests
import textwrap
from datetime import datetime
from pathlib import Path

# =========================
# CONFIG
# =========================

PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY", "")
PICOCLAW_BIN = os.getenv("PICOCLAW_BIN", "picoclaw")
OUTPUT_DIR = Path(__file__).parent / "materiais_gerados"
OUTPUT_DIR.mkdir(exist_ok=True)

# =========================
# 1. CHAMAR PICOCLAW -> DEEPSEEK
# =========================

def chamar_picoclaw(mensagem: str, timeout: int = 120) -> dict:
    """Envia prompt ao PicoClaw que roteia pro DeepSeek."""
    print(f"🦞 PicoClaw acionado — {len(mensagem)} chars")
    try:
        resultado = subprocess.run(
            [PICOCLAW_BIN, 'agent', '-m', mensagem],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        saida = resultado.stdout.strip()

        # Limpa output
        linhas = saida.split('\n')
        linhas_limpas = [
            l for l in linhas
            if l.strip()
            and '█' not in l
            and '╚' not in l
            and '╔' not in l
            and '╗' not in l
            and '╝' not in l
            and '🦞' not in l
        ]
        resposta = '\n'.join(linhas_limpas).strip()
        resposta = re.sub(r'\x1b\[[0-9;]*m', '', resposta)
        resposta = re.sub(r'\[0m', '', resposta)

        if resultado.returncode != 0 or not resposta:
            return {"success": False, "conteudo": resultado.stderr.strip() or "Sem resposta"}

        return {"success": True, "conteudo": resposta}

    except subprocess.TimeoutExpired:
        return {"success": False, "conteudo": "Timeout"}
    except Exception as e:
        return {"success": False, "conteudo": str(e)}


# =========================
# 2. BUSCAR IMAGEM NO PIXABAY
# =========================

def buscar_imagem_pixabay(tema: str) -> str:
    """Busca imagem relacionada ao tema no Pixabay. Retorna URL ou None."""
    if not PIXABAY_API_KEY:
        print("⚠️  PIXABAY_API_KEY não configurada — pulando busca de imagem")
        return None

    # Palavras-chave em português e inglês
    keywords = [tema, f"{tema} education", f"{tema} school"]
    
    for kw in keywords:
        try:
            url = "https://pixabay.com/api/"
            params = {
                "key": PIXABAY_API_KEY,
                "q": kw,
                "lang": "pt",
                "image_type": "photo",
                "orientation": "horizontal",
                "per_page": 3,
                "safesearch": "true"
            }
            resp = requests.get(url, params=params, timeout=10)
            data = resp.json()
            
            if data.get("hits") and len(data["hits"]) > 0:
                img_url = data["hits"][0]["largeImageURL"]
                print(f"✅ Imagem encontrada: {img_url}")
                return img_url
            
            # Tenta em inglês
            params["q"] = tema
            params["lang"] = "en"
            resp = requests.get(url, params=params, timeout=10)
            data = resp.json()
            
            if data.get("hits") and len(data["hits"]) > 0:
                img_url = data["hits"][0]["largeImageURL"]
                print(f"✅ Imagem encontrada (EN): {img_url}")
                return img_url
                
        except Exception as e:
            print(f"⚠️  Erro Pixabay: {e}")
            continue
    
    print("⚠️  Nenhuma imagem encontrada no Pixabay")
    return None


# =========================
# 3. MONTAR PROMPT PARA O DEEPSEEK
# =========================

def montar_prompt(dados: dict) -> str:
    """Monta o prompt otimizado para gerar o material didático."""
    
    serie = dados["serie"]
    disciplina = dados["disciplina"]
    tema = dados["tema"]
    bncc = dados.get("bncc", [])
    tipos = dados.get("tipos", ["📋 Plano de Aula", "📝 Atividades"])
    
    bncc_str = ", ".join(bncc) if bncc else "Nenhuma específica"
    tipos_str = ", ".join(tipos)

    prompt = f"""Você é um professor especialista em {disciplina} para {serie}. 
Gere um material didático completo de alta qualidade sobre o tema: "{tema}".

Habilidades BNCC: {bncc_str}
Tipo de material solicitado: {tipos_str}

IMPORTANTE: O material será convertido em PDF com design moderno. 
Use emojis nos títulos e seções. 
Estrutura clara com tópicos e subtópicos.
Linguagem adequada para alunos de {serie}.
Se for plano de aula: inclua objetivos, metodologia, recursos, desenvolvimento, avaliação.
Se for atividades: inclua pelo menos 5 questões com enunciados claros, variando dificuldade.
Se for prova: inclua 10 questões (objetivas + discursivas) com gabarito.
Se for slides: numerar cada slide.

Formato da resposta: markdown limpo, sem códigos de formatação complexos.
Use linhas claras de separação entre seções.

Gere o conteúdo completo agora:"""

    return prompt


# =========================
# 4. GERAR PDF (MARKDOWN -> TXT ESTRUTURADO)
# =========================

def gerar_conteudo_formatado(conteudo: str, dados: dict, imagem_url: str = None) -> str:
    """Organiza o conteúdo gerado em formato rico com emojis e imagem."""
    
    serie = dados["serie"]
    disciplina = dados["disciplina"]
    tema = dados["tema"]
    data = datetime.now().strftime("%d/%m/%Y")
    
    blocos = []
    
    # Cabeçalho com imagem
    cabecalho = f"""
╔══════════════════════════════════════════════════════════════╗
║                    🎯 PROFESSORPRO                           ║
║         Material Didático Gerado por IA                      ║
╚══════════════════════════════════════════════════════════════╝

📚 Série: {serie}
🧪 Disciplina: {disciplina}
📌 Tema: {tema}
📅 Data: {data}
"""
    if imagem_url:
        cabecalho += f"\n🖼️ Imagem ilustrativa: {imagem_url}\n"
    
    blocos.append(cabecalho)
    blocos.append("─" * 70)
    blocos.append(conteudo)
    blocos.append("─" * 70)
    
    rodape = """
╔══════════════════════════════════════════════════════════════╗
║            📚 ProfessorPro — by COREGOV                     ║
║               coregov.com.br/professorpro                    ║
║         📲 Dúvidas? WhatsApp: (18) 9 9188-8698                ║
╚══════════════════════════════════════════════════════════════╝
"""
    blocos.append(rodape)
    
    return "\n\n".join(blocos)


# =========================
# 5. SALVAR ARQUIVO
# =========================

def salvar_material(conteudo_formatado: str, dados: dict) -> Path:
    """Salva o material em arquivo .txt estruturado."""
    
    # Nome do arquivo
    tema_clean = re.sub(r'[^a-zA-Z0-9áéíóúàâêãõç ]', '', dados["tema"])
    tema_clean = tema_clean.replace(' ', '_').lower()[:30]
    data_str = datetime.now().strftime("%Y%m%d_%H%M")
    nome_arquivo = f"material_{tema_clean}_{data_str}.txt"
    caminho = OUTPUT_DIR / nome_arquivo
    
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo_formatado)
    
    print(f"✅ Material salvo: {caminho}")
    return caminho


# =========================
# 6. FUNÇÃO PRINCIPAL
# =========================

def gerar_material(dados: dict) -> dict:
    """
    Gera material didático completo.
    
    Args:
        dados: dicionário com serie, disciplina, tema, bncc[], tipos[]
    
    Returns:
        dict com success, caminho_arquivo, pdf_url, imagem_url
    """
    
    print(f"\n{'='*60}")
    print(f"🎯 GERANDO MATERIAL DIDÁTICO")
    print(f"{'='*60}")
    print(f"📚 {dados['serie']} | 🧪 {dados['disciplina']}")
    print(f"📌 {dados['tema']}")
    print(f"{'='*60}\n")
    
    # 1. Buscar imagem
    print("\n🔍 Buscando imagem no Pixabay...")
    imagem_url = buscar_imagem_pixabay(dados["tema"])
    
    # 2. Montar prompt
    print("\n📝 Montando prompt para IA...")
    prompt = montar_prompt(dados)
    
    # 3. Chamar IA
    print("\n🦞 Chamando PicoClaw + DeepSeek...")
    resultado = chamar_picoclaw(prompt, timeout=120)
    
    if not resultado["success"]:
        return {"success": False, "msg": f"Erro na IA: {resultado['conteudo']}"}
    
    conteudo = resultado["conteudo"]
    
    # 4. Formatar
    print("\n📄 Formatando conteúdo com emojis e imagem...")
    conteudo_formatado = gerar_conteudo_formatado(conteudo, dados, imagem_url)
    
    # 5. Salvar
    caminho = salvar_material(conteudo_formatado, dados)
    
    return {
        "success": True,
        "caminho_arquivo": str(caminho),
        "imagem_url": imagem_url,
        "tamanho": len(conteudo_formatado)
    }


# =========================
# CLI
# =========================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--exemplo":
        # Modo exemplo
        dados = {
            "serie": "6º ano EF",
            "disciplina": "Ciências",
            "tema": "Cadeia Alimentar",
            "bncc": ["EF06CI01", "EF06CI02"],
            "tipos": ["📋 Plano de Aula", "📝 Atividades", "📄 Prova"]
        }
        resultado = gerar_material(dados)
        
        print(f"\n{'='*60}")
        print(f"✅ RESULTADO:")
        print(f"{'='*60}")
        print(f"Arquivo: {resultado.get('caminho_arquivo', 'N/A')}")
        print(f"Imagem: {resultado.get('imagem_url', 'Nenhuma')}")
        print(f"Tamanho: {resultado.get('tamanho', 0)} caracteres")
        
    elif len(sys.argv) > 1:
        # Recebe dados via JSON string
        try:
            dados = json.loads(sys.argv[1])
            resultado = gerar_material(dados)
            print(json.dumps(resultado, ensure_ascii=False, indent=2))
        except json.JSONDecodeError as e:
            print(f"❌ Erro no JSON: {e}")
            sys.exit(1)
    else:
        # Modo interativo
        print("🎯 PROFESSORPRO — Gerador de Material Didático\n")
        dados = {
            "serie": input("Série (ex: 6º ano EF): ").strip(),
            "disciplina": input("Disciplina: ").strip(),
            "tema": input("Tema: ").strip(),
            "bncc": input("BNCC (separados por vírgula): ").strip().split(",") if input("Informar BNCC? (s/N): ").lower() == "s" else [],
            "tipos": ["📋 Plano de Aula", "📝 Atividades", "📄 Prova", "📽️ Slides"]
        }
        dados["bncc"] = [b.strip() for b in dados["bncc"] if b.strip()]
        
        resultado = gerar_material(dados)
        print(f"\n✅ Arquivo salvo em: {resultado.get('caminho_arquivo', 'N/A')}")
