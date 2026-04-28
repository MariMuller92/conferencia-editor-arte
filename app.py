import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.units import cm
from datetime import date
import os

# ==================================================
# CONFIGURAÇÃO GERAL
# ==================================================
st.set_page_config(
    page_title="Conferência Editor de Arte",
    layout="wide",
)

AZUL = HexColor("#1B2D6B")
AMARELO = HexColor("#FFF3B0")
CINZA = HexColor("#F2F2F2")
PRETO = HexColor("#000000")

LOGO_PATH = "logo_bernoulli.png"

# ==================================================
# FUNÇÕES PDF
# ==================================================
def cabecalho_pdf(c, width, height):
    # tarja superior fina
    c.setFillColor(AZUL)
    c.rect(0, height - 1*cm, width, 0.35*cm, fill=1, stroke=0)

    # logo no canto superior direito
    if os.path.exists(LOGO_PATH):
        c.drawImage(
            LOGO_PATH,
            width - 6.5*cm,
            height - 1.8*cm,
            width=5.5*cm,
            preserveAspectRatio=True,
            mask="auto",
        )

    # tarja inferior fina
    c.rect(0, 0.6*cm, width, 0.3*cm, fill=1, stroke=0)

def titulo_pdf(c, texto, y):
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(AZUL)
    c.drawString(2*cm, y, texto)

def texto_pdf(c, texto, y, size=10):
    c.setFont("Helvetica", size)
    c.setFillColor(PRETO)
    c.drawString(2.2*cm, y, texto)

def nova_pagina(c, y, height):
    if y < 3*cm:
        c.showPage()
        cabecalho_pdf(c, width, height)
        return height - 3*cm
    return y

# ==================================================
# ESTADO GLOBAL
# ==================================================
if "dados" not in st.session_state:
    st.session_state.dados = {}

# ==================================================
# TÍTULO
# ==================================================
st.title("📘 Conferência Editor de Arte")

# ==================================================
# NAVEGAÇÃO
# ==================================================
pagina = st.sidebar.radio(
    "Etapas da Conferência",
    [
        "Parte 1 — Cadastro",
        "Parte 2 — Checklist Técnico",
        "Parte 3 — Conferência de Conteúdo",
        "Relatório",
    ],
)

# ==================================================
# PARTE 1 — CADASTRO
# ==================================================
if pagina == "Parte 1 — Cadastro":
    st.header("🔰 Cadastro do Projeto")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.session_state.dados["simulado"] = st.text_input("Nome do Simulado")
        st.session_state.dados["etapa"] = st.text_input("Etapa")
        st.session_state.dados["volume"] = st.text_input("Volume")
        st.session_state.dados["prova"] = st.text_input("Prova")

    with col2:
        data = st.date_input("Data de aplicação")
        st.session_state.dados["data"] = data.strftime("%d/%m/%Y")

        st.session_state.dados["num_inicial"] = st.number_input(
            "Numeração inicial das questões",
            min_value=1,
            step=1,
        )

        st.session_state.dados["qtd"] = st.number_input(
            "Quantidade de questões",
            min_value=1,
            step=1,
        )

    with col3:
        st.session_state.dados["disciplinas"] = st.multiselect(
            "Disciplinas",
            [
                "Ciências Humanas",
                "Ciências da Natureza",
                "Língua Estrangeira",
                "Língua Portuguesa",
                "Matemática",
            ],
        )

        st.session_state.dados["redacao"] = st.radio(
            "Tem redação?",
            ["Sim", "Não"],
        )

        st.session_state.dados["codigo_barras"] = st.text_input(
            "Código de barras"
        )

        st.session_state.dados["miolo"] = st.radio(
            "Miolo",
            ["Preto e Branco", "Colorido"],
        )

    st.success("✅ Dados salvos automaticamente")

# ==================================================
# PARTE 2 — CHECKLIST TÉCNICO
# ==================================================
elif pagina == "Parte 2 — Checklist Técnico":
    st.header("✅ Checklist Técnico")

    st.subheader("CAPA")
    capa = [
        "Código de barras correto",
        "Data de aplicação",
        "Disciplinas",
        "Nome do simulado",
        "Prova",
        "Volume",
        "Cor da capa",
        "Código da prova correto",
        "Orientações de acordo",
    ]

    for item in capa:
        col1, col2 = st.columns([1, 6])
        with col1:
            st.checkbox("", key=f"capa_{item}")
        with col2:
            st.text_input(item, key=f"corr_capa_{item}")

    st.divider()

    st.subheader("MIOLO / DIAGRAMAÇÃO")
    miolo = [
        "Paginação",
        "Cabeçalho e rodapé",
        "Arquivo múltiplo de 4",
        "Arquivo em alta",
        "Quantidade de questões",
        "Numeração das questões",
        "Código da questão oculto no PDF",
        "Questões de duas colunas com linha divisória",
        "Questões de uma coluna sem linha divisória",
        "Folha de rascunho",
        "Contracapa fechando a prova",
    ]

    for item in miolo:
        col1, col2 = st.columns([1, 6])
        with col1:
            st.checkbox("", key=f"miolo_{item}")
        with col2:
            st.text_input(item, key=f"corr_miolo_{item}")

