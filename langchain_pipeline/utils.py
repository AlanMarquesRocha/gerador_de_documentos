# langchain_pipeline/utils.py
# Bibliotecas para gerar o arquivo em PDF
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import cm
from datetime import datetime
import os

# Cria a pasta generated_docs, caso não exista.
def salvar_contrato_pdf(texto_contrato: str, nome_arquivo: str = None) -> str:
    if not os.path.exists("data/generated_docs"):
        os.makedirs("data/generated_docs")

    if not nome_arquivo:
        nome_arquivo = f"contrato_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    caminho_pdf = os.path.join("data/generated_docs", nome_arquivo)

    # Definição das propriedades do arquivo em PDF de acordo com as normas da ABNT
    doc = SimpleDocTemplate(
        caminho_pdf,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=3 * cm,
        topMargin=3 * cm,
        bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justificado', alignment=4, leading=18, fontSize=12))

    story = []

    # Cabeçalho institucional do documento
    story.append(Paragraph("<b>INSTITUTO ANALYTICS.AI</b>", styles['Title']))
    #story.append(Paragraph("Gerador de Documentos Legais Personalizados", styles['Normal']))
    story.append(Spacer(1, 12))

    # Contrato (formatado por parágrafos)
    for paragrafo in texto_contrato.split('\n\n'):
        story.append(Paragraph(paragrafo.strip().replace('\n', '<br/>'), styles['Justificado']))
        story.append(Spacer(1, 12))

    # Assinaturas
    story.append(Spacer(1, 30))
    story.append(Paragraph("__________________________<br/>Contratante", styles['Normal']))
    story.append(Spacer(1, 30))
    story.append(Paragraph("__________________________<br/>Contratado", styles['Normal']))

    doc.build(story)

    return caminho_pdf
