# 📋 Levantamento Completo — Infraestrutura COREGOV

## 🏗️ Arquitetura Atual

```
┌─────────────────────────────────────────────────────┐
│                     coregov.com.br                    │
├──────────────────────┬──────────────────────────────┤
│   SITE (GitHub Pages)│    APP (Render + Supabase)    │
│   ─────────────      │    ────────────────────       │
│   ✅ GRATUITO        │    💰 CUSTOS MENSAIS          │
│                      │                               │
│   repo_simulador     │    social-ai-app (Flask)      │
│   • index.html       │    • Render (~$7-15/mês)      │
│   • blog/ (30+ posts)│    • Supabase DB              │
│   • ferramentas/     │    • Supabase Auth            │
│   • servicos/        │    • Supabase Storage         │
│   • professorpro     │    • MercadoPago              │
│   • editais/         │    • IA (PicoClaw/DeepSeek)   │
│   • vagas/           │    • LinkedIn/Instagram API   │
│   • materiais_gerados│                               │
└──────────────────────┴──────────────────────────────┘
```

## 🔍 Detalhamento do App (social-ai-app)

### Rotas do Flask (~50 rotas identificadas)

| Categoria | Rotas | O que faz |
|-----------|-------|-----------|
| **🔐 Auth** | `/login`, `/register`, `/logout`, `/login/google`, `/auth/callback` | Supabase Auth (email/senha + Google OAuth) |
| **📊 Dashboard** | `/` | Visão geral com estatísticas do banco |
| **🤖 Conteúdo IA** | `/ia`, `/gerar-conteudo`, `/api/processar-conteudo` | Geração de posts, roteiros, CTAs, ebooks |
| **📝 Posts** | `/posts-site`, `/agendamentos`, `/publicacoes`, `/deletar/<id>` | CRUD de posts |
| **📹 TikTok** | `/roteiros-tiktok-site` | Roteiros para TikTok |
| **📄 E-books** | `/ebooks-site` | E-books gerados por IA |
| **📊 Infográficos** | `/infograficos-site` | Infográficos |
| **📋 Templates** | `/templates-site` | Templates |
| **💳 Pagamentos** | `/planos`, `/api/mercadopago/ipn` | MercadoPago |
| **📈 Editais** | `/gerar/monitorar-editais` | Monitoramento PNCP |
| **📑 Vagas** | `/vagas`, `/api/vagas/*` | Página de vagas |
| **📋 Estatuto** | `/analisar-estatuto` | Analisador de estatuto ONG |
| **📸 Instagram** | `/instagram/login` | Postagem automática |

### Dependências do App

```
Flask, Gunicorn, Supabase (Python), MercadoPago, PicoClaw
Pillow, fpdf2, PyMuPDF, APScheduler, Flask-Limiter
```

## 💰 Custos Atuais (estimados)

| Serviço | Função | Custo/mês |
|---------|--------|-----------|
| **Render** | Flask hosting | ~$7-15 |
| **Supabase** | DB + Auth + Storage | ~$0-25 (depende do uso) |
| **MercadoPago** | Pagamentos | Taxa por transação |
| **GitHub Pages** | Site estático | ✅ Grátis |
| **DeepSeek/PicoClaw** | IA | ✅ Gratuito |

---

# 🚀 Plano de Migração — Custo Zero

## Opção 1: 🥇 Hugging Face Spaces + Turso + Cloudflare R2
### **Melhor custo-benefício, sem reescrever código**

| Substitui | Por | Custo |
|-----------|-----|-------|
| **Render** → | **Hugging Face Spaces** (Docker/Python) | ✅ Grátis (CPU, sempre ativo) |
| **Supabase DB** → | **Turso** (SQLite serverless) | ✅ Grátis (500MB, 1B rows/mês) |
| **Supabase Auth** → | **Auth0** ou **Supabase free tier limitado** | ✅ Grátis (7k usuários) |
| **Supabase Storage** → | **Cloudflare R2** | ✅ Grátis (10GB) |
| **GitHub Actions** → | Cron jobs para scraping/monitoramento | ✅ Grátis (2000 min/mês) |

**Vantagens:**
- Python puro, **não precisa reescrever nada**
- HF Spaces já tem GPU opcional (se quiser)
- Espaço sempre ativo (sem cold start)
- Turso usa SQLite — compatível com Python

**Desvantagens:**
- HF Spaces tem CPU limitada (2 vCPUs, 16GB RAM no free)
- Precisa adaptar queries Supabase → Turso (SQLite)

---

## Opção 2: 🥈 Cloudflare Pages + Functions
### **Mais moderno, edge computing**

| Substitui | Por | Custo |
|-----------|-----|-------|
| **Render** → | **Cloudflare Pages** (static) + **Functions** (backend) | ✅ Grátis (100k req/dia) |
| **Supabase DB** → | **D1 (SQLite nativo Cloudflare)** | ✅ Grátis (5GB) |
| **Supabase Auth** → | **Cloudflare Access** | ✅ Grátis (50 users) |
| **Supabase Storage** → | **Cloudflare R2** | ✅ Grátis (10GB) |

