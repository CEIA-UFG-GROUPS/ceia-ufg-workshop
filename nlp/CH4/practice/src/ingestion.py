import uuid

from datasets import load_dataset
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, PointStruct, VectorParams
from sentence_transformers import SentenceTransformer


def main():
    print("1. Carregando o dataset SQuAD v2 (amostra de 500 linhas para CPU)...")
    # Usamos uma amostra pequena para rodar rápido em fins educacionais
    dataset = load_dataset("squad_v2", split="train[:500]")

    # Extrair contextos únicos para indexar no banco
    contextos_unicos = list(set(dataset["context"]))
    print(f"Total de documentos (contextos) únicos: {len(contextos_unicos)}")

    print("2. Carregando modelo de embeddings na CPU...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("3. Gerando embeddings...")
    embeddings = model.encode(contextos_unicos, show_progress_bar=True)

    print("4. Conectando ao Qdrant e criando coleção...")
    client = QdrantClient(host="localhost", port=6333)
    collection_name = "squad_docs"

    # Recria a coleção se ela já existir
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=384, distance=Distance.COSINE
        ),  # 384 é a dimensão do MiniLM
    )

    print("5. Inserindo dados no banco vetorial...")
    pontos = []
    for i, (texto, vetor) in enumerate(zip(contextos_unicos, embeddings)):
        pontos.append(
            PointStruct(
                id=str(uuid.uuid4()),  # ID único gerado aleatoriamente
                vector=vetor.tolist(),
                payload={"texto": texto},  # Guardamos o texto original no payload
            )
        )

    client.upsert(collection_name=collection_name, points=pontos)
    print("✅ Ingestão concluída com sucesso!")


if __name__ == "__main__":
    main()
