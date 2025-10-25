# import pandas as pd
# import streamlit as st
# from datetime import datetime, timedelta
#
#
# st.set_page_config(page_title="Simulador de Beneficiamento", layout="wide")
#
# inicio_beneficio = datetime(2025, 7, 29)
# hoje = datetime.today()
#
#
# def dias_trabalhados(inicio, fim):
#     dias = pd.date_range(start=inicio, end=fim)
#     dias_uteis = dias[dias.dayofweek != 6]  # 6 = domingo
#     return len(dias_uteis)
#
# dias_uteis = dias_trabalhados(inicio_beneficio, hoje)
#
# df = pd.read_excel("TesteOdair.xlsx")
#
# df["Fardos Restantes"] = df["FardaoColhido"] - df["Beneficiado"]
#
# aba1, aba2 = st.tabs(["📋 Dados Atuais", "📅 Simulação de Término"])
#
# with aba1:
#     st.markdown("## 📋 Dados Atuais de Beneficiamento")
#     st.markdown(f"**Dias úteis trabalhados desde 29/07/2025 até hoje:** `{dias_uteis}` dias")
#
#     # Calcular média de fardos beneficiados por dia
#     total_beneficiado = df["Beneficiado"].sum()
#     media_por_dia = total_beneficiado / dias_uteis if dias_uteis > 0 else 0
#     st.markdown(f"**Média de fardos beneficiados por dia:** `{media_por_dia:.2f}` fardos/dia")
#
#     st.divider()
#
#
#     def estimar_termino_real(row):
#         if dias_uteis == 0 or row["Beneficiado"] == 0:
#             return "Dados insuficientes"
#         produtividade_real = row["Beneficiado"] / dias_uteis
#         if produtividade_real == 0:
#             return "Produtividade zero"
#         dias_necessarios = int(row["Fardos Restantes"] / produtividade_real) + (1 if row["Fardos Restantes"] % produtividade_real > 0 else 0)
#
#         data = hoje
#         adicionados = 0
#         while adicionados < dias_necessarios:
#             data += timedelta(days=1)
#             if data.weekday() != 6:
#                 adicionados += 1
#         return data.strftime("%d/%m/%Y")
#
#     df["Data Estimada (Produtividade Real)"] = df.apply(estimar_termino_real, axis=1)
#
#     st.dataframe(df[["FardaoColhido", "Beneficiado", "Fardos Restantes", "Data Estimada (Produtividade Real)"]], use_container_width=True)
#
#
# with aba2:
#     st.markdown("## 📅 Simulador de Data de Término")
#     simulacao_dia = st.slider("Simule a produtividade diária (fardos/dia)", min_value=0, max_value=150, value=50)
#     st.divider()
#
#     def estimar_termino_simulado(faltantes, produtividade_dia):
#         if produtividade_dia == 0:
#             return "Produtividade zero"
#         if faltantes <= 0:
#             return "Já concluído"
#
#         dias_necessarios = int(faltantes / produtividade_dia) + (1 if faltantes % produtividade_dia > 0 else 0)
#
#         data = hoje
#         adicionados = 0
#
#
#         if data.weekday() != 6:
#             adicionados = 1
#
#         while adicionados < dias_necessarios:
#             data += timedelta(days=1)
#             if data.weekday() != 6:  # pula domingo
#                 adicionados += 1
#
#         return data.strftime("%d/%m/%Y")
#
#     df["Data Término Estimada (Simulação)"] = df["Fardos Restantes"].apply(lambda x: estimar_termino_simulado(x, simulacao_dia))
#
#     st.dataframe(df[["FardaoColhido", "Beneficiado", "Fardos Restantes", "Data Término Estimada (Simulação)"]], use_container_width=True)


import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Simulador de Beneficiamento",
    layout="centered",  # Melhor para mobile
    initial_sidebar_state="collapsed"  # Sidebar fechada por padrão
)

inicio_beneficio = datetime(2025, 7, 29)
hoje = datetime.today()


def dias_trabalhados(inicio, fim):
    dias = pd.date_range(start=inicio, end=fim)
    dias_uteis = dias[dias.dayofweek != 6]  # 6 = domingo
    return len(dias_uteis)


dias_uteis = dias_trabalhados(inicio_beneficio, hoje)

df = pd.read_excel("TesteOdair.xlsx")

df["Fardos Restantes"] = df["FardaoColhido"] - df["Beneficiado"]

aba1, aba2 = st.tabs(["📋 Dados Atuais", "📅 Simulação de Término"])

with aba1:
    st.markdown("## 📋 Dados Atuais de Beneficiamento")

    # Cards com métricas (melhor visualização em mobile)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Dias Úteis Trabalhados", f"{dias_uteis} dias")
    with col2:
        total_beneficiado = df["Beneficiado"].sum()
        media_por_dia = total_beneficiado / dias_uteis if dias_uteis > 0 else 0
        st.metric("Média/Dia", f"{media_por_dia:.1f} fardos")

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

    st.dataframe(
        df[["FardaoColhido", "Beneficiado", "Fardos Restantes", "Data Estimada (Produtividade Real)"]],
        use_container_width=True,
        height=400  # Altura fixa para melhor scroll em mobile
    )

with aba2:
    st.markdown("## 📅 Simulador de Data de Término")
    simulacao_dia = st.slider(
        "Simule a produtividade diária (fardos/dia)",
        min_value=0,
        max_value=150,
        value=50,
        help="Arraste para ajustar a produtividade"  # Tooltip útil
    )

    # Mostrar valor atual em destaque
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

        # Se hoje não é domingo, conta hoje como dia 1
        if data.weekday() != 6:
            adicionados = 1

        # Continua adicionando dias até completar os dias necessários
        while adicionados < dias_necessarios:
            data += timedelta(days=1)
            if data.weekday() != 6:  # pula domingo
                adicionados += 1

        return data.strftime("%d/%m/%Y")


    df["Data Término Estimada (Simulação)"] = df["Fardos Restantes"].apply(
        lambda x: estimar_termino_simulado(x, simulacao_dia))

    st.dataframe(
        df[["FardaoColhido", "Beneficiado", "Fardos Restantes", "Data Término Estimada (Simulação)"]],
        use_container_width=True,
        height=400
    )