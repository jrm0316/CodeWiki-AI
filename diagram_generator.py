def gerar_mermaid(imports_encontrados):

    linhas = ["graph TD"]

    for arquivo, imports in imports_encontrados.items():

        origem = arquivo.replace(".py", "")

        for imp in imports:

            linhas.append(
                f"{origem} --> {imp}"
            )

    return "\n".join(linhas)