
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configurações da página
st.set_page_config(layout="wide")

# Carregar dados
@st.cache_data
def load_data():
    df = pd.read_excel("DADOS to AI Testing.xlsx", sheet_name="Dados para AI- Light")
    df.replace([1, 11], 0, inplace=True)
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

df = load_data()

# Preparo dos dados para gráfico
meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago2', 'Set', 'out', 'Nov', 'Dez']
df_melted = df.drop(columns=["total"]).melt(id_vars=["Conta Contábil"], var_name="Mês", value_name="Valor")
df_melted['Mês'] = pd.Categorical(df_melted['Mês'], categories=meses, ordered=True)

# Layout com painel lateral
col_filtro, col_grafico = st.columns([1, 4])

with col_filtro:
    st.markdown("### Filtros")
    contas_opcao = st.multiselect(
        "Selecione as contas contábeis:",
        df["Conta Contábil"].unique(),
        default=df["Conta Contábil"].unique()
    )

with col_grafico:
    df_filtrado = df_melted[df_melted["Conta Contábil"].isin(contas_opcao)]

    # Gráfico de linhas
    fig = go.Figure()
    for conta in contas_opcao:
        dados = df_filtrado[df_filtrado["Conta Contábil"] == conta]
        fig.add_trace(go.Scatter(
            x=dados["Mês"],
            y=dados["Valor"],
            mode="lines+markers",
            name=conta,
            line=dict(width=0.5),
            marker=dict(size=6)
        ))
    fig.update_layout(
        title="Composição de Despesas por Conta Contábil",
        plot_bgcolor="white",
        xaxis_title="Mês",
        yaxis_title="Valor (R$)",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

# Cálculos dos cards
df_totais = df.set_index("Conta Contábil")
receita = df_totais.loc["Receita Líquida", "total"]
despesas = df_totais.drop("Receita Líquida")["total"].sum()
resultado = receita + despesas  # despesas são negativas

# Exibir cards
col1, col2, col3 = st.columns(3)
col1.metric("Receita Líquida", f"R$ {receita:,.2f}".replace(",", "."))
col2.metric("Total Despesas", f"R$ {abs(despesas):,.2f}".replace(",", "."))
col3.metric("Resultado Geral", f"R$ {resultado:,.2f}".replace(",", "."))
