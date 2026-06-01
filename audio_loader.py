#import whisper
import re
import os

model = whisper.load_model("base")


def limpar_texto(texto):

    texto = texto.replace("\n", " ")

    texto = re.sub(r"\s+", " ", texto)

    return texto.strip()

def dividir_texto_segmentos(segmentos, max_palavras=120):

    chunks = []

    texto_atual = []

    inicio = None

    fim = None

    total_palavras = 0

    for seg in segmentos:

        texto = limpar_texto(seg["text"])

        palavras = texto.split()

        if inicio is None:

            inicio = seg["start"]

        fim = seg["end"]

        texto_atual.append(texto)

        total_palavras += len(palavras)

        # =========================
        # FECHA CHUNK
        # =========================

        if total_palavras >= max_palavras:

            chunks.append({
                "texto": " ".join(texto_atual),
                "inicio": inicio,
                "fim": fim
            })

            texto_atual = []

            total_palavras = 0

            inicio = None

    # =========================
    # ÚLTIMO CHUNK
    # =========================

    if texto_atual:

        chunks.append({
            "texto": " ".join(texto_atual),
            "inicio": inicio,
            "fim": fim
        })

    return chunks


def carregar_audio(caminho_audio):

    nome_arquivo = os.path.basename(caminho_audio)

    nome_sem_extensao = os.path.splitext(nome_arquivo)[0]

    caminho_txt = f"transcricoes/{nome_sem_extensao}.txt"

    # =========================
    # CACHE TXT
    # =========================

    if os.path.exists(caminho_txt):

        print(f"\n📄 Carregando transcrição salva: {caminho_txt}")

        with open(caminho_txt, "r", encoding="utf-8") as f:

            texto = f.read()

        chunks = [{
            "texto": texto,
            "inicio": 0,
            "fim": 0,
            "arquivo": caminho_audio
        }]

        return chunks

    # =========================
    # TRANSCRIÇÃO
    # =========================

    print("\n🎤 Transcrevendo áudio...")

    resultado = model.transcribe(caminho_audio)

    texto_completo = resultado["text"]

    # =========================
    # SALVAR TXT
    # =========================

    os.makedirs("transcricoes", exist_ok=True)
    with open(caminho_txt, "w", encoding="utf-8") as f:

        f.write(texto_completo)

    print(f"\n✅ Transcrição salva em: {caminho_txt}")

    segmentos = resultado["segments"]

    partes = dividir_texto_segmentos(segmentos)

    chunks = []

    for parte in partes:

        chunks.append({
            "texto": parte["texto"],
            "inicio": parte["inicio"],
            "fim": parte["fim"],
            "arquivo": caminho_audio
        })

    return chunks