# ==================================================
# PARTE 3 — CONFERÊNCIA DE CONTEÚDO
# ==================================================
elif pagina == "Parte 3 — Conferência de Conteúdo":
    st.header("🧠 Conferência de Conteúdo")

    qtd = st.session_state.dados.get("qtd", 0)
    inicio = st.session_state.dados.get("num_inicial", 1)

    itens_conferencia = [
        "Fragmentação",
        "Viúva",
        "Bplay",
        "Referência",
        "Alternativas (A–E)",
        "Ponto final",
        "Imagem legível e em boa qualidade",
        "Poema centralizado e justificado à esquerda",
        "Música centralizada",
        "Expressões math type corretas",
        "Padrões química",
    ]

    for i in range(qtd):
        numero = inicio + i
        st.subheader(f"Questão {numero}")

        colA, colB = st.columns([3, 2])

        with colA:
            st.markdown("**Conferência**")
            st.multiselect(
                "Itens conferidos",
                itens_conferencia,
                key=f"conf_{numero}",
            )

        with colB:
            st.markdown("**Correção**")
            st.radio(
                "Houve correção?",
                ["Não", "Sim"],
                horizontal=True,
                key=f"corrigido_{numero}",
            )
            st.text_area(
                "O que foi feito",
                key=f"desc_{numero}",
            )

        st.markdown("---")

# ==================================================
# RELATÓRIO — PDF
# ==================================================
elif pagina == "Relatório":
    st.header("📄 Relatório Final")

    nome_conferente = st.text_input("Nome de quem realizou a conferência")

    if st.button("Gerar PDF"):
        pdf_name = "relatorio_conferencia_editor_arte.pdf"
        c = canvas.Canvas(pdf_name, pagesize=A4)
        width, height = A4

        # -------- RESUMO --------
        cabecalho_pdf(c, width, height)
        titulo_pdf(c, "Resumo da Conferência", height - 3*cm)

        y = height - 4.5*cm
        d = st.session_state.dados

        c.setFillColor(CINZA)
        c.rect(2*cm, y - 3.2*cm, width - 4*cm, 3*cm, fill=1, stroke=0)

        texto_pdf(c, f"Simulado: {d.get('simulado','')}", y)
        texto_pdf(c, f"Etapa: {d.get('etapa','')}", y - 0.5*cm)
        texto_pdf(c, f"Prova: {d.get('prova','')}", y - 1*cm)
        texto_pdf(c, f"Volume: {d.get('volume','')}", y - 1.5*cm)
        texto_pdf(c, f"Data de aplicação: {d.get('data','')}", y - 2*cm)
        texto_pdf(c, f"Disciplinas: {', '.join(d.get('disciplinas', []))}", y - 2.5*cm)

        c.showPage()

        # -------- CONTEÚDO --------
        cabecalho_pdf(c, width, height)
        titulo_pdf(c, "Conferência de Conteúdo", height - 3*cm)
        y = height - 4.5*cm

        for i in range(d.get("qtd", 0)):
            numero = d.get("num_inicial", 1) + i
            selecionados = st.session_state.get(f"conf_{numero}", [])

            if selecionados:
                c.setFillColor(AMARELO)
                c.rect(2*cm, y - 0.3*cm, width - 4*cm, 0.7*cm, fill=1, stroke=0)

                texto_pdf(c, f"Questão {numero}", y)
                y -= 0.8*cm

                for s in selecionados:
                    texto_pdf(c, f"- {s}", y)
                    y -= 0.4*cm

                texto_pdf(
                    c,
                    f"Corrigido: {st.session_state.get(f'corrigido_{numero}','Não')}",
                    y,
                )
                y -= 0.4*cm

                desc = st.session_state.get(f"desc_{numero}", "")
                if desc:
                    texto_pdf(c, f"O que foi feito: {desc}", y)
                    y -= 0.6*cm

                y = nova_pagina(c, y, height)

        texto_pdf(
            c,
            f"Documento gerado em {date.today().strftime('%d/%m/%Y')} por {nome_conferente}",
            1.5*cm,
            size=9,
        )

        c.save()

        with open(pdf_name, "rb") as f:
            st.download_button(
                "📥 Baixar relatório em PDF",
                f,
                file_name=pdf_name,
                mime="application/pdf",
            )
