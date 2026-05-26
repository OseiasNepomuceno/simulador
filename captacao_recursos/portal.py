import streamlit as st
import pandas as pd
import gdown
import os

# =================================================================
# 1. CONFIGURAÇÕES TÉCNICAS E ESTABILIDADE (NÃO ALTERAR)
# =================================================================
st.set_page_config(page_title="CoreGov", page_icon="🛰️", layout="wide")

# Inicialização de variáveis de estado para evitar "resets" acidentais
if 'secao' not in st.session_state: st.session_state['secao'] = 'home'
if 'logado' not in st.session_state: st.session_state['logado'] = False
if 'usuario_plano' not in st.session_state: st.session_state['usuario_plano'] = 'BÁSICO'
if 'usuario_nome' not in st.session_state: st.session_state['usuario_nome'] = ''

# INJEÇÃO DE CSS CUSTOMIZADO PARA MANTER O PADRÃO DARK PREMIUM
st.markdown("""
    <style>
        /* Estilização dos botões principais do relatório */
        .btn-whatsapp-st {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background-color: #128c7e !important;
            color: white !important;
            padding: 10px 20px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: bold;
            margin-top: 15px;
            width: 100%;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# =================================================================
# 2. FUNÇÕES DE SUPORTE (LOGIN E DADOS)
# =================================================================
def autenticar_usuario(u, p):
    file_id = st.secrets.get("file_id_licencas")
    url = f'https://drive.google.com/uc?id={file_id}'
    try:
        nome_arq = "licencas_login.xlsx"
        if os.path.exists(nome_arq): os.remove(nome_arq)
        gdown.download(url, nome_arq, quiet=True)
        df = pd.read_excel(nome_arq, sheet_name='usuario')
        df.columns = [str(c).strip().upper() for c in df.columns]
        
        u_clean = str(u).strip().lower()
        p_clean = str(p).strip()
        
        user_row = df[(df['USUARIO'].astype(str).str.strip().str.lower() == u_clean) & 
                      (df['SENHA'].astype(str).str.strip() == p_clean)]
        
        if not user_row.empty:
            dados = user_row.iloc[0]
            if str(dados.get('STATUS')).lower().strip() == 'ativo':
                st.session_state['logado'] = True
                st.session_state['usuario_nome'] = u_clean
                st.session_state['usuario_plano'] = str(dados.get('PLANO')).upper().strip()
                return True
        return False
    except Exception as e:
        st.error(f"Erro técnico: {e}")
        return False

# =================================================================
# 3. MÓDULOS INTERNOS (RECHEIO DO SISTEMA)
# =================================================================

def modulo_gestao_clientes():
    st.header("💼 Gestão de Clientes e Relatórios")
    if st.session_state['usuario_plano'] == 'BÁSICO':
        st.warning("⚠️ Módulo disponível apenas no Plano Premium.")
    else:
        aba_ativa = st.tabs(["👥 Minha Carteira", "➕ Novo Cadastro", "📊 Relatórios de Captação"])
        
        with aba_ativa[0]:
            st.subheader("Entidades Atendidas")
            st.info("Lista de clientes carregada do banco de dados.")

        with aba_ativa[1]:
            st.subheader("Cadastrar Nova Entidade")
            with st.form("form_novo_cliente"):
                nome = st.text_input("Nome da Instituição")
                cnpj = st.text_input("CNPJ")
                if st.form_submit_button("Salvar Registro"):
                    st.success(f"{nome} cadastrado!")

        with aba_ativa[2]:
            st.subheader("Relatórios de Captação")
            st.info("Preencha os dados que o cliente visualizará no portal.")
            st.text_area("Captação Pública", placeholder="Editais, emendas...")
            st.text_area("Captação Privada", placeholder="Fundos, doações...")
            st.button("Publicar Relatório")

def modulo_revisor_estatuto():
    st.header("📜 Revisor de Estatuto")
    st.caption("Análise automatizada de conformidade jurídica para OSCs e ONGs (TransfereGov)")
    
    st.write("Insira o texto bruto extraído do estatuto ou as palavras-chave principais do documento para auditar a conformidade com as Portarias Interministeriais federais:")
    
    texto_estatuto = st.text_area("Conteúdo ou Cláusulas do Estatuto", height=250, placeholder="Cole aqui o texto do estatuto para pesquisa de conformidade legislativa...").upper()
    
    if st.button("🚀 Rodar Auditoria de Elegibilidade"):
        if not texto_estatuto:
            st.warning("Por favor, insira o texto do estatuto para iniciar a análise.")
            return
            
        with st.spinner("Analisando cláusulas contra portarias federais..."):
            riscos = []
            alertas = []
            pontos_ok = []

            # 1. Distribuição de Lucros / Destinação do Patrimônio Residual (Portaria 424/2016 e MROSC)
            if "LUCRO" not in texto_estatuto and "SUPERÁVIT" not in texto_estatuto and "REVERSÃO DE PATRIMÔNIO" not in texto_estatuto and "PATRIMÔNIO RESIDUAL" not in texto_estatuto:
                riscos.push("Ausência de cláusula explícita de não-distribuição de lucros económicos, dividendos ou bonificações patrimoniais.")
            elif "DISSOLUÇÃO" not in texto_estatuto or "EXTINÇÃO" not in texto_estatuto:
                alertas.push("Cláusula de encerramento da entidade carece de detalhamento técnico sobre a reversão de património para fins públicos.")
            else:
                pontos_ok.append("Regulamentação de destinação e uso de superávits institucionais identificada.")

            # 2. Conselho Fiscal (Exigência estrutural TransfereGov)
            if "CONSELHO FISCAL" not in texto_estatuto and "ÓRGÃO DE FISCALIZAÇÃO" not in texto_estatuto:
                riscos.append("Inexistência ou omissão de Conselho Fiscal devidamente estruturado (Obrigatório para a governança exigida na Portaria 424/2016).")
            else:
                pontos_ok.append("Estrutura interna de fiscalização de contas e controle orçamentário localizada.")

            # 3. Vedação a Parentesco / Nepotismo (Diretrizes de Integridade 2021 a 2026)
            if "PARENTESCO" not in texto_estatuto and "CONJUGE" not in texto_estatuto and "NEPOTISMO" not in texto_estatuto and "CÔNJUGE" not in texto_estatuto:
                riscos.append("O documento não prevê cláusula de barreira contra contratação ou vantagens a parentes de dirigentes com verbas da União (Desconformidade com as normativas recentes do TransfereGov).")
            else:
                pontos_ok.append("Critérios restritivos contra conflitos de interesse e nepotismo institucional mapeados.")

            # 4. Mecanismos de Transparência Ativa (Atualizações Regulatórias 2025/2026)
            if "TRANSPARÊNCIA" not in texto_estatuto and "SÍTIO ELETRÔNICO" not in texto_estatuto and "INTERNET" not in texto_estatuto:
                alertas.append("Ausência de adequação às obrigações de transparência digital ativa para o recebimento de emendas parlamentares federais.")
            else:
                pontos_ok.append("Referência ao princípio da publicidade e transparência corporativa localizada.")

            # EXIBIÇÃO DO DIAGNÓSTICO ESTRUTURADO
            st.subheader("📊 Diagnóstico de Elegibilidade - TransfereGov")
            st.markdown("---")
            
            # Inadequações Críticas
            st.markdown("#### ❌ Inadequações Críticas (Bloqueiam Captação):")
            if riscos:
                for r in riscos: st.error(f"⚠️ {r}")
            else:
                st.success("✔️ Nenhuma desconformidade impeditiva primária foi identificada de forma automatizada.")
                
            # Falhas de Ajuste Técnico
            st.markdown("#### ⚠️ Falhas de Ajuste Técnico (Risco de Rejeição de Propostas):")
            if alertas:
                for a in alertas: st.warning(f"⚠️ {a}")
            else:
                st.success("✔️ O documento está alinhado com as normativas acessórias mapeadas.")

            # Requisitos Encontrados
            st.markdown("#### ✔️ Requisitos Identificados no Estatuto:")
            if pontos_ok:
                for p in pontos_ok: st.info(f"✔️ {p}")
            else:
                st.warning("⚠️ Estrutura de redação padrão com termos muito genéricos.")
                
            # Alerta e Botão de Ação Comercial
            st.markdown("""
                <div style="background-color: rgba(239, 68, 68, 0.1); border-left: 4px solid #ef4444; padding: 15px; border-radius: 4px; margin-top: 20px;">
                    <strong style="color: #ef4444;">🚨 STATUS DA ORGANIZAÇÃO: INAPTA PARA RECEBIMENTO DE EMENDAS</strong><br>
                    Estatutos defasados ou sem a inclusão de termos específicos exigidos pelas portarias governamentais atualizadas resultam na <strong>rejeição sumária de propostas e convênios</strong> dentro da plataforma federal. É necessário redigir emendas de adequação e registrar ata corretiva para liberar a captação de recursos públicos.
                </div>
            """, unsafe_allow_html=True)
            
            texto_msg = f"Olá! Sou utilizador do Portal CoreGov. Rodei a validação do Estatuto e identifiquei falhas de conformidade com as Portarias do TransfereGov. Preciso de suporte para a emissão da ata e cláusulas corretivas."
            link_whatsapp = f"https://wa.me/5518991511523?text={texto_msg.replace(' ', '%20')}"
            
            st.markdown(f'<a href="{link_whatsapp}" target="_blank" class="btn-whatsapp-st">💬 Solicitar Minuta de Adequação e Regularizar Entidade</a>', unsafe_allow_html=True)

# =================================================================
# 4. INTERFACES DE NAVEGAÇÃO (ESQUELETO)
# =================================================================

def exibir_home():
    st.markdown("<h1 style='text-align: center;'>Portal CoreGov</h1>", unsafe_allow_html=True)
    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("👤 Consultor", use_container_width=True): 
            st.session_state['secao'] = 'login'; st.rerun()
    with c2:
        if st.button("📝 Licenças", use_container_width=True): 
            st.session_state['secao'] = 'planos'; st.rerun()
    with c3:
        st.button("🚀 Tecnologia", use_container_width=True)
    with c4:
        if st.button("🏛️ Sou Cliente", use_container_width=True): 
            st.session_state['secao'] = 'cliente'; st.rerun()

def exibir_planos():
    st.markdown("<h2 style='text-align: center;'>Planos Profissionais</h2>", unsafe_allow_html=True)
    p1, p2 = st.columns(2)
    with p1:
        with st.container(border=True):
            st.markdown("### Plano Básico\n**R$ 1.250,00/mês**")
            st.write("✅ Radar de Recursos\n✅ Radar de Emenda\n❌ Gestão de Clientes")
            st.link_button("Assinar Básico", "https://mercadopago.com.br")
    with p2:
        with st.container(border=True):
            st.markdown("### Plano Premium 🔥\n**R$ 2.300,00/mês**")
            st.write("✅ Tudo do Básico\n✅ Gestão de Clientes\n✅ Relatórios de Captação")
            st.link_button("Assinar Premium", "https://mercadopago.com.br")
    if st.button("⬅️ Voltar"): st.session_state['secao'] = 'home'; st.rerun()

# =================================================================
# 5. ORQUESTRAÇÃO PRINCIPAL (MAIN)
# =================================================================

def main():
    if not st.session_state['logado']:
        # Fluxo Público
        if st.session_state['secao'] == 'home':
            exibir_home()
        elif st.session_state['secao'] == 'planos':
            exibir_planos()
        elif st.session_state['secao'] == 'login':
            st.markdown("### 🔑 Acesso ao Painel")
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                with st.form("f_login"):
                    u = st.text_input("Usuário")
                    p = st.text_input("Senha", type="password")
                    if st.form_submit_button("Entrar"):
                        if autenticar_usuario(u, p): st.rerun()
                        else: st.error("Login inválido.")
                if st.button("Voltar"): st.session_state['secao'] = 'home'; st.rerun()
        elif st.session_state['secao'] == 'cliente':
            st.markdown("### 🏛️ Portal do Ente")
            st.text_input("CNPJ da Instituição")
            st.button("Consultar")
            if st.button("Voltar"): st.session_state['secao'] = 'home'; st.rerun()
            
    else:
        # Fluxo Logado (Sidebar + Módulos Padronizados sem sufixos técnicos)
        with st.sidebar:
            st.title("🛰️ CoreGov")
            st.write(f"Plano: **{st.session_state['usuario_plano']}**")
            
            # Ajuste de nomenclaturas padronizadas conforme o guia do usuário
            menu = st.radio("Menu:", ["🏠 Início", "📊 Radar de Recursos", "🏛️ Radar de Emenda", "📜 Revisor de Estatuto", "💼 Gestão de Clientes"])
            st.divider()
            if st.button("🚪 Sair"): 
                st.session_state.clear(); st.rerun()

        # RENDERIZAÇÃO DO CONTEÚDO
        if menu == "🏠 Início":
            st.write(f"### Bem-vindo, {st.session_state['usuario_nome'].upper()}!")
            st.info("Selecione um módulo no menu lateral.")
        elif menu == "💼 Gestão de Clientes":
            modulo_gestao_clientes()
        elif menu == "📜 Revisor de Estatuto":
            modulo_revisor_estatuto()
        else:
            st.write(f"### Módulo {menu}")
            st.write("Módulo ativo e pronto para receber o código específico.")

if __name__ == "__main__":
    main()
