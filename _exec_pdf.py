"""Gera PDF do exemplo de Matematica - Fracoes"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
exec(open(os.path.join(os.path.dirname(__file__), "gerar_pdf_professor.py"), encoding="utf-8").read())
