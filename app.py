import streamlit as st

st.set_page_config(page_title="Simulador Café PT", page_icon="☕", layout="centered")

st.markdown("<h1 style='text-align: center;'>☕ Simulador Café PT</h1>", unsafe_allow_html=True)
st.caption("Simule a viabilidade do seu café em minutos")

st.subheader("Receita")
preco_medio = st.number_input("Gasto médio por atendimento (€)", value=3.50, step=0.10)
clientes_dia = st.number_input("Atendimentos por dia", value=60, step=1)
dias_abertura = st.number_input("Dias de abertura por mês", value=26, step=1)

st.subheader("Custos variáveis")
custo_mercadorias_pct = st.number_input("Custo de mercadorias (%)", value=30.0, step=0.5) / 100
comissoes_cartoes_pct = st.number_input("Comissões de cartões (%)", value=1.5, step=0.1) / 100

st.subheader("Custos fixos mensais")
col1, col2 = st.columns(2)
with col1:
    renda = st.number_input("Renda mensal (€)", value=900)
    salarios = st.number_input("Salários mensais (€)", value=1500)
    utilities = st.number_input("Utilities / Água / Luz (€)", value=450)
with col2:
    seguros = st.number_input("Seguros (€)", value=100)
    contabilidade = st.number_input("Contabilidade (€)", value=150)
    marketing = st.number_input("Marketing (€)", value=100)
    outros = st.number_input("Outros custos fixos (€)", value=100)

# Fórmulas financeiras idênticas às da sua folha de cálculo
receita_mensal = preco_medio * clientes_dia * dias_abertura
custos_variaveis = receita_mensal * (custo_mercadorias_pct + comissoes_cartoes_pct)
custos_fixos = renda + salarios + utilities + seguros + contabilidade + marketing + outros
resultado_mensal = receita_mensal - custos_variaveis - custos_fixos

margem_por_cliente = preco_medio * (1 - custo_mercadorias_pct - comissoes_cartoes_pct)
if margem_por_cliente > 0:
    clientes_mes_eq = custos_fixos / margem_por_cliente
    clientes_dia_eq = clientes_mes_eq / dias_abertura
else:
    clientes_dia_eq = 0

st.divider()
st.subheader("📊 Resultados da Simulação")

st.metric("Receita Mensal Estimada", f"{receita_mensal:,.2f} €")
st.metric("Resultado Mensal Simplificado", f"{resultado_mensal:,.2f} €")

if resultado_mensal >= 0:
    st.success(f"A receita estimada é de {receita_mensal:,.0f} €. O resultado mensal estimado é de **{resultado_mensal:,.0f} €**.")
else:
    st.error(f"A receita estimada é de {receita_mensal:,.0f} €. O resultado mensal estimado é de **{resultado_mensal:,.0f} €** (prejuízo).")

st.info(f"Para cobrir os custos desta simulação, precisa de uma média de **{int(round(clientes_dia_eq))} atendimentos por dia**.")
