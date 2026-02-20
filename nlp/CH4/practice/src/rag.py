import os

from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Carrega a chave da API do arquivo .env
load_dotenv()
cliente_openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

model = SentenceTransformer("all-MiniLM-L6-v2")
qdrant_client = QdrantClient(host="localhost", port=6333)


def buscar_contexto(pergunta: str, limite: int = 3) -> str:
    vetor = model.encode(pergunta).tolist()
    resultados = qdrant_client.search(
        collection_name="squad_docs", query_vector=vetor, limit=limite
    )
    # Junta os textos recuperados em uma única string
    contexto = "\n\n".join([res.payload["texto"] for res in resultados])
    return contexto


def gerar_resposta_rag(pergunta: str) -> str:
    print("Buscando contexto no Qdrant...")
    contexto = buscar_contexto(pergunta)

    prompt = f"""Use o contexto abaixo para responder à pergunta. 
Se a resposta não estiver no contexto, diga que não sabe baseado nos dados fornecidos.

Contexto:
{contexto}

Pergunta: {pergunta}
"""
    print("Enviando para a OpenAI...")
    response = cliente_openai.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Você é um assistente útil e preciso."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    pergunta_teste = "When did Beyonce start becoming popular?"
    resposta = gerar_resposta_rag(pergunta_teste)
    print("\n=== Resposta do RAG ===")
    print(resposta)
