from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def gerar_pdf(
    arquivo_saida,
    titulo,
    conteudo
):

    doc = SimpleDocTemplate(
        arquivo_saida
    )

    styles = getSampleStyleSheet()

    elementos = []

    elementos.append(
        Paragraph(
            titulo,
            styles["Title"]
        )
    )

    elementos.append(
        Spacer(1, 12)
    )

    elementos.append(
        Paragraph(
            conteudo.replace(
                "\n",
                "<br/>"
            ),
            styles["BodyText"]
        )
    )

    doc.build(elementos)