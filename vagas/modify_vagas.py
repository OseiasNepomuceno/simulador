#!/usr/bin/env python3
"""Aplica todas as modificacoes na pagina de vagas"""
import re

with open("repo_simulador/vagas/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# === 1. SUBSTITUIR onclicks dos botoes de plano ===
# Bronze
html = html.replace(
    '<a href="https://mpago.la/2UmiPMV" target="_blank" class="btn-plano btn-prata"  \nonclick="event.stopPropagation();">\U0001f949 Assinar Bronze</a>',
    '<a href="#" class="btn-plano btn-prata" onclick="event.preventDefault();abrirModalEmail(\'bronze\')">\U0001f949 Assinar Bronze</a>'
)
# Prata
html = html.replace(
    '<a href="https://mpago.la/1XWEeC6" target="_blank" class="btn-plano btn-prata"  \nonclick="event.stopPropagation();">\U0001f949\U0000005a Assinar Prata</a>',
    '<a href="#" class="btn-plano btn-prata" onclick="event.preventDefault();abrirModalEmail(\'prata\')">\U0001f949\U0000005a Assinar Prata</a>'
)
# Ouro
html = html.replace(
    '<a href="https://mpago.la/2mSYs6U" target="_blank" class="btn-plano btn-ouro"  \nonclick="event.stopPropagation();">\U0001f949\'Z Assinar Ouro</a>',
    '<a href="#" class="btn-plano btn-ouro" onclick="event.preventDefault();abrirModalEmail(\'ouro\')">\U0001f949\'Z Assinar Ouro</a>'
)
# Diamante
html = html.replace(
    '<a href="https://mpago.la/2fCg4C2" target="_blank" class="btn-plano btn-diamante"  \nonclick="event.stopPropagation();">\U0001f949\'\' Assinar Diamante</a>',
    '<a href="#" class="btn-plano btn-diamante" onclick="event.preventDefault();abrirModalEmail(\'diamante\')">\U0001f949\'\' Assinar Diamante</a>'
)

# === 2. ADICIONAR CSS DO MODAL EMAIL e VERIFICACAO (antes do fechamento </style>) ===
css_extra = """
        /* EMAIL CAPTURE MODAL */
        .modal-email-overlay {
            display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.6); z-index: 400;
            align-items: center; justify-content: center; padding: 24px;
        }
        .modal-email-overlay.active { display: flex; }
        .modal-email {
            background: white; border-radius: 24px; max-width: 440px; width: 100%;
            padding: 40px 36px; text-align: center;
            animation: modalIn 0.3s ease; position: relative;
        }
        .modal-email .modal-close {
            position: absolute; top: 16px; right: 20px; font-size: 1.5rem;
            cursor: pointer; color: var(--text-light); background: none; border: none;
        }
        .modal-email .modal-close:hover { color: var(--accent); }
        .modal-email h2 { color: var(--primary); margin-bottom: 8px; }
        .modal-email p { color: var(--text-light); margin-bottom: 20px; font-size: 0.95rem; }
        .modal-email .plano-label {
            display: inline-block; background: var(--gold); color: var(--primary-dark);
            padding: 4px 16px; border-radius: 20px; font-weight: 700;
            font-size: 0.85rem; margin-bottom: 16px;
        }
        .modal-email input[type="email"] {
            width: 100%; padding: 14px 16px; border: 2px solid var(--border);
            border-radius: 12px; font-size: 1rem; outline: none;
            transition: all 0.2s; margin-bottom: 12px;
        }
        .modal-email input[type="email"]:focus {
            border-color: var(--primary); box-shadow: 0 0 0 3px rgba(15,52,96,0.1);
        }
        .modal-email .btn-email-submit {
            width: 100%; background: var(--primary); color: white; border: none;
            padding: 14px; border-radius: 12px; font-weight: 700;
            font-size: 1rem; cursor: pointer; transition: all 0.3s;
        }
        .modal-email .btn-email-submit:hover { background: var(--primary-light); transform: translateY(-2px); }
        .modal-email .btn-email-submit:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
        .modal-email .email-erro { color: var(--accent); font-size: 0.85rem; margin-top: 8px; display: none; }
        .modal-email .email-erro.show { display: block; }
        .modal-email .email-sucesso { color: var(--green); font-size: 0.9rem; margin-top: 8px; display: none; }
        .modal-email .email-sucesso.show { display: block; }

        /* VERIFICAR ACESSO SECTION */
        .verificar-section {
            background: var(--bg); padding: 40px 24px; border-bottom: 1px solid var(--border);
            text-align: center;
        }
        .verificar-inner { max-width: 500px; margin: 0 auto; }
        .verificar-inner h3 { color: var(--primary); font-size: 1.3rem; margin-bottom: 8px; }
        .verificar-inner p { color: var(--text-light); font-size: 0.95rem; margin-bottom: 16px; }
        .verificar-inner .input-group {
            display: flex; gap: 8px; max-width: 400px; margin: 0 auto;
        }
        .verificar-inner .input-group input {
            flex: 1; padding: 12px 16px; border: 2px solid var(--border);
            border-radius: 10px; font-size: 0.95rem; outline: none;
        }
        .verificar-inner .input-group input:focus { border-color: var(--primary); }
        .verificar-inner .input-group button {
            background: var(--primary); color: white; border: none;
            padding: 12px 24px; border-radius: 10px; font-weight: 700;
            cursor: pointer; transition: all 0.2s; white-space: nowrap;
        }
        .verificar-inner .input-group button:hover { background: var(--primary-light); }
        .verificar-result {
            margin-top: 12px; padding: 12px; border-radius: 10px;
            font-size: 0.95rem; display: none;
        }
        .verificar-result.ativo {
            display: block; background: rgba(46,204,113,0.1);
            border: 1px solid var(--green); color: #1a7a3a;
        }
        .verificar-result.inativo {
            display: block; background: rgba(233,69,96,0.08);
            border: 1px dashed var(--accent); color: var(--accent);
        }
"""

html = html.replace("</style>", css_extra + "\n    </style>")

# === 3. ADICIONAR HTML DO MODAL EMAIL (antes do modal de vaga existente) ===
modal_email_html = """
<!-- MODAL CAPTURA EMAIL -->
<div class="modal-email-overlay" id="modalEmail" onclick="if(event.target===this)fecharModalEmail()">
    <div class="modal-email">
        <button class="modal-close" onclick="fecharModalEmail()">&times;</button>
        <div style="font-size:3rem;margin-bottom:12px;" id="modalEmailIcon">\U0001f949</div>
        <h2 id="modalEmailTitle">Assinar Plano</h2>
        <span class="plano-label" id="modalEmailPlano">BRONZE</span>
        <p id="modalEmailDesc">Digite seu email para receber o link de pagamento e ativar seu acesso.</p>
        <input type="email" id="inputEmail" placeholder="seu@email.com" autocomplete="email">
        <div class="email-erro" id="emailErro">Por favor, insira um email válido.</div>
        <div class="email-sucesso" id="emailSucesso"></div>
        <button class="btn-email-submit" id="btnEmailSubmit" onclick="enviarEmail()">
            \U0001f4e8 Continuar para Pagamento
        </button>
    </div>
</div>
"""

html = html.replace(
    '<!-- MODAL -->',
    modal_email_html + '\n<!-- MODAL -->'
)

# === 4. ADICIONAR SECAO VERIFICAR ACESSO (depois da secao planos, antes do rastreio) ===
verificar_html = """
<!-- SECAO VERIFICAR ACESSO -->
<section class="verificar-section" id="verificar">
    <div class="verificar-inner">
        <h3>\U0001f50d Verificar Meu Acesso</h3>
        <p>Já assinou? Digite o email usado no pagamento para liberar as vagas do seu plano.</p>
        <div class="input-group">
            <input type="email" id="inputVerificarEmail" placeholder="seu@email.com" autocomplete="email">
            <button onclick="verificarAcesso()">\U00002728 Verificar</button>
        </div>
        <div class="verificar-result" id="verificarResult"></div>
    </div>
</section>
"""

html = html.replace(
    '<!-- SEC\u00c7\u00c3O RASTREAMENTO -->',
    verificar_html + '\n<!-- SEC\u00c7\u00c3O RASTREAMENTO -->'
)

# === 5. ADICIONAR FUNCOES JS (antes de filtrarVagas()) ===
js_extra = """
// ===== ASSINATURA VAGAS - CAPTURA DE EMAIL =====
let planoSelecionado = '';

const PLANOS_INFO = {
    bronze: { nome: 'Bronze', icone: '\U0001f949', faixa: 'R$ 3.001 ~ R$ 5.000', preco: 'R$ 9,90/trimestre', link: 'https://mpago.la/2UmiPMV' },
    prata: { nome: 'Prata', icone: '\U0001f949\U0000005a', faixa: 'R$ 5.001 ~ R$ 8.000', preco: 'R$ 15,00/trimestre', link: 'https://mpago.la/1XWEeC6' },
    ouro: { nome: 'Ouro', icone: '\U0001f949\'Z', faixa: 'R$ 8.001 ~ R$ 10.000', preco: 'R$ 35,00/trimestre', link: 'https://mpago.la/2mSYs6U' },
    diamante: { nome: 'Diamante', icone: '\U0001f949\'\'', faixa: 'Acima de R$ 10.000', preco: 'R$ 69,90/trimestre', link: 'https://mpago.la/2fCg4C2' }
};

function abrirModalEmail(plano) {
    planoSelecionado = plano;
    const info = PLANOS_INFO[plano];
    if (!info) return;

    document.getElementById('modalEmailIcon').textContent = info.icone;
    document.getElementById('modalEmailTitle').textContent = 'Assinar ' + info.nome;
    document.getElementById('modalEmailPlano').textContent = info.nome.toUpperCase() + ' - ' + info.faixa;
    document.getElementById('modalEmailDesc').textContent = 'Apenas ' + info.preco + '. Digite seu email e siga para o pagamento no Mercado Pago.';
    document.getElementById('inputEmail').value = '';
    document.getElementById('emailErro').classList.remove('show');
    document.getElementById('emailSucesso').classList.remove('show');
    document.getElementById('btnEmailSubmit').disabled = false;
    document.getElementById('btnEmailSubmit').textContent = '\U0001f4e8 Continuar para Pagamento';

    document.getElementById('modalEmail').classList.add('active');
    document.body.style.overflow = 'hidden';
    setTimeout(() => { document.getElementById('inputEmail').focus(); }, 300);
}

function fecharModalEmail() {
    document.getElementById('modalEmail').classList.remove('active');
    document.body.style.overflow = 'auto';
}

function enviarEmail() {
    const email = document.getElementById('inputEmail').value.trim();
    if (!email || !email.includes('@') || !email.includes('.')) {
        document.getElementById('emailErro').textContent = 'Por favor, insira um email v\u00e1lido.';
        document.getElementById('emailErro').classList.add('show');
        return;
    }

    document.getElementById('emailErro').classList.remove('show');
    document.getElementById('btnEmailSubmit').disabled = true;
    document.getElementById('btnEmailSubmit').textContent = '\u23f3 Registrando...';

    // Salvar email no localStorage
    localStorage.setItem('coregov_email', email);
    localStorage.setItem('coregov_plano_' + planoSelecionado, 'pending');

    // Enviar para o backend
    fetch('https://app.coregov.com.br/api/vagas/capturar-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email, plano: planoSelecionado })
    })
    .then(r => r.json())
    .then(data => {
        if (data.success && data.ja_assinante) {
            document.getElementById('emailSucesso').textContent = '\u2705 ' + data.mensagem;
            document.getElementById('emailSucesso').classList.add('show');
            document.getElementById('btnEmailSubmit').textContent = '\U0001f517 Ir para vagas';
            document.getElementById('btnEmailSubmit').onclick = function() { fecharModalEmail(); window.location.reload(); };
            return;
        }

        // Redirecionar para o MP
        document.getElementById('emailSucesso').textContent = '\u2705 Email registrado! Redirecionando...';
        document.getElementById('emailSucesso').classList.add('show');
        document.getElementById('btnEmailSubmit').textContent = '\u23f3 Redirecionando...';

        const link = data.redirect_url || PLANOS_INFO[planoSelecionado].link;
        setTimeout(() => { window.location.href = link; }, 800);
    })
    .catch(err => {
        // Fallback: redirecionar direto
        const link = PLANOS_INFO[planoSelecionado].link;
        window.location.href = link;
    });
}

function verificarAcesso() {
    const email = document.getElementById('inputVerificarEmail').value.trim();
    const resultEl = document.getElementById('verificarResult');

    if (!email || !email.includes('@')) {
        resultEl.className = 'verificar-result inativo';
        resultEl.textContent = 'Por favor, digite um email v\u00e1lido.';
        return;
    }

    resultEl.className = 'verificar-result';
    resultEl.textContent = '\u23f3 Verificando...';
    resultEl.style.display = 'block';

    fetch('https://app.coregov.com.br/api/vagas/verificar-acesso?email=' + encodeURIComponent(email))
    .then(r => r.json())
    .then(data => {
        if (data.acesso) {
            resultEl.className = 'verificar-result ativo';
            resultEl.innerHTML = '\u2705 <strong>Acesso Liberado!</strong> Plano ' + data.plano.charAt(0).toUpperCase() + data.plano.slice(1) + '.<br>As vagas do seu plano j\u00e1 est\u00e3o vis\u00edveis com empresa e contato.';
            localStorage.setItem('coregov_email', email);
            localStorage.setItem('coregov_plano_' + data.plano, 'ativo');
            // Recarregar para aplicar
            setTimeout(() => { window.location.reload(); }, 1500);
        } else {
            resultEl.className = 'verificar-result inativo';
            resultEl.innerHTML = '\U0001f512 ' + (data.mensagem || 'Nenhuma assinatura ativa encontrada.') + '<br><a href="#planos" style="color:var(--accent);font-weight:700;">\U0001f449 Assinar agora</a>';
        }
    })
    .catch(err => {
        resultEl.className = 'verificar-result inativo';
        resultEl.textContent = 'Erro ao verificar. Tente novamente.';
    });
}

// Auto-verificar se email salvo
(function() {
    const savedEmail = localStorage.getItem('coregov_email');
    if (savedEmail) {
        // Verificar se tem alguma assinatura ativa
        fetch('https://app.coregov.com.br/api/vagas/verificar-acesso?email=' + encodeURIComponent(savedEmail))
        .then(r => r.json())
        .then(data => {
            if (data.acesso) {
                localStorage.setItem('coregov_plano_' + data.plano, 'ativo');
            }
        })
        .catch(() => {});
    }
})();

"""

html = html.replace("filtrarVagas();", js_extra + "\nfiltrarVagas();")

# Salvar
with open("repo_simulador/vagas/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Modificacoes aplicadas com sucesso!")
print(f"   Tamanho final: {len(html)} bytes")
