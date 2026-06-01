import os
import ast

def buscar_referencias(nome, python_files):

    resultados = []

    for file in python_files:

        linhas = file["content"].split("\n")

        for numero, linha in enumerate(
            linhas,
            start=1
        ):

            if nome in linha:

                resultados.append({
                    "arquivo": file["path"],
                    "linha": numero,
                    "conteudo": linha.strip()
                })

    return resultados

def mapa_chamadas(python_files):

    resultado = {}

    for file in python_files:

        chamadas = []

        linhas = file["content"].split("\n")

        for linha in linhas:

            linha = linha.strip()

            if "(" in linha and ")" in linha:

                chamadas.append(linha)

        resultado[file["path"]] = chamadas

    return resultado

def detectar_codigo_morto(
    documents,
    python_files
):

    funcoes = []

    for doc in documents:

        if doc["tipo"] == "funcao":

            funcoes.append(
                doc["nome"]
            )

    mortas = []

    for funcao in funcoes:

        usada = False

        for file in python_files:

            conteudo = file["content"]

            ocorrencias = conteudo.count(
                funcao
            )

            if ocorrencias > 1:

                usada = True
                break

        if not usada:

            mortas.append(
                funcao
            )

    return mortas