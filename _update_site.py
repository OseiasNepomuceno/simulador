import re

# ====== ALTERAR index.html ======
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. TITLE + META + OG
html = html.replace(
    '<title>CoreGov | Consultoria para ONGs e Projetos Sociais</title>',
    '<title>CoreGov | ONGs \u2022 Prefeituras \u2022 Intelig\u00eancia Artificial</title>'
)

html = html.replace(
    'content="CoreGov: consultoria especializada em estatutos, planos de neg\u00f3cio e capta\u00e7\u00e3o de recursos para ONGs e projetos sociais. +15 projetos estruturados. Transforme sua organiza\u00e7\u00e3o."',
    'content="CoreGov: consultoria para ONGs, recursos federais para prefeituras e agentes de IA para automatizar sua opera\u00e7\u00e3o. Estatuto, Transferegov, capta\u00e7\u00e3o e automa\u00e7\u00e3o inteligente."'
)

html = html.replace(
    'content="consultoria ONG, estatuto ONG, captacao de recursos, plano de negocio social, projetos sociais, adequacao de estatuto"',
    'content="consultoria ONG, estatuto ONG, capta\u00e7\u00e3o de recursos, plano de neg\u00f3cio social, projetos sociais, adequa\u00e7\u00e3o de estatuto, recursos federais, transferegov, arboriza\u00e7\u00e3o, prefeituras, agentes de IA, automa\u00e7\u00e3o de processos, intelig\u00eancia artificial, terceiro setor, gest\u00e3o p\u00fablica"'
)

html = html.replace(
    'content="CoreGov | Consultoria para ONGs e Projetos Sociais">',
    'content="CoreGov | ONGs \u2022 Prefeituras \u2022 Intelig\u00eancia Artificial">'
)

html = html.replace(
    'content="Da elaboracao de estatutos a captacao de recursos: transformamos projetos sociais em oportunidades reais de impacto."',
    'content="Da ONG \u00e0 prefeitura: estruturamos projetos, acessamos recursos federais e automatizamos processos com IA. Estatuto, Transferegov, capta\u00e7\u00e3o e agentes inteligentes."'
)

# 2. HERO BADGE
html = html.replace(
    'Consultoria especializada para ONGs',
    'Consultoria para ONGs \u2022 Prefeituras \u2022 IA'
)

# 3. HERO TITLE
html = html.replace(
    'Sua ONG <span>estruturada</span> para crescer e transformar',
    'Da ONG \u00e0 <span>prefeitura</span>: projetos que captam recursos'
)

# 4. HERO DESCRIPTION
html = html.replace(
    'Da elabora\u00e7\u00e3o de estatutos \u00e0 curadoria de patrocinadores: \n                    transformamos projetos sociais em oportunidades reais \n                    de impacto e sustentabilidade financeira.',
    'Estatutos, planos de neg\u00f3cio, recursos federais via Transferegov \n                    e agentes de IA para automatizar sua opera\u00e7\u00e3o. \n                    Da ONG \u00e0 prefeitura, entregamos tudo pronto.'
)

# 5. HERO CARD - update list items
html = html.replace(
    '<li><i class="fas fa-check-circle"></i> Curadoria de patrocinadores</li>\n                        <li><i class="fas fa-check-circle"></i> Capta\u00e7\u00e3o de recursos</li>',
    '<li><i class="fas fa-check-circle"></i> Recursos federais para prefeituras</li>\n                        <li><i class="fas fa-check-circle"></i> Agentes de IA e automa\u00e7\u00e3o</li>'
)

# 6. ADD 2 NEW SERVICE CARDS - find the end of servicos-grid
# Find the closing div of card 3 (Curadoria) and the closing of servicos-grid
card3_end = 'href="https://wa.me/5518991888698?text=Ol%C3%A1!%20Quero%20saber%20mais%20sobre%20a%20Curadoria%20de%20Patrocinadores." \n                       target="_blank" \n                       class="card-cta">\n                        Consultar <i class="fas fa-arrow-right"></i>\n                    </a>\n                </div>'

card4 = '''                <!-- Card 4: Recursos Federais -->
                <div class="servico-card">
                    <div class="servico-icon">
                        <i class="fas fa-city"></i>
                    </div>
                    <h3>Recursos Federais para Prefeituras</h3>
                    <p>
                        Acesso a recursos n\u00e3o reembols\u00e1veis do Governo Federal via Transferegov. 
                        Editais como ArborizaCidades (FNMA), saneamento e infraestrutura verde. 
                        Da an\u00e1lise de elegibilidade ao envio, entregamos tudo pronto.
                    </p>
                    <span class="servico-tag">Prefeituras</span>
                    <br>
                    <a href="editais/" 
                       class="card-cta">
                        Ver Editais <i class="fas fa-arrow-right"></i>
                    </a>
                </div>

                <!-- Card 5: IA e Automa\u00e7\u00e3o -->
                <div class="servico-card destaque">
                    <div class="servico-icon">
                        <i class="fas fa-robot"></i>
                    </div>
                    <h3>Agentes de IA & Automa\u00e7\u00e3o</h3>
                    <p>
                        Agentes aut\u00f4nomos de Intelig\u00eancia Artificial que eliminam tarefas 
                        repetitivas, automatizam fluxos de dados e criam assistentes 
                        inteligentes de atendimento e gest\u00e3o. Diagn\u00f3stico gratuito de ROI.
                    </p>
                    <span class="servico-tag">\u2b50 Tech</span>
                    <br>
                    <a href="https://wa.me/5518991888698?text=Ol%C3%A1!%20Quero%20saber%20mais%20sobre%20Agentes%20de%20IA%20e%20Automa%C3%A7%C3%A3o." 
                       target="_blank" 
                       class="card-cta">
                        Consultar <i class="fas fa-arrow-right"></i>
                    </a>
                </div>'''

