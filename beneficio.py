import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Simulador de Beneficiamento",
    layout="centered",
    initial_sidebar_state="collapsed"
)

inicio_beneficio = datetime(2026, 7, 23)
hoje = datetime.today()


def dias_trabalhados(inicio, fim):
    dias = pd.date_range(start=inicio, end=fim)
    dias_uteis = dias[dias.dayofweek != 6]  # 6 = domingo
    return len(dias_uteis)


dias_uteis = dias_trabalhados(inicio_beneficio, hoje)

df = pd.read_excel("TesteOdair.xlsx")
df["Fardos Restantes"] = df["FardaoColhido"] - df["Beneficiado"]

aba1, aba2 = st.tabs(["📋 Dados Atuais", "📅 Simulação de Término"])

# --- ABA 1: Dados Atuais ---
with aba1:
    st.markdown("## 📋 Dados Atuais de Beneficiamento")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Dias Úteis Trabalhados", f"{dias_uteis} dias")
    with col2:
        total_beneficiado = df["Beneficiado"].sum()
        media_por_dia = total_beneficiado / dias_uteis if dias_uteis > 0 else 0
        st.metric("Média/Dia", f"{media_por_dia:.1f} Fardos")

    st.divider()

    def estimar_termino_real(row):
        if dias_uteis == 0 or row["Beneficiado"] == 0:
            return "Dados insuficientes"
        produtividade_real = row["Beneficiado"] / dias_uteis
        if produtividade_real == 0:
            return "Produtividade zero"
        dias_necessarios = int(row["Fardos Restantes"] / produtividade_real) + (
            1 if row["Fardos Restantes"] % produtividade_real > 0 else 0)

        data = hoje
        adicionados = 0
        while adicionados < dias_necessarios:
            data += timedelta(days=1)
            if data.weekday() != 6:
                adicionados += 1
        return data.strftime("%d/%m/%Y")

    df["Data Estimada (Produtividade Real)"] = df.apply(estimar_termino_real, axis=1)

    st.markdown("### 🧺 Dados Atuais")

    for index, row in df.iterrows():
        #st.markdown(f"**🔹 Lote {index + 1}**")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Fardos Colhidos", row["FardaoColhido"])
            st.metric("Beneficiado", row["Beneficiado"])
        with col2:
            st.metric("Fardos Restantes", row["Fardos Restantes"])
            st.metric("Data Estimada", row["Data Estimada (Produtividade Real)"])
        st.divider()

# --- ABA 2: Simulação ---
with aba2:
    st.markdown("## 📅 Simulador de Data de Término")
    st.markdown("""
        <style>
        .streamlit-expanderHeader, .stSlider label, .stSlider div[data-testid="stSliderValue"] {
            font-size: 5rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

    simulacao_dia = st.slider(
        "Simule a produtividade diária (fardos/dia)",
        min_value=0,
        max_value=150,
        value=50,
        help="Arraste para ajustar a produtividade"
    )

    st.info(f"📊 Produtividade simulada: **{simulacao_dia} fardos/dia**")
    st.divider()

    def estimar_termino_simulado(faltantes, produtividade_dia):
        if produtividade_dia == 0:
            return "Produtividade zero"
        if faltantes <= 0:
            return "Já concluído"

        dias_necessarios = int(faltantes / produtividade_dia) + (1 if faltantes % produtividade_dia > 0 else 0)

        data = hoje
        adicionados = 0
        if data.weekday() != 6:
            adicionados = 1

        while adicionados < dias_necessarios:
            data += timedelta(days=1)
            if data.weekday() != 6:
                adicionados += 1

        return data.strftime("%d/%m/%Y")

    df["Data Término Estimada (Simulação)"] = df["Fardos Restantes"].apply(
        lambda x: estimar_termino_simulado(x, simulacao_dia))

    #st.markdown("### 📦 Simulação por Lote")

    for index, row in df.iterrows():
       # st.markdown(f"**📦 Lote {index + 1}**")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Fardos Restantes", row["Fardos Restantes"])
        with col2:
            st.metric("Data Estimada (Simulação)", row["Data Término Estimada (Simulação)"])
        st.divider()