**Vantagens:**
- Latência baixíssima (edge)
- Tudo na Cloudflare
- 100k requests/dia gratuitos

**Desvantagens:**
- ⚠️ **Precisa reescrever Flask em JS/TS** (Cloudflare Workers)
- D1 é beta ainda
- Complexidade de migração alta

---

## Opção 3: 🥉 Vercel + Neon DB
### **Popular, fácil de começar**

| Substitui | Por | Custo |
|-----------|-----|-------|
| **Render** → | **Vercel** (serverless Python) | ✅ Grátis (100h/mês) |
| **Supabase DB** → | **Neon** (Postgres serverless) | ✅ Grátis (500MB) |
| **Supabase Storage** → | **Uploadthing** ou **Cloudinary** | ✅ Grátis (2GB) |
| **Supabase Auth** → | **NextAuth** ou **Supabase free** | ✅ Grátis |

**Vantagens:**
- Suporta Python (serverless functions)
- Neon é Postgres → compatível com Supabase
- Muito popular, boa documentação

**Desvantagens:**
- 100h/mês pode ser pouco se o app fica sempre ligado
- Cold start nas functions

---

## 🎯 Opção Recomendada: HÍBRIDA

```
┌── SITE (coregov.com.br) ──┐
│   GitHub Pages             │  ✅ JÁ FUNCIONA
│   (repo_simulador)         │
└────────────────────────────┘

┌── APP (app.coregov.com.br) ─┐
│   Hugging Face Spaces        │  ✅ GRATUITO
│   (Flask, sem mudanças)      │
├──────────────────────────────┤
│   Turso (SQLite serverless)  │  ✅ GRATUITO
│   (substitui Supabase DB)    │
├──────────────────────────────┤
│   Cloudflare R2 (storage)    │  ✅ GRATUITO
│   (substitui Supabase Stor.) │
├──────────────────────────────┤
│   GitHub Actions (cron)      │  ✅ GRATUITO
│   (agendamentos, scraping)   │
└──────────────────────────────┘

┌── DOMÍNIO ──────────────────┐
│   Cloudflare (DNS free)      │  ✅ JÁ FUNCIONA
└──────────────────────────────┘
```

### 📋 Passo a Passo da Migração

#### Fase 1 — Site (sem alterações)
- ✅ **GitHub Pages** mantido como está
- Apenas atualizar DNS se necessário

#### Fase 2 — Backend (Render → HF Spaces)
1. Criar Dockerfile para o Flask
2. Publicar no Hugging Face Spaces
3. Configurar variáveis de ambiente
4. Redirecionar DNS

#### Fase 3 — Banco (Supabase → Turso)
1. Exportar dados do Supabase (tabelas: users, posts, conteudos, analytics, etc.)
2. Criar schema SQLite equivalente
3. Adaptar queries no app.py (trocar `supabase.table("X").select()` por queries SQLite)
4. Importar dados para Turso

#### Fase 4 — Storage (Supabase → R2)
1. Baixar todas as imagens do Supabase Storage
2. Fazer upload para Cloudflare R2
3. Atualizar URLs no banco

#### Fase 5 — Auth (Supabase Auth → alternativo)
1. Simplificar para login com senha hash + sessão em cookie
2. Ou usar Supabase auth apenas no free tier

#### Fase 6 — Cron Jobs (APScheduler → GitHub Actions)
1. Migrar scraping de editais, PNCP, etc. para GitHub Actions
2. Manter scheduler no app apenas para tarefas em tempo real

---

## 🔧 Complexidade da Migração

| Componente | Esforço | Dificuldade |
|-----------|---------|-------------|
| Site → GitHub Pages | ✅ Já feito | Nenhuma |
| Flask → HF Spaces | ⏱️ 2-3h | Fácil |
| Supabase DB → Turso/SQLite | ⏱️ 4-8h | Média |
| Supabase Storage → R2 | ⏱️ 1-2h | Fácil |
| Supabase Auth → alternativo | ⏱️ 4-6h | Média |
| Adaptar queries no app.py | ⏱️ 6-10h | Média |
| MercadoPago (mantém) | ✅ Sem alteração | Nenhuma |
| GitHub Actions (cron) | ⏱️ 2-3h | Fácil |

**Tempo total estimado: 20-30h de trabalho**

---

## ⚡ Sugestão Minimalista (se quiser simplificar AGORA)

Se a ideia é reduzir custos SEM complexidade, o caminho mais rápido é:

1. **Flask no HF Spaces** (migração simples, sem mudar código)
2. **Manter Supabase no free tier** (enquanto couber no limite)
3. **Manter GitHub Pages** para tudo que é estático

Isso já elimina o custo do Render. E quando o Supabase free acabar, migra o banco.
