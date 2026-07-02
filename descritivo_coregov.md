# Descritivo — Página Inicial coregov.com.br

## Visão Geral

Landing page profissional para a **CoreGov**, consultoria especializada em estruturação de projetos sociais, elaboração de estatutos, planos de negócio e curadoria de patrocinadores para ONGs.

**URL:** https://coregov.com.br  
**Tecnologia:** HTML + CSS puro (sem frameworks), hospedado via GitHub Pages  
**Responsivo:** Sim — adaptado para desktop, tablet e mobile  

---

## 1. Identidade Visual

### Paleta de Cores

| Cor | Hexadecimal | Uso |
|-----|-------------|-----|
| Azul escuro | `#0f3460` | Títulos, botões primários, header, footer |
| Azul mais escuro | `#091c33` | Footer, hover de botões |
| Dourado | `#f5c518` | Detalhes, badges, ícones, destaque |
| Vermelho | `#e94560` | Acionamento pontual (não utilizado na página) |
| Fundo claro | `#f8fafc` | Background principal |
| Fundo alternativo | `#f1f5f9` | Seções "Sobre" e "Contato" |
| Branco | `#ffffff` | Cards, formulários |
| Texto | `#1e293b` | Corpo do texto |
| Texto suave | `#64748b` | Subtítulos, descrições |

### Tipografia

- **Fonte:** Inter (Google Fonts)
- **Pesos:** 300 a 800
- **Tamanhos:** 12px (tags) a 46px (título hero)

### Ícones

- **Biblioteca:** Font Awesome 6.5.0 (gratuita)
- Usados para: ícones de serviços, redes sociais, bullets de listas, botões

---

## 2. Estrutura da Página (6 Seções)

### 2.1 Header (Fixado no topo)

- **Logo:** `CORE<span>GOV</span>` — azul + dourado
- **Navegação:** Serviços | Sobre | Plataforma | Contato
- **CTA:** Botão "Fale Conosco" (WhatsApp) — destaque azul
- **Efeito:** Fundo com blur (`backdrop-filter: blur(12px)`), sombra ao scroll
- **Mobile:** Menu hamburguer com toggle via JavaScript

### 2.2 Hero (Seção de entrada)

- **Badge:** "Consultoria especializada para ONGs"
- **Título:** "Sua ONG estruturada para crescer e transformar"
- **Subtítulo:** Descrição dos serviços
- **CTAs:** "Ver Serviços" (âncora) + "Falar Agora" (WhatsApp)
- **Card lateral:** Indicadores de impacto:
  - +15 projetos estruturados
  - 4 benefícios listados com check
- **Fundo:** Gradiente sutil com elementos decorativos em radial gradient

### 2.3 Serviços (3 cards)

Grid de 3 colunas com cards de serviço:

| Card | Ícone | Título | Tag | Destaque |
|------|-------|--------|-----|----------|
| 1 | `fa-file-contract` | Elaboração de Estatutos | "Base Legal" | Normal |
| 2 | `fa-chart-line` | Plano de Negócio Social | "⭐ Mais Procurado" | **Sim** (borda dourada) |
| 3 | `fa-hand-holding-heart` | Curadoria de Patrocinadores | "Novo" | Normal |

Cada card possui:
- Ícone com hover animado (fundo azul)
- Descrição do serviço
- Tag indicativa
- Link "Consultar →" direto para WhatsApp

### 2.4 Sobre (Quem Somos)

Layout 2 colunas:
- **Lado esquerdo:** Texto institucional
  - "CoreGov nasceu da experiência prática de quem já estruturou dezenas de projetos sociais"
  - Diferencial: conhecimento técnico + inteligência artificial
- **Lado direito:** 4 indicadores numéricos:
  - +15 Projetos Estruturados
  - +R$ 2M Captados em Editais
  - 100% Adequação Legal
  - +30 ONGs Atendidas

### 2.5 Plataforma (CoreGov App)

Seção secundária apresentando o app coregov.com.br:

- **Badge:** "Tecnologia"
- **Lista de funcionalidades:** Copiloto de IA, agendamento, relatórios, multi-redes
- **Botão:** "Conhecer o App" (outline)
- **Card azul à direita:** "Experimente grátis" com CTA "Criar Conta Gratuita"

### 2.6 Contato

Layout 2 colunas:

**Lado esquerdo — Informações:**
- WhatsApp: (18) 99188-8698
- E-mail: contato@coregov.com.br
- Site: coregov.com.br
- Botão "Fale pelo WhatsApp"

**Lado direito — Formulário:**
- Envia via FormSubmit.co (gratuito, sem servidor)
- Campos: Nome, E-mail, Serviço de interesse (select), Mensagem
- Botão "Enviar Mensagem"

### 2.7 Footer

3 colunas:
- **Brand:** Logo + descrição da consultoria
- **Serviços:** Links rápidos para as seções
- **Links:** Institucionais + WhatsApp

**Parte inferior:** © 2026 + redes sociais (WhatsApp, Instagram, LinkedIn, TikTok)

---

## 3. Elementos Especiais

### Botão Flutuante WhatsApp
- Posição: canto inferior direito (fixed)
- Cor: verde `#25D366`
- Animação: scale ao hover
- Link direto: `wa.me/5518991888698`

### Scroll Suave
- `scroll-behavior: smooth` no HTML
- Navegação por âncoras (`#servicos`, `#sobre`, etc.)

### Formulário
- Integrado com **FormSubmit.co** (serviço gratuito)
- Envia para: contato@coregov.com.br
- Captcha desabilitado (pode ser ativado depois)

---

## 4. Responsividade

| Breakpoint | Comportamento |
|------------|---------------|
| >1024px | Layout padrão 3 colunas serviços, hero 2 colunas |
| 768-1024px | Serviços 2 colunas, fonte hero reduzida |
| <768px (tablet) | Tudo em 1 coluna, menu vira hamburguer, padding ajustado |
| <480px (mobile) | Botões em pilha, indicadores em 1 coluna |

---

## 5. Hospedagem

- **Plataforma:** GitHub Pages
- **Repositório:** `OseiasNepomuceno/simulador`
- **Domínio personalizado:** coregov.com.br
- **Arquivo principal:** `index.html` na raiz do repositório

---

## 6. Próximas Melhorias Possíveis

- [ ] Adicionar página "Quem Somos" (`quem-somos.html`)
- [ ] Adicionar página "Serviços" com detalhamento
- [ ] Criar blog ou página de cases de sucesso
- [ ] Ativar captcha no formulário
- [ ] Conectar Instagram/LinkedIn reais nos links do footer
- [ ] Adicionar analytics (Google Analytics ou similar)

---

*Documento gerado em 19 de junho de 2026.*  
*CoreGov — Consultoria para ONGs e Projetos Sociais*
