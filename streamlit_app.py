import streamlit as st
import os
import zipfile
import pickle

from llm import (
    responder,
    resumir_projeto,
    documentar_codigo,
    explicar_arquitetura,
    gerar_readme
)

from code_parser import (
    extrair_blocos_python,
    extrair_imports,
    mapa_dependencias
)

from dependency_analyzer import (
    buscar_referencias,
    mapa_chamadas,
    detectar_codigo_morto
)
# =========================
# CONFIG
# =========================
from rag import (
    gerar_embeddings,
    criar_indice,
    buscar
)
from storage import (
    salvar_documentos,
    carregar_documentos,
    salvar_indice,
    carregar_indice
)
from pdf_generator import (
    gerar_pdf
)
from diagram_generator import (
    gerar_mermaid
)
st.set_page_config(page_title="CodeWiki AI")
st.title("💻 CodeWiki AI")

def titulo(texto):
    st.markdown(
        f"<h5>{texto}</h5>",
        unsafe_allow_html=True
    )
# =========================
# UPLOAD
# =========================
uploaded_file = st.file_uploader(
    "Upload do projeto ZIP",
    type=["zip"]
)
codigo_files = []
if uploaded_file is not None:
    st.success("Projeto enviado com sucesso!")
UPLOAD_FOLDER = "uploads"
INDEX_FOLDER = "indexes"
os.makedirs(
    INDEX_FOLDER,
    exist_ok=True
)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
projetos_salvos = []
for arquivo in os.listdir(INDEX_FOLDER):
    if arquivo.endswith(".faiss"):
        projetos_salvos.append(
            arquivo.replace(".faiss", "")
        )
st.sidebar.subheader(
    "📂 Projetos Processados"
)
projeto_selecionado = st.sidebar.selectbox(
    "Escolha um projeto",
    ["Nenhum"] + projetos_salvos
)
if projeto_selecionado != "Nenhum":
    docs_path = os.path.join(
        INDEX_FOLDER,
        f"{projeto_selecionado}_docs.pkl"
    )
    index_path = os.path.join(
        INDEX_FOLDER,
        f"{projeto_selecionado}.faiss"
    )
    st.session_state["documents"] = (
        carregar_documentos(docs_path)
    )
    st.session_state["index"] = (
        carregar_indice(index_path)
    )
    st.success(
        f"{projeto_selecionado} carregado!"
    )
