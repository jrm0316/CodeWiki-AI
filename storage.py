import faiss
import pickle

def salvar_documentos(caminho, documentos):
    with open(caminho, "wb") as f:
        pickle.dump(documentos, f)

def carregar_documentos(caminho):
    with open(caminho, "rb") as f:
        return pickle.load(f)

def salvar_indice(caminho, index):
    faiss.write_index(
        index,
        caminho
    )

def carregar_indice(caminho):
    return faiss.read_index(
        caminho
    )