html = html.replace(card3_end, card3_end + '\n' + card4)

# 7. SOBRE TEXT - replace the CoreGov nasceu paragraph
old_sobre_1 = 'A <strong>CoreGov</strong> nasceu da experi\u00eancia pr\u00e1tica de quem j\u00e1 \n                        estruturou dezenas de projetos sociais, elaborou estatutos, \n                        planos de neg\u00f3cio e conex\u00f5es com patrocinadores para ONGs \n                        de todos os portes.'
new_sobre_1 = 'A <strong>CoreGov</strong> nasceu da experi\u00eancia de quem est\u00e1 h\u00e1 mais de \n                        25 anos em projetos sociais, gera\u00e7\u00e3o de emprego e renda, \n                        e desenvolvimento institucional \u2014 unindo for\u00e7as com \n                        <strong>Intelig\u00eancia Artificial</strong> para ampliar resultados.'
html = html.replace(old_sobre_1, new_sobre_1)

old_sobre_2 = 'Nosso diferencial \u00e9 unir <strong>conhecimento t\u00e9cnico</strong> \n                        (legisla\u00e7\u00e3o, gest\u00e3o, finan\u00e7as) com <strong>intelig\u00eancia artificial</strong> \n                        para acelerar entregas e ampliar o alcance dos projetos que \n                        atendemos.'
new_sobre_2 = 'Atendemos <strong>ONGs</strong> (estatutos, planos de neg\u00f3cio, capta\u00e7\u00e3o), \n                        <strong>prefeituras</strong> (recursos federais via Transferegov) e \n                        <strong>empresas</strong> (agentes de IA para automatizar processos). \n                        Nosso diferencial: diagnosticamos onde cada a\u00e7\u00e3o gera retorno \n                        financeiro r\u00e1pido e entregamos tudo pronto.'
html = html.replace(old_sobre_2, new_sobre_2)

# Add keywords paragraph after "Acreditamos que toda organização social merece ter uma base sólida"
old_sobre_3 = 'Acreditamos que toda organiza\u00e7\u00e3o social merece ter uma \n                        base s\u00f3lida para crescer e gerar impacto verdadeiro.'
new_sobre_3 = 'Acreditamos que toda organiza\u00e7\u00e3o social merece ter uma \n                        base s\u00f3lida para crescer e gerar impacto verdadeiro.\n                    </p>\n                    <p>\n                        \ud83d\udd0d <strong>Palavras-chave:</strong> Consultoria para ONGs | \n                        Capta\u00e7\u00e3o de recursos federais | Transferegov | \n                        Arboriza\u00e7\u00e3o urbana | Agentes de IA | \n                        Automa\u00e7\u00e3o de processos | Projetos para prefeituras'
html = html.replace(old_sobre_3, new_sobre_3)

# 8. SOBRE DADOS - update second item
html = html.replace(
    '<div class="numero">Consultoria para MEI, Me e EPP</div>\n                        <div class="rotulo">Recursos para Todos</div>',
    '<div class="numero">ONGs +</div>\n                        <div class="rotulo">Prefeituras + Empresas</div>'
)

# 9. FOOTER TEXT
html = html.replace(
    'Consultoria especializada em estrutura\u00e7\u00e3o de projetos sociais, \n                        estatutos, planos de neg\u00f3cio e curadoria de patrocinadores \n                        para ONGs em todo o Brasil.',
    'Consultoria para ONGs, recursos federais para prefeituras \n                        e agentes de IA para automatizar processos. \n                        Da elabora\u00e7\u00e3o de estatutos ao Transferegov.'
)

# 10. FOOTER COLS - add new links
html = html.replace(
    '<a href="#servicos">Curadoria de Patrocinadores</a>\n                    <a href="#plataforma">CoreGov App</a>',
    '<a href="#servicos">Curadoria de Patrocinadores</a>\n                    <a href="#servicos">Recursos Federais</a>\n                    <a href="#servicos">Agentes de IA</a>\n                    <a href="#plataforma">CoreGov App</a>'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html atualizado com sucesso!")