if uploaded_file is not None:
    zip_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(zip_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Projeto salvo em: {zip_path}")
    extract_folder = os.path.join(
        UPLOAD_FOLDER,
        uploaded_file.name.replace(".zip", "")
    )
    os.makedirs(extract_folder, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)
    st.success(f"Projeto extraído em: {extract_folder}")
    codigo_files = []
    for root, dirs, files in os.walk(extract_folder):
        dirs[:] = [
            d for d in dirs
            if d not in [
                "venv",
                "__pycache__",
                ".git",
                "node_modules"
            ]
        ]
        for file in files:

            if file.endswith(
                (
                    ".py",
                    ".go",
                    ".js",
                    ".ts",
                    ".java",
                    ".cs"
                )
            ):

                full_path = os.path.join(
                    root,
                    file
                )

                with open(
                    full_path,
                    "r",
                    encoding="utf-8",
                    errors="ignore"
                ) as f:

                    content = f.read()

                codigo_files.append({
                    "path": full_path,
                    "content": content
                })

col1, col2 = st.columns([3,2]) #Duas colunas
with col1:
    titulo("📂 Arquivos Python encontrados")
    st.write(len(codigo_files))
    titulo("🗺️ Estrutura do Projeto")
    for file in codigo_files:
        st.write(
            os.path.relpath(
                file["path"],
                extract_folder
            )
        )
    titulo(
        "📦 Dependências do Projeto"
    )
    dependencias = mapa_dependencias(
        codigo_files
    )
    for arquivo, imports in dependencias.items():
        st.write(f"📄 {arquivo}")
        for imp in imports:
            st.write(f" └── {imp}")
    documents = []
    imports_encontrados = {}
    arquivos_projeto = set()
    for file in codigo_files:

        nome = os.path.basename(
            file["path"]
        ).replace(".py", "")
        arquivos_projeto.add(nome)
    for file in codigo_files:
        imports = extrair_imports(
            file["content"]
        )
        imports_encontrados[
            os.path.basename(file["path"])
        ] = imports
        blocos = extrair_blocos_python(
            file["content"]
        )
        for bloco in blocos:
            documents.append({
                "path": file["path"],
                "tipo": bloco["tipo"],
                "nome": bloco["nome"],
                "content": bloco["conteudo"]
            })
        st.write(file["path"])
    titulo("📦 Chunks criados")
    st.write(len(documents))
    titulo("🧠 Blocos encontrados")
    for doc in documents:
        st.write(
            f'{doc["tipo"]}: {doc["nome"]}'
        )

    # =========================
    # VISÃO GERAL DO PROJETO
    # =========================
    if st.button(
        "📋 Gerar Visão Geral do Projeto"
    ):
        contexto_projeto = "\n\n".join([
            doc["content"]
            for doc in documents
        ])
        with st.spinner(
            "Analisando projeto..."
        ):
            resumo = resumir_projeto(
                contexto_projeto
            )
        titulo(
            "📋 Visão Geral do Projeto"
        )
        st.write(resumo)
    texts = [
        doc["content"]
        for doc in documents
    ]
    # =========================
    # MAPA DE CHAMADAS
    # =========================
    titulo(
        "🕸️ Mapa de Chamadas"
    )
    chamadas = mapa_chamadas(
        codigo_files
    )
    for arquivo, itens in chamadas.items():
        st.write(
            f"📄 {os.path.basename(arquivo)}"
        )
        for item in itens[:10]:
            st.code(item)


    # =========================
    # NAVEGAÇÃO ENTRE FUNÇÕES
    # =========================

    titulo(
        "🧭 Navegação entre Funções"
    )

    funcoes = [
        doc
        for doc in documents
        if doc["tipo"] == "funcao"
    ]

    nomes_funcoes = [
        f["nome"]
        for f in funcoes
    ]

    if nomes_funcoes:

        funcao_selecionada = st.selectbox(
            "Escolha uma função",
            nomes_funcoes
        )

        funcao = next(
            f
            for f in funcoes
            if f["nome"] == funcao_selecionada
        )

        st.markdown(
            f"### 📌 {funcao['nome']}"
        )

        st.code(
            funcao["content"],
            language="python"
        )
        if st.button(
            f"📚 Documentar {funcao['nome']}",
            key=f"nav_doc_{funcao['nome']}"
        ):

            documentacao = documentar_codigo(
                funcao["content"]
            )

            st.markdown(documentacao)
            if st.button(
                f"🔍 Referências de {funcao['nome']}",
                key=f"nav_ref_{funcao['nome']}"
            ):

                refs = buscar_referencias(
                    funcao["nome"],
                    codigo_files
                )

                st.write(
                    f"Referências encontradas: {len(refs)}"
                )

                for ref in refs:

                    st.write(
                        f"📄 {os.path.basename(ref['arquivo'])}"
                    )

                    st.code(
                        ref["conteudo"]
                    )
with col2:
    # =========================
    # IMPORTS ENCONTRADOS
    # =========================
    titulo("🔗 Dependências Encontradas")
    for arquivo, imports in imports_encontrados.items():
        st.write(f"📄 {arquivo}")
        internos = []
        externos = []
        for imp in imports:
            if imp in arquivos_projeto:
                internos.append(imp)
            else:
                externos.append(imp)
        if internos:
            st.write("🔗 Projeto")
            for item in internos:
                st.write(f"↳ {item}.py")
        if externos:
            st.write("🌎 Externos")
            for item in externos:
                st.write(f"↳ {item}")
    if st.button("⚙️ Gerar embeddings"):
        with st.spinner("🧠 Gerando embeddings..."):
            st.write("Quantidade de documentos:", len(documents))
            st.write("Quantidade de textos:", len(texts))
            embeddings = gerar_embeddings(texts)
            st.write("Shape embeddings:", embeddings.shape)
        st.success("Embeddings gerados!")
        with st.spinner("📦 Criando índice FAISS..."):
            index = criar_indice(embeddings)
        st.success("Índice criado!")
        st.session_state["documents"] = documents
        st.session_state["index"] = index
        project_name = uploaded_file.name.replace(
            ".zip",
            ""
        )

        docs_path = os.path.join(
            INDEX_FOLDER,
            f"{project_name}_docs.pkl"
        )

        salvar_documentos(
            docs_path,
            documents
        )
        index_path = os.path.join(
            INDEX_FOLDER,
            f"{project_name}.faiss"
        )

        salvar_indice(
            index_path,
            index
        )

        st.success(
            "Índice FAISS salvo!"
        )

        st.success(
            "Documentos salvos em disco!"
        )

    if "documents" in st.session_state:

        if st.button("📄 Gerar README"):

            contexto = "\n\n".join([
                doc["content"]
                for doc in st.session_state["documents"]
            ])

            with st.spinner(
                "Gerando documentação..."
            ):

                readme = gerar_readme(
                    contexto
                )

            titulo(
                "README Gerado"
            )

            st.markdown(readme)
            arquivo_md = "README.md"

            with open(
                arquivo_md,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(readme)

            st.download_button(
                label="💾 Baixar README.md",
                data=readme,
                file_name="README.md",
                mime="text/markdown"
            )

    # =========================
    # FLUXOGRAMA DO PROJETO
    # =========================

    titulo(
        "🕸️ Fluxograma do Projeto"
    )

    for arquivo, imports in imports_encontrados.items():

        st.markdown(
            f"### 📄 {arquivo}"
        )

        for imp in imports:

            st.write(
                f"└── {imp}"
            )

    # =========================
    # RELAÇÕES ENTRE ARQUIVOS
    # =========================

    titulo(
        "🔄 Relações Entre Arquivos"
    )

    for arquivo, imports in imports_encontrados.items():

        internos = [
            imp
            for imp in imports
            if imp in arquivos_projeto
        ]

        if internos:

            st.write(f"📄 {arquivo}")

            for imp in internos:

                st.write(
                    f" └── {imp}.py"
                )

    # =========================
    # DIAGRAMA MERMAID
    # =========================

    titulo(
        "📊 Diagrama Mermaid"
    )

    if st.button(
        "📊 Gerar Diagrama"
    ):

        mermaid = gerar_mermaid(
            imports_encontrados
        )

        st.code(
            mermaid,
            language="text"
        )

    # =========================
    # ARQUITETURA
    # =========================

    if "documents" in st.session_state:

        titulo(
            "🏗️ Arquitetura do Projeto"
        )

        if st.button(
            "🏗️ Explicar Arquitetura"
        ):

            contexto_projeto = "\n\n".join([
                doc["content"]
                for doc in st.session_state["documents"]
            ])

            with st.spinner(
                "Analisando arquitetura..."
            ):

                arquitetura = explicar_arquitetura(
                    contexto_projeto
                )

                st.write(arquitetura)

                st.download_button(
                    label="💾 Baixar Arquitetura.md",
                    data=arquitetura,
                    file_name="arquitetura.md",
                    mime="text/markdown"
                )

    # =========================
    # EXPORTAR PDF
    # =========================

    if "documents" in st.session_state:

        titulo(
            "📄 Exportar Relatório PDF"
        )

        if st.button(
            "📄 Gerar PDF"
        ):

            contexto = "\n\n".join([
                doc["content"]
                for doc in st.session_state["documents"]
            ])

            with st.spinner(
                "Gerando relatório..."
            ):

                resumo = resumir_projeto(
                    contexto
                )

                pdf_path = "relatorio_projeto.pdf"

                gerar_pdf(
                    pdf_path,
                    "Relatório do Projeto",
                    resumo
                )

            with open(
                pdf_path,
                "rb"
            ) as pdf_file:

                st.download_button(
                    label="💾 Baixar PDF",
                    data=pdf_file,
                    file_name="relatorio_projeto.pdf",
                    mime="application/pdf"
                )

    # =========================
    # CÓDIGO MORTO
    # =========================

    titulo(
        "☠️ Código Possivelmente Morto"
    )

    if st.button(
        "☠️ Analisar Código Morto"
    ):

        mortas = detectar_codigo_morto(
            documents,
            codigo_files
        )

        st.write(
            f"Funções encontradas: {len(mortas)}"
        )

        for funcao in mortas:

            st.write(
                f"⚠️ {funcao}"
            )
            
    # =========================
    # CHAT
    # =========================
    if "index" in st.session_state:
        pergunta = st.text_input(
            "💬 Faça uma pergunta sobre o código"
        )
        if pergunta:
            resultados = buscar(
                pergunta,
                st.session_state["documents"],
                st.session_state["index"]
            )
            contexto = "\n".join([
                r["content"]
                for r in resultados
            ])
            resposta = responder(
                pergunta,
                contexto
            )
            titulo("🧠 Resposta")
            st.write(resposta)

            titulo("📂 Arquivos relacionados")

            arquivos = set()

            for r in resultados:
                arquivos.add(r["path"])

            for arquivo in arquivos:
                st.write(arquivo)

            titulo("🔎 Trechos encontrados")
            st.write(
                "Resultados encontrados:",
                len(resultados)
            )

            for r in resultados:

                st.markdown(
                    f"""
            **Tipo:** {r.get('tipo', 'desconhecido')}

            **Nome:** {r.get('nome', 'desconhecido')}

            **Arquivo:** {os.path.basename(r['path'])}
            """
                )

                st.code(
                    r["content"],
                    language="python"
                )
                if r.get("tipo") in ["funcao", "classe"]:
                    if st.button(
                        f"📚 Documentar {r['nome']}",
                        key=f"doc_{r['nome']}"
                    ):

                        doc = documentar_codigo(
                            r["content"]
                        )

                        st.markdown(doc)

                if r.get("tipo") == "funcao":

                    if st.button(
                        f"🔍 Onde {r['nome']} é usada?",
                        key=f"ref_{r['nome']}"
                    ):

                        refs = buscar_referencias(
                            r["nome"],
                            codigo_files
                        )

                        st.write(
                            "Encontrada em:"
                        )

                        for ref in refs:
                            st.write(
                                f"📄 {os.path.basename(ref['arquivo'])}"
                            )

                            st.write(
                                f"Linha: {ref['linha']}"
                            )

                            st.code(
                                ref["conteudo"]
                            )
    # =========================
    # BUSCAR REFERÊNCIAS
    # =========================

    titulo(
        "🔍 Buscar Referências"
    )

    nome_referencia = st.text_input(
        "Função, classe ou variável"
    )

    if nome_referencia:

        referencias = buscar_referencias(
            nome_referencia,
            codigo_files
        )

        st.write(
            f"Referências encontradas: {len(referencias)}"
        )

        for ref in referencias:

            st.markdown(
                f"""
    **Arquivo:** {os.path.basename(ref["arquivo"])}

    **Linha:** {ref["linha"]}
    """
            )

            st.code(ref["conteudo"])