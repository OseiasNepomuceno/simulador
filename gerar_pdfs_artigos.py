#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera versões PDF-friendly dos artigos do blog"""

def gerar_pdf_artigo_01():
    html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>3 Passos para um Projeto Cultural - COREGOV</title>
<style>
    @page { size: A4; margin: 1.6cm; }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; color: #1a1a1a; line-height: 1.8; font-size: 12pt; padding: 0; }
    .page { max-width: 100%; padding: 0; }
    h1 { font-size: 22pt; color: #0f3460; margin: 20px 0 10px 0; line-height: 1.2; }
    .meta { font-size: 10pt; color: #666; margin-bottom: 24px; }
    h2 { font-size: 16pt; color: #0f3460; margin: 28px 0 12px 0; }
    h3 { font-size: 13pt; color: #1a1a1a; margin: 20px 0 10px 0; }
    p { margin-bottom: 14px; text-align: justify; }
    p strong { color: #0f3460; }
    ul { margin: 10px 0 16px 20px; line-height: 1.8; }
    ul li { margin-bottom: 6px; }
    ul li strong { color: #0f3460; }
    .destaque { background: #f1f5f9; border-left: 4px solid #f5c518; padding: 14px 18px; margin: 18px 0; border-radius: 0 6px 6px 0; font-size: 11pt; }
    .destaque p { margin-bottom: 0; }
    .cta-box { border: 2px solid #f5c518; padding: 20px 24px; margin: 28px 0; text-align: center; border-radius: 8px; }
    .cta-box h2 { margin-top: 0; font-size: 15pt; }
    .cta-box p { margin-bottom: 12px; text-align: center; }
    .footer { margin-top: 30px; padding-top: 14px; border-top: 1px solid #ccc; font-size: 10pt; color: #888; text-align: center; }
    .tag { display: inline-block; font-size: 9pt; color: #f5c518; background: rgba(245,197,24,0.1); padding: 2px 12px; border-radius: 100px; margin-bottom: 10px; }
    @media print { body { font-size: 11pt; } h1 { font-size: 20pt; } h2 { font-size: 14pt; } }
</style>
</head>
<body>
<div class="page">
    <div style="text-align:center; margin-bottom:10px;">
        <span style="font-size:20pt; font-weight:800; color:#0f3460;">CORE<span style="color:#f5c518;">GOV</span></span>
    </div>
    <hr style="border: none; border-top: 2px solid #0f3460; margin-bottom: 20px;">

    <span class="tag">ARTIGO</span>
    <h1>3 Passos Importantes para um Projeto Cultural de Sucesso</h1>
    <p class="meta">10 de julho de 2026 • Leitura: 6 min</p>

    <p>Todo ano, milhões em recursos são destinados à cultura por meio de leis de incentivo, editais públicos e fundos setoriais. Mas muitos projetos culturais — mesmo com ideias brilhantes — acabam reprovados por falhas na estruturação.</p>

    <p>Se você é produtor cultural, artista ou gestor de um espaço cultural, estes <strong>3 passos</strong> são a base para transformar sua ideia em um projeto aprovado e executável.</p>

    <h2>Passo 1 — Diagnóstico e Justificativa</h2>

    <p>Antes de escrever qualquer linha do projeto, você precisa responder a uma pergunta fundamental: <strong>por que esse projeto existe?</strong></p>

    <p>O diagnóstico é a alma do projeto cultural. É onde você demonstra:</p>

    <ul>
      <li><strong>Qual é o problema ou demanda cultural</strong> que seu projeto pretende resolver ou atender</li>
      <li><strong>Quem é o público-alvo</strong> — comunidade, estudantes, artistas locais, terceira idade, etc.</li>
      <li><strong>Qual a relevância social</strong> — por que isso importa para a cidade, o bairro ou a região</li>
      <li><strong>Dados e referências</strong> — números, pesquisas ou experiências anteriores que comprovam a necessidade</li>
    </ul>

    <div class="destaque">
      <p><strong>Dica prática:</strong> Um bom diagnóstico convence o avaliador de que seu projeto não é apenas uma ideia bonita, mas uma resposta a uma necessidade real da comunidade. Use linguagem clara e evite jargões excessivos.</p>
    </div>

    <h2>Passo 2 — Plano de Execução com Cronograma Realista</h2>

    <p>O plano de execução responde a uma pergunta prática: <strong>como o projeto vai acontecer no dia a dia?</strong></p>

    <p>Esse é o passo que mais reprova projetos, não por falta de criatividade, mas por falta de realismo. Avaliadores experientes percebem rapidamente quando um cronograma é irreal ou genérico demais.</p>

    <p>Seu plano de execução deve conter:</p>

    <ul>
      <li><strong>Etapas claras</strong> — pré-produção, produção, pós-produção</li>
      <li><strong>Cronograma detalhado</strong> — mês a mês, com atividades específicas</li>
      <li><strong>Equipe envolvida</strong> — quem faz o quê em cada etapa</li>
      <li><strong>Metodologia</strong> — como as atividades serão realizadas (oficinas, apresentações, exposições, etc.)</li>
      <li><strong>Resultados esperados</strong> — o que será entregue ao final de cada etapa</li>
    </ul>

    <div class="destaque">
      <p><strong>Dica prática:</strong> Se seu cronograma diz que vai montar uma exposição em 15 dias com 3 pessoas, explique como. Se não for possível, ajuste. Avaliadores valorizam mais um projeto modesto bem executado do que um ambicioso que não sai do papel.</p>
    </div>

    <h2>Passo 3 — Orçamento e Contrapartidas</h2>

    <p>O orçamento é onde muitos projetos naufragam. Não por falta de recursos, mas por <strong>falta de clareza e compatibilidade</strong> com a proposta.</p>

    <p>Um orçamento bem estruturado precisa mostrar:</p>

    <ul>
      <li><strong>Custos detalhados</strong> — cada item com valor unitário e total (não adianta colocar "R$ 10 mil para produção" sem detalhar)</li>
      <li><strong>Compatibilidade com o porte do projeto</strong> — o orçamento precisa ser condizente com o cronograma e as atividades</li>
      <li><strong>Fontes de recurso</strong> — quanto vem do edital/lei de incentivo e quanto é contrapartida</li>
      <li><strong>Contrapartidas claras</strong> — sociais, culturais ou econômicas que o projeto devolve para a comunidade</li>
      <li><strong>Plano de prestação de contas</strong> — como cada centavo será comprovado</li>
    </ul>

    <div class="destaque">
      <p><strong>Dica prática:</strong> Itens como "imprevistos" (5-10% do total) e "cachê da equipe" são legítimos e esperados. Não os omita por medo de parecer caro. Um orçamento transparente passa mais credibilidade.</p>
    </div>

    <h2>E depois dos 3 passos?</h2>

    <p>Com esses três pilares bem estruturados, seu projeto cultural já está na frente de 80% dos concorrentes. Mas lembre-se: cada edital ou lei de incentivo tem seus próprios requisitos documentais e burocráticos.</p>

    <p>É aí que entra a importância de ter <strong>toda a documentação da sua organização regularizada</strong> — estatuto, CNPJ, certidões — para não ser desclassificado antes mesmo de ter o conteúdo avaliado.</p>

    <div class="cta-box">
      <h2>Quer estruturar seu projeto cultural?</h2>
      <p>A COREGOV ajuda produtores culturais e organizações a preparar projetos completos para editais e leis de incentivo.</p>
      <p style="font-weight:600; color:#0f3460;">Telegram: @coregovbr | coregov.com.br</p>
    </div>

    <div class="footer">
        COREGOV® • coregov.com.br • Telegram: @coregovbr
    </div>
</div>
</body>
</html>"""
    return html

def gerar_pdf_artigo_02():
    html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Associações de Bairro - Datas Comemorativas 2027 - COREGOV</title>
<style>
    @page { size: A4; margin: 1.6cm; }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; color: #1a1a1a; line-height: 1.8; font-size: 12pt; padding: 0; }
    .page { max-width: 100%; padding: 0; }
    h1 { font-size: 22pt; color: #0f3460; margin: 20px 0 10px 0; line-height: 1.2; }
    .meta { font-size: 10pt; color: #666; margin-bottom: 24px; }
    h2 { font-size: 16pt; color: #0f3460; margin: 28px 0 12px 0; }
    h3 { font-size: 13pt; color: #1a1a1a; margin: 20px 0 10px 0; }
    p { margin-bottom: 14px; text-align: justify; }
    p strong { color: #0f3460; }
    ul { margin: 10px 0 16px 20px; line-height: 1.8; }
    ul li { margin-bottom: 6px; }
    ul li strong { color: #0f3460; }
    .destaque { background: #f1f5f9; border-left: 4px solid #f5c518; padding: 14px 18px; margin: 18px 0; border-radius: 0 6px 6px 0; font-size: 11pt; }
    .destaque p { margin-bottom: 0; }
    .cta-box { border: 2px solid #f5c518; padding: 20px 24px; margin: 28px 0; text-align: center; border-radius: 8px; }
    .cta-box h2 { margin-top: 0; font-size: 15pt; }
    .cta-box p { margin-bottom: 12px; text-align: center; }
    .footer { margin-top: 30px; padding-top: 14px; border-top: 1px solid #ccc; font-size: 10pt; color: #888; text-align: center; }
    .tag { display: inline-block; font-size: 9pt; color: #f5c518; background: rgba(245,197,24,0.1); padding: 2px 12px; border-radius: 100px; margin-bottom: 10px; }
    @media print { body { font-size: 11pt; } h1 { font-size: 20pt; } h2 { font-size: 14pt; } }
</style>
</head>
<body>
<div class="page">
    <div style="text-align:center; margin-bottom:10px;">
        <span style="font-size:20pt; font-weight:800; color:#0f3460;">CORE<span style="color:#f5c518;">GOV</span></span>
    </div>
    <hr style="border: none; border-top: 2px solid #0f3460; margin-bottom: 20px;">

    <span class="tag">ARTIGO</span>
    <h1>Associações de Bairro: Como Planejar e Captar Recursos para Datas Comemorativas em 2027</h1>
    <p class="meta">10 de julho de 2026 • Leitura: 8 min</p>

    <p>Falta pouco mais de um ano para o calendário de 2027. Pode parecer cedo para pensar nisso, mas para quem atua no terceiro setor, <strong>julho de 2026 é o momento ideal para começar o planejamento das festas e eventos do ano que vem</strong>.</p>

    <p>Associações de bairro têm um papel essencial na animação cultural e social das comunidades. Festa junina, aniversário do bairro, Dia das Crianças, Natal solidário — são eventos que fortalecem os laços comunitários. Mas a pergunta que não quer calar é: <strong>como fazer isso sem depender apenas de doações de última hora?</strong></p>

    <p>A resposta está em três pilares: <strong>planejamento antecipado, diversificação de fontes e regularidade documental</strong>. Vamos a eles.</p>

    <h2>1. Planejamento Antecipado — O Mapa do Caminho</h2>

    <p>Comece mapeando as principais datas comemorativas de 2027 relevantes para sua comunidade:</p>

    <ul>
      <li><strong>Fevereiro</strong> — Carnaval (blocos, desfiles, matinês)</li>
      <li><strong>Abril</strong> — Páscoa (ações solidárias, chocolate para crianças)</li>
      <li><strong>Maio</strong> — Festa do Trabalhador, Dia das Mães</li>
      <li><strong>Junho/Julho</strong> — Festas juninas e julinas</li>
      <li><strong>Agosto</strong> — Dia dos Pais, aniversário do bairro (se aplicável)</li>
      <li><strong>Outubro</strong> — Dia das Crianças</li>
      <li><strong>Dezembro</strong> — Natal solidário, celebrações de fim de ano</li>
    </ul>

    <p>Para cada data, responda: <strong>quanto custa, quem faz, e de onde vem o recurso</strong>. Esse exercício simples já revela onde sua associação precisa focar os esforços de captação.</p>

    <div class="destaque">
      <p><strong>Dica prática:</strong> Crie uma planilha com as 5 principais datas e estime o custo de cada uma. Você vai descobrir que, com R$ 5 mil bem planejados, é possível fazer um evento melhor do que com R$ 15 mil de última hora.</p>
    </div>

    <h2>2. Captação de Recursos — De Onde Vai Vir o Dinheiro</h2>

    <p>Uma associação de bairro não precisa (nem deve) depender de uma única fonte. Quanto mais diversificada a captação, mais sustentável o calendário de eventos.</p>

    <h3>Editais municipais e estaduais</h3>
    <p>A maioria das prefeituras e governos estaduais publica editais de fomento à cultura, ao esporte e à assistência social. Muitos aceitam propostas de associações de bairro. O segredo é <strong>estar com a documentação em dia</strong> antes do edital abrir.</p>

    <h3>Parcerias com comércio local</h3>
    <p>Padarias, supermercados, farmácias e lojas do bairro têm interesse em apoiar eventos comunitários — seja com recursos, produtos ou serviços. Em troca, a associação oferece visibilidade (faixas, camisetas, redes sociais).</p>

    <h3>Emendas parlamentares</h3>
    <p>Vereadores e deputados podem destinar emendas para eventos comunitários. O caminho é: apresentar um projeto bem estruturado ao gabinete do parlamentar, com orçamento, cronograma e contrapartidas claras.</p>

    <h3>Taxa de participação simbólica</h3>
    <p>Uma contribuição voluntária de R$ 5 ou R$ 10 por morador que participa do evento pode fazer diferença. O segredo é comunicar com transparência onde o dinheiro será aplicado.</p>

    <h2>3. Regularidade Documental — A Base de Tudo</h2>

    <p>Não importa o quanto sua associação seja querida na comunidade: <strong>sem estatuto atualizado, CNPJ regular e certidões negativas, nenhum edital ou emenda parlamentar será aprovado</strong>.</p>

    <p>Antes de começar a captação, garanta que sua associação tem:</p>

    <ul>
      <li><strong>Estatuto social registrado em cartório</strong> — com finalidades compatíveis com os projetos que pretende realizar</li>
      <li><strong>CNPJ ativo</strong> — com situação fiscal regular na Receita Federal</li>
      <li><strong>Diretoria eleita e registrada</strong> — mandato vigente e atas registradas</li>
      <li><strong>Certidões negativas</strong> — FGTS, INSS, tributos federais, dívida ativa</li>
      <li><strong>Prestação de contas em dia</strong> — demonstrações financeiras dos últimos exercícios</li>
    </ul>

    <div class="destaque">
      <p><strong>Dica prática:</strong> Associações que organizam a documentação entre janeiro e março de cada ano têm muito mais chances de aprovar projetos nos editais que abrem ao longo do ano. O segredo é não deixar para a última hora.</p>
    </div>

    <h2>Calendário Sugerido para 2027</h2>

    <p>Se sua associação começar agora (julho de 2026), este é o cronograma ideal:</p>

    <ul>
      <li><strong>Jul-Set/2026</strong> — Regularização documental (estatuto, certidões, CNPJ)</li>
      <li><strong>Out-Nov/2026</strong> — Mapeamento de editais e contato com parlamentares</li>
      <li><strong>Dez/2026</strong> — Captação de parcerias com comércio local</li>
      <li><strong>Jan-Fev/2027</strong> — Submissão de projetos nos primeiros editais do ano</li>
      <li><strong>Mar-Mai/2027</strong> — Pré-produção dos eventos do primeiro semestre</li>
      <li><strong>Jun-Dez/2027</strong> — Execução dos eventos + prestação de contas</li>
    </ul>

    <h2>Conclusão</h2>

    <p>Associações de bairro que planejam com antecedência, diversificam fontes e mantêm a documentação em dia conseguem realizar eventos de qualidade sem depender de milagres financeiros. O segredo não está em ter muito dinheiro, mas em <strong>começar cedo e fazer bem-feito</strong>.</p>

    <p>2027 está logo ali. O que sua associação vai fazer este mês para começar o planejamento?</p>

    <div class="cta-box">
      <h2>Sua associação quer se preparar para 2027?</h2>
      <p>A COREGOV ajuda associações de bairro a regularizar documentação, estruturar projetos e identificar editais para datas comemorativas e eventos comunitários.</p>
      <p style="font-weight:600; color:#0f3460;">Telegram: @coregovbr | coregov.com.br</p>
    </div>

    <div class="footer">
        COREGOV® • coregov.com.br • Telegram: @coregovbr
    </div>
</div>
</body>
</html>"""
    return html

# Gerar arquivos PDF-friendly
with open("artigo_01_projeto_cultural_pdf.html", "w", encoding="utf-8") as f:
    f.write(gerar_pdf_artigo_01())

with open("artigo_02_associacoes_bairro_2027_pdf.html", "w", encoding="utf-8") as f:
    f.write(gerar_pdf_artigo_02())

print("OK - Artigo 01 PDF: artigo_01_projeto_cultural_pdf.html")
print("OK - Artigo 02 PDF: artigo_02_associacoes_bairro_2027_pdf.html")
print("\nArquivos salvos em: repo_simulador/")
print("Abra no navegador e Ctrl+P -> Salvar como PDF")
