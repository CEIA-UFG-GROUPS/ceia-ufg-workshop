import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

# Importa a função que criamos no script anterior
from src.rag import gerar_resposta_rag

app = FastAPI(title="API RAG Educacional")


# Modelo de dados esperado no corpo da requisição POST
class PerguntaRequest(BaseModel):
    pergunta: str


@app.post("/rag")
def endpoint_rag(req: PerguntaRequest):
    """
    Recebe uma pergunta, executa o pipeline RAG e retorna a resposta gerada.
    """
    resposta = gerar_resposta_rag(req.pergunta)
    return {"pergunta": req.pergunta, "resposta": resposta}


if __name__ == "__main__":
    # Roda o servidor na porta 8000
    uvicorn.run("src.04_api:app", host="0.0.0.0", port=8000, reload=True)
