from fastapi import FastAPI
from supabase import create_client
import os

app = FastAPI()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.post("/gerar-conteudo")
def gerar_conteudo(titulo: str, tipo: str):
    # chama Picoclaw
    resultado = chamar_picoclaw(f"Crie um {tipo} sobre {titulo}")
    if resultado.get("success"):
        conteudo = resultado["conteudo"]
        supabase.table("conteudos").insert({
            "titulo": titulo,
            "tipo": tipo,
            "conteudo": conteudo,
            "status": "rascunho"
        }).execute()
        return {"status": "ok", "conteudo": conteudo}
    return {"status": "erro"}
