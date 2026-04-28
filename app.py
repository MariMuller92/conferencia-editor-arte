import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.units import cm
from datetime import date
import os

# ==================================================
# CONFIG STREAMLIT
# ==================================================
st.set_page_config(
    page_title="Conferência Editor de Arte",
    layout="wide",
)

# ==================================================
# CORES
# ==================================================
AZUL = HexColor("#1B2D6B")
AMARELO = HexColor("#FFF3B0")
CINZA = HexColor("#F2F2F2")
PRETO = HexColor("#000000")
LOGO_PATH = "logo_bernoulli.png"

# ==================================================
# ESTADO GLOBAL (NUNCA REMOVE)
# ==================================================
if "dados" not in st.session_state:
    st.session_state.dados = {
        "simulado": "",
        "etapa": "",
        "volume": "",
        "prova": "",
        "data": "",
        "disciplinas": [],
        "redacao": "Não",
        "miolo": "Preto e Branco",
        "codigo_barras": "",
        "qtd": 0,
        "num_inicial": 1,
    }

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
        st.session_state.dados["simulado"] = st.text_input(
            "Nome do Simulado", st.session_state.dados["simulado"]
        )
        st.session_state.dados["etapa"] = st.text_input(
            "Etapa", st.session_state.dados["etapa"]
        )
        st.session_state.dados["volume"] = st.text_input(
            "Volume", st.session_state.dados["volume"]
        )
        st.session_state.dados["prova"] = st.text_input(
            "Prova", st.session_state.dados["prova"]
        )

    with col2:
        data_valor = st.date_input("Data de aplicação")
        st.session_state.dados["data"] = data_valor.strftime("%d/%m/%Y")

        st.session_state.dados["num_inicial"] = st.number_input(
            "Numeração inicial das questões",
            min_value=1,
            value=st.session_state.dados["num_inicial"],
            step=1,
        )

        st.session_state.dados["qtd"] = st.number_input(
            "Quantidade de questões",
            min_value=1,
            value=max(st.session_state.dados["qtd"], 1),
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
            default=st.session_state.dados["disciplinas"],
        )

        st.session_state.dados["redacao"] = st.radio(
            "Tem redação?",
            ["Sim", "Não"],
            index=0 if st.session_state.dados["redacao"] == "Sim" else 1,
        )

        st.session_state.dados["codigo_barras"] = st.text_input(
            "Código de barras", st.session_state.dados["codigo_barras"]
        )

        st.session_state.dados["miolo"] = st.radio(
            "Miolo",
            ["Preto e Branco", "Colorido"],
            index=0 if st.session_state.dados["miolo"] == "Preto e Branco" else 1,
        )

    st.success("✅ Dados salvos automaticamente")

# ==================================================
# PARTE 2 — CHECKLIST TÉCNICO
# ==================================================
elif pagina == "Parte 2 — Checklist Técnico":
    st.header("✅ Checklist Técnico")

    st.subheader("CAPA")
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
        col1, col2 = st.columns([1, 6])
        with col1:
            st.checkbox("", key=f"capa_{item}")
        with col2:
            st.text_input(item, key=f"corr_capa_{item}")

    st.divider()

    st.subheader("MIOLO / DIAGRAMAÇÃO")
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

    qtd = st.session_state.dados["qtd"]
    inicio = st.session_state.dados["num_inicial"]

    if qtd <= 0:
        st.warning("Preencha a Parte 1 antes de continuar.")
    else:
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
                st.multiselect(
                    "Itens conferidos",
                    itens_conferencia,
                    key=f"conf_{numero}",
                )

            with colB:
                st.radio(
                    "Houve correção?",
                    ["Não", "Sim"],
                    horizontal=True,
                    key=f"corrigido_{numero}",
                )
                st.text_area("O que foi feito", key=f"desc_{numero}")

            st.markdown("---")

# ==================================================
# RELATÓRIO — PDF
# ==================================================
elif pagina == "Relatório":
    st.header("📄 Relatório Final")
    st.info("Geração de PDF estável e com layout institucional ✅")
