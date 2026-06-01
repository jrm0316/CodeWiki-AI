import ast
import os

def extrair_blocos_python(codigo):
    blocos = []
    try:
        tree = ast.parse(codigo)
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                bloco = ast.get_source_segment(
                    codigo,
                    node
                )
                blocos.append({
                    "tipo": "funcao",
                    "nome": node.name,
                    "conteudo": bloco
                })
            elif isinstance(node, ast.ClassDef):
                bloco = ast.get_source_segment(
                    codigo,
                    node
                )
                blocos.append({
                    "tipo": "classe",
                    "nome": node.name,
                    "conteudo": bloco
                })
    except Exception as e:
        print(e)
    if len(blocos) == 0:
        blocos.append({
            "tipo": "arquivo",
            "nome": "codigo_completo",
            "conteudo": codigo
        })
    return blocos

def extrair_imports(codigo):
    imports = []
    try:
        tree = ast.parse(codigo)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
    except Exception as e:
        print(e)
    return imports

def mapa_dependencias(python_files):

    resultado = {}

    for file in python_files:

        imports = extrair_imports(
            file["content"]
        )

        resultado[
            os.path.basename(
                file["path"]
            )
        ] = imports

    return resultado