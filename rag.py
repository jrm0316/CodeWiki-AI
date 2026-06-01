import faiss
import numpy as np
import pickle
import os
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

# =========================
# EMBEDDINGS
# =========================
def gerar_embeddings(textos):
    return model.encode(textos)

# =========================
# CRIAR ÍNDICE
# =========================
def criar_indice(embeddings):
    embeddings = np.array(embeddings).astype("float32")
    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    return index

def buscar(query, textos, index, k=5):
    query_embedding = model.encode([query])
    query_embedding = np.array(
        query_embedding
    ).astype("float32")

    k = min(k, len(textos))

    _, indices = index.search(
        query_embedding,
        k
    )

    return [
        textos[i]
        for i in indices[0]
    ]

# =========================
# CACHE INTELIGENTE (SALVAR)
# =========================
def salvar_cache(index, embeddings, textos):
    faiss.write_index(index, "cache/faiss.index")

    with open("cache/embeddings.pkl", "wb") as f:
        pickle.dump(embeddings, f)

    with open("cache/textos.pkl", "wb") as f:
        pickle.dump(textos, f)

    print("💾 Cache salvo com sucesso!")


# =========================
# CACHE INTELIGENTE (CARREGAR)
# =========================
def carregar_cache():
    if not os.path.exists("cache/faiss.index"):
        return None, None, None

    index = faiss.read_index("cache/faiss.index")

    with open("cache/embeddings.pkl", "rb") as f:
        embeddings = pickle.load(f)

    with open("cache/textos.pkl", "rb") as f:
        textos = pickle.load(f)

    print("📦 Cache carregado!")

    return index, embeddings, textos