import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.units import cm
from datetime import date
import os

# ==========================
# CONFIG STREAMLIT
# ==========================
st.set_page_config(
    page_title="Conferência Editor de Arte",
    layout="wide"
)

# ==========================
# CORES INSTITUCIONAIS
# ==========================
AZUL = HexColor("#1B2D6B")
VERDE = HexColor("#00A98F")
CINZA = HexColor("#F2F2F2")
PRETO = HexColor("#000000")

LOGO_PATH = "logo_bernoulli.png"

# ==========================
# FUNÇÕES PDF
# ==========================
def cabecalho_pdf(c, width, height):
    c.setFillColor(AZUL)
    c.rect(0, height - 3*cm, width, 3*cm, fill=1, stroke=0)

    if os.path.exists(LOGO_PATH):
        c.drawImage(
            LOGO_PATH,
            1.5*cm,
            height - 2.4*cm,
            width=6*cm,
            preserveAspectRatio=True,
            mask="auto"
        )

def titulo_pdf(c, texto, y):
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(AZUL)
    c.drawString(2*cm, y, texto)

def subtitulo_pdf(c, texto, y):
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(VERDE)
    c.drawString(2*cm, y, texto)

def texto_pdf(c, texto, y, tamanho=10):
    c.setFont("Helvetica", tamanho)
    c.setFillColor(PRETO)
    c.drawString(2.2*cm, y, texto)

def nova_pagina_se_preciso(c, y, height):
    if y < 3*cm:
        c.showPage()
        cabecalho_pdf(c, width, height)
        return height - 4*cm
    return y

# ==========================
# APP
# ==========================
st.title("📘 Conferência Editor de Arte")

# ---------- PARTE 1 ----------
st.header("🔰 Parte 1 — Cadastro do Projeto")

col1, col2, col3 = st.columns(3)

with col1:
    nome_simulado = st.text_input("Nome do Simulado")
    etapa = st.text_input("Etapa")
    volume = st.text_input("Volume")
    prova = st.text_input("Prova")

with col2:
    data_aplicacao = st.date_input("Data de aplicação")
    qtd_questoes = st.number_input("Quantidade de questões", min_value=1, step=1)
    disciplinas = st.text_input("Disciplinas")

with col3:
    inicio_numeracao = st.number_input("Numeração das questões começa em", min_value=1, step=1)
    tem_redacao = st.radio("Tem redação?", ["Sim", "Não"])
    codigo_barras = st.text_input("Código de barras")
    miolo_cor = st.radio("Miolo", ["Preto e Branco", "Colorido"])

# ---------- PARTE 2 ----------
st.header("✅ Parte 2 — Checklist Técnico")

checklist = {
    "Capa": [
        "Código de barras correto",
        "Data de aplicação",
        "Disciplina",
        "Nome do simulado",
        "Volume de aplicação",
        "Cor da capa",
        "Código da prova correto",
        "Orientações de acordo",
    ],
    "Miolo / Diagramação": [
        "Paginação",
        "Cabeçalho e rodapé",
        "Arquivo múltiplo de 4",
        "Arquivo em alta com marca de corte",
        "Quantidade de questões",
        "Numeração das questões",
        "Código da questão oculto no PDF",
        "Questões de duas colunas com linha divisória",
        "Questões de uma coluna sem linha divisória",
        "Folha de rascunho da redação",
        "Contracapa fechando a prova",
    ]
}

checklist_resultados = []

for bloco, itens in checklist.items():
    st.subheader(bloco)
    for item in itens:
        if item == "Folha de rascunho da redação" and tem_redacao == "Não":
            continue

        c1, c2, c3 = st.columns([1, 4, 6])
        with c1:
            ok = st.checkbox("", key=f"{bloco}-{item}")
        with c2:
            st.write(item)
        with c3:
            correcao = st.text_input("Correção", key=f"corr-{bloco}-{item}")

        checklist_resultados.append((bloco, item, ok, correcao))

# ---------- PARTE 3 ----------
st.header("🧠 Parte 3 — Conferência de Conteúdo")

