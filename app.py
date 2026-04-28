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

def titulo_pdf(c, texto, y, tamanho=18):
    c.setFont("Helvetica-Bold", tamanho)
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

        # ============================
        # PÁGINA 1 — RESUMO (PARTE 1)
        # ============================
        cabecalho_pdf(c, width, height)
        titulo_pdf(c, "Resumo do Projeto", height - 3.5*cm, 20)

        y = height - 5.2*cm
        d = st.session_state.dados

        c.setFillColor(CINZA)
        c.rect(2*cm, y - 6.8*cm, width - 4*cm, 6.5*cm, fill=1, stroke=0)

        texto_pdf(c, f"Simulado: {d.get('simulado','')}", y, 16)
        texto_pdf(c, f"Etapa: {d.get('etapa','')}", y - 0.9*cm, 16)
        texto_pdf(c, f"Prova: {d.get('prova','')}", y - 1.8*cm, 16)
        texto_pdf(c, f"Volume: {d.get('volume','')}", y - 2.7*cm, 16)
        texto_pdf(c, f"Data de aplicação: {d.get('data','')}", y - 3.6*cm, 16)
        texto_pdf(c, f"Disciplinas: {', '.join(d.get('disciplinas', []))}", y - 4.5*cm, 16)
        texto_pdf(c, f"Redação: {d.get('redacao','')}", y - 5.4*cm, 16)
        texto_pdf(c, f"Miolo: {d.get('miolo','')}", y - 6.3*cm, 16)

        c.showPage()

        # ============================
        # PÁGINA 2 — CHECKLIST TÉCNICO
        # ============================
        cabecalho_pdf(c, width, height)
        titulo_pdf(c, "Checklist Técnico", height - 3.5*cm, 18)

        y = height - 5*cm

        # --- CAPA ---
        titulo_pdf(c, "CAPA", y, 14)
        y -= 1*cm

        capa_itens = [
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

        for item in capa_itens:
            marcado = st.session_state.get(f"capa_{item}", False)
            c.rect(2*cm, y - 0.2*cm, 0.4*cm, 0.4*cm)
            if marcado:
                c.drawString(2.05*cm, y - 0.15*cm, "✔")
            texto_pdf(c, item, y, 11)
            y -= 0.7*cm

        y -= 0.8*cm

        # --- MIOLO ---
        titulo_pdf(c, "MIOLO / DIAGRAMAÇÃO", y, 14)
        y -= 1*cm

        miolo_itens = [
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

        for item in miolo_itens:
            marcado = st.session_state.get(f"miolo_{item}", False)
            c.rect(2*cm, y - 0.2*cm, 0.4*cm, 0.4*cm)
            if marcado:
                c.drawString(2.05*cm, y - 0.15*cm, "✔")
            texto_pdf(c, item, y, 11)
            y -= 0.7*cm

        c.showPage()

        # ============================
        # PÁGINA 3 — CONFERÊNCIA (3 COLUNAS)
        # ============================
        cabecalho_pdf(c, width, height)
        titulo_pdf(c, "Conferência de Conteúdo", height - 3.5*cm, 18)

        y = height - 5*cm
        col_x = [2*cm, width/3 + 0.5*cm, 2*width/3 + 0.5*cm]
        col = 0

        qtd = d.get("qtd", 0)
        inicio = d.get("num_inicial", 1)

        for i in range(qtd):
            numero = inicio + i
            selecionados = st.session_state.get(f"conf_{numero}", [])

            if selecionados:
                x = col_x[col]

                c.setFillColor(AMARELO)
                c.rect(x, y - 0.4*cm, width/3 - 2*cm, 0.8*cm, fill=1, stroke=0)
                c.setFillColor(PRETO)
                c.setFont("Helvetica-Bold", 11)
                c.drawString(x, y, f"Questão {numero}")

                y -= 0.6*cm
                c.setFont("Helvetica", 9)
                for s in selecionados:
                    c.drawString(x + 0.2*cm, y, f"- {s}")
                    y -= 0.35*cm

                y -= 0.6*cm
                col += 1

                if col == 3:
                    col = 0
                    y -= 0.8*cm

                if y < 3*cm:
                    c.showPage()
                    cabecalho_pdf(c, width, height)
                    y = height - 5*cm
                    col = 0

        texto_pdf(
            c,
            f"Documento gerado em {date.today().strftime('%d/%m/%Y')} — {nome_conferente}",
            1.5*cm,
            9,
        )

        c.save()

        with open(pdf_name, "rb") as f:
            st.download_button(
                "📥 Baixar relatório em PDF",
                f,
                file_name=pdf_name,
                mime="application/pdf",
            )
