import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar dados gerados previamente
resumo_vendedor = pd.read_csv("resumo_vendedor.csv")
resumo_cliente = pd.read_csv("resumo_cliente.csv")
df_valid = pd.read_csv("df_valid.csv", parse_dates=['dt_hr_criacao'])

st.set_page_config(page_title="Dashboard Vendas", layout="wide")
st.image("logo_empresa.png", width=300)  # ajuste o tamanho com width
st.title("📊 Dashboard Interativo de Vendas Ecommerce Boni")

# KPIs principais
valor_total = df_valid['valor_total_atendido'].sum()
num_pedidos = df_valid['pedido_site'].nunique()
num_clientes = df_valid['codcli'].nunique()
num_vendedores = df_valid['nome_vendedor'].nunique()
ticket_medio = valor_total / num_pedidos

col1, col2, col3, col4 = st.columns(4)
col1.metric("Valor Total Vendido", f"R$ {valor_total:,.2f}")
col2.metric("Nº de Pedidos", num_pedidos)
col3.metric("Clientes Únicos", num_clientes)
col4.metric("Vendedores", num_vendedores)

# Texto com participação do e-commerce
st.markdown(f"""
🔎 **Participação do E-commerce:**
- Resultado do e-commerce representa **9,88%** das vendas do time de revenda.
- Resultado do e-commerce representa **6,15%** das vendas totais da empresa.
""")

# Informações sobre clientes ativos e conversão
st.markdown(f"""
📌 **Clientes Ativos e Conversão no Site:**
- Total de clientes ativos: **1.288**, desses **514** já fizeram ou fazem pedidos.
- Canal Obra: **178** ativos, **30** já fizeram ou fazem pedidos.
- Canal Revenda: **1.110** ativos, **484** já fizeram ou fazem pedidos.
""")


# Vendas por Data em gráfico de barras
st.subheader("📅 Vendas por Data")
vendas_por_dia = df_valid.groupby(df_valid['dt_hr_criacao'].dt.date)['valor_total_atendido'].sum().reset_index()
fig_timeline = px.bar(vendas_por_dia, x='dt_hr_criacao', y='valor_total_atendido', title="Vendas Diárias")
st.plotly_chart(fig_timeline, use_container_width=True)

# Análise por Vendedor
st.subheader("👨‍💼 Análise por Vendedor")
with st.expander("Tabela por Vendedor"):
    st.dataframe(resumo_vendedor)
fig_vendedor = px.bar(resumo_vendedor.sort_values('valor_vendido', ascending=False),
                      x='nome_vendedor', y='valor_vendido',
                      title="Total Vendido por Vendedor", text_auto=True)
st.plotly_chart(fig_vendedor, use_container_width=True)

# Dispersão Ticket Médio x Clientes Únicos
fig_disp = px.scatter(resumo_vendedor, x='clientes_unicos', y='ticket_medio',
                      size='valor_vendido', color='nome_vendedor',
                      title="Ticket Médio x Clientes Únicos por Vendedor")
st.plotly_chart(fig_disp, use_container_width=True)

# Análise por Cliente
st.subheader("🧑‍💼 Análise por Cliente")
with st.expander("Tabela por Cliente"):
    st.dataframe(resumo_cliente)

# Pareto Clientes
resumo_cliente_sorted = resumo_cliente.sort_values("valor_comprado", ascending=False)
fig_pareto = px.bar(resumo_cliente_sorted.head(20), x='razao_social', y='valor_comprado',
                    title="Top 20 Clientes - Valor Comprado")
st.plotly_chart(fig_pareto, use_container_width=True)
