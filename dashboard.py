import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard Financeiro", layout="wide")

st.title("📊 Dashboard Financeiro Interativo")

uploaded_file = st.file_uploader("📎 Envie a planilha com a aba 'Dados para AI- Light'", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name="Dados para AI- Light")
    df.replace(1, np.nan, inplace=True)
    df_mensal = df.drop(columns=['total'])
    df_mensal.set_index('Conta Contábil', inplace=True)
    df_mensal_t = df_mensal.T.apply(pd.to_numeric, errors='coerce')

    contas_receita = [conta for conta in df_mensal_t.columns if "Receita" in conta]
    contas_despesa = [conta for conta in df_mensal_t.columns if "Despesa" in conta or "Imposto" in conta]

    resultado_geral = df_mensal_t.sum(axis=1).sum()
    total_receitas = df_mensal_t[contas_receita].sum().sum()
    total_despesas = df_mensal_t[contas_despesa].sum().sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Resultado Geral", f"R$ {resultado_geral:,.2f}")
    col2.metric("📈 Total de Receitas", f"R$ {total_receitas:,.2f}")
    col3.metric("📉 Total de Despesas", f"R$ {total_despesas:,.2f}")

    contas = st.multiselect("Escolha as contas para o gráfico:", options=df_mensal_t.columns.tolist(), default=df_mensal_t.columns.tolist())

    fig = go.Figure()
    for conta in contas:
        fig.add_trace(go.Scatter(x=df_mensal_t.index, y=df_mensal_t[conta], mode='lines', name=conta, line=dict(width=0.5)))

    fig.update_layout(title="📊 Evolução Mensal das Contas", xaxis_title="Mês", yaxis_title="Valor", plot_bgcolor='white')

    st.plotly_chart(fig, use_container_width=True)