itens_conteudo = [
    "Fragmentação",
    "Viúva",
    "Bplay",
    "Referência",
    "Alternativas (A–E)",
    "Ponto final",
    "Imagem legível e em boa qualidade",
    "Poema centralizado e justificado à esquerda",
    "Música centralizada",
    "Expressões MathType corretas",
    "Padrões de química",
]

conferencias = []

for i in range(int(qtd_questoes)):
    numero = inicio_numeracao + i
    with st.expander(f"Questão {numero}"):
        marcados = [item for item in itens_conteudo if st.checkbox(item, key=f"{numero}-{item}")]
        corrigido = st.radio("Corrigido?", ["Sim", "Não"], key=f"corrigido-{numero}")
        descricao = st.text_area("O que foi feito", key=f"desc-{numero}")

        conferencias.append((numero, marcados, corrigido, descricao))

# ---------- PDF ----------
st.header("📄 Gerar Relatório")
nome_conferente = st.text_input("Nome de quem realizou a conferência")

if st.button("Gerar PDF"):
    pdf_name = "relatorio_conferencia_editor_arte.pdf"
    c = canvas.Canvas(pdf_name, pagesize=A4)
    width, height = A4

    # CAPA
    cabecalho_pdf(c, width, height)

    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(AZUL)
    c.drawString(2*cm, height - 5*cm, "Relatório de Conferência")

    y = height - 7*cm
    dados = [
        f"Simulado: {nome_simulado}",
        f"Etapa: {etapa}",
        f"Volume: {volume}",
        f"Prova: {prova}",
        f"Disciplinas: {disciplinas}",
        f"Data de aplicação: {data_aplicacao}",
        f"Quantidade de questões: {qtd_questoes}",
        f"Numeração inicial: {inicio_numeracao}",
        f"Redação: {tem_redacao}",
        f"Código de barras: {codigo_barras}",
        f"Miolo: {miolo_cor}",
        f"Emitido em: {date.today()}",
        f"Conferente: {nome_conferente}",
    ]

    for d in dados:
        texto_pdf(c, d, y)
        y -= 0.6*cm

    c.showPage()

    # CHECKLIST
    cabecalho_pdf(c, width, height)
    titulo_pdf(c, "Checklist Técnico", height - 4.5*cm)
    y = height - 6*cm

    for bloco, item, ok, correcao in checklist_resultados:
        if ok:
            c.setFillColor(CINZA)
            c.rect(2*cm, y - 0.3*cm, width - 4*cm, 0.8*cm, fill=1, stroke=0)
            c.setFont("Helvetica-Bold", 10)
            c.setFillColor(AZUL)
            c.drawString(2.2*cm, y, f"{bloco} — {item}")
            c.setFont("Helvetica", 9)
            c.drawString(11*cm, y, correcao)
            y -= 1*cm
            y = nova_pagina_se_preciso(c, y, height)

    c.showPage()

    # CONTEÚDO
    cabecalho_pdf(c, width, height)
    titulo_pdf(c, "Conferência de Conteúdo", height - 4.5*cm)
    y = height - 6*cm

    for numero, itens, corrigido, descricao in conferencias:
        if itens or corrigido == "Sim":
            subtitulo_pdf(c, f"Questão {numero}", y)
            y -= 0.6*cm
            for i in itens:
                texto_pdf(c, f"- {i}", y)
                y -= 0.4*cm
            texto_pdf(c, f"Corrigido: {corrigido}", y)
            y -= 0.4*cm
            if descricao:
                texto_pdf(c, f"O que foi feito: {descricao}", y)
                y -= 0.6*cm
            c.setStrokeColor(VERDE)
            c.line(2*cm, y, width - 2*cm, y)
            y -= 1*cm
            y = nova_pagina_se_preciso(c, y, height)

    c.save()

    with open(pdf_name, "rb") as f:
        st.download_button("📥 Baixar relatório em PDF", f, file_name=pdf_name, mime="application/pdf")
