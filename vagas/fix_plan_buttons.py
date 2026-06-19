#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aplica modificacoes nos botoes de plano da pagina de vagas"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("repo_simulador/vagas/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# === 1. SUBSTITUIR botoes de plano - LINHA UNICA ===
# Bronze
html = html.replace(
    '<a href="https://mpago.la/2UmiPMV" target="_blank" class="btn-plano btn-prata" onclick="event.stopPropagation();">🥉 Assinar Bronze</a>',
    '<a href="#" class="btn-plano btn-prata" onclick="event.preventDefault();abrirModalEmail(\'bronze\')">🥉 Assinar Bronze</a>'
)
# Prata
html = html.replace(
    '<a href="https://mpago.la/1XWEeC6" target="_blank" class="btn-plano btn-prata" onclick="event.stopPropagation();">🎯 Assinar Prata</a>',
    '<a href="#" class="btn-plano btn-prata" onclick="event.preventDefault();abrirModalEmail(\'prata\')">🎯 Assinar Prata</a>'
)
# Ouro
html = html.replace(
    '<a href="https://mpago.la/2mSYs6U" target="_blank" class="btn-plano btn-ouro" onclick="event.stopPropagation();">💎 Assinar Ouro</a>',
    '<a href="#" class="btn-plano btn-ouro" onclick="event.preventDefault();abrirModalEmail(\'ouro\')">💎 Assinar Ouro</a>'
)
# Diamante
html = html.replace(
    '<a href="https://mpago.la/2fCg4C2" target="_blank" class="btn-plano btn-diamante" onclick="event.stopPropagation();">👑 Assinar Diamante</a>',
    '<a href="#" class="btn-plano btn-diamante" onclick="event.preventDefault();abrirModalEmail(\'diamante\')">👑 Assinar Diamante</a>'
)

# === 2. TAMBEM substituir os botoes de bloqueio nas vagas ===
# "Assinar Bronze" nos cards de vaga bloqueada
html = html.replace(
    '🔓 Assinar Bronze',
    '🔓 Assinar'
)
html = html.replace(
    '🔓 Assinar Prata',
    '🔓 Assinar'
)
html = html.replace(
    '🔓 Assinar Ouro',
    '🔓 Assinar'
)
html = html.replace(
    '🔓 Assinar Diamante',
    '🔓 Assinar'
)
# E links de bloqueio no modal
html = html.replace(
    '🔓 Assinar ',
    '🔓 Assinar '
)

# Count occurrences
print(f"Bronze buttons: {html.count('abrirModalEmail')}")
print(f"mpago.la links still present: {html.count('mpago.la')}")

# Salvar
with open("repo_simulador/vagas/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Correcao aplicada!")
print(f"Tamanho final: {len(html)} bytes")
