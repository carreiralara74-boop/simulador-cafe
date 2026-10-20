import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Simulador Café PT", page_icon="☕", layout="centered")

st.markdown("<h1 style='text-align: center;'>☕ Simulador Café PT</h1>", unsafe_allow_html=True)
st.caption("Simule a viabilidade do seu café em minutos")

# Conexão direta ao seu Google Sheets "Viabilidade_Cafe_PT"
url_sheet = "https://docs.google.com/spreadsheets/d/1qykXmea2am5L090K0IRymlApe11oAaNo86as6O_gsUw/edit"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_inputs = conn.read(spreadsheet=url_sheet, worksheet="Inputs")
    # Ler os valores por omissão diretamente do Google Sheets (primeira linha)
    default_preco = float(str(df_inputs.iloc[0]['preco_medio_cliente']).replace(',', '.'))
    default_clientes = int(df_inputs.iloc[0]['clientes_dia'])
    default_dias = int(df_inputs.iloc[0]['dias_abertura_mes'])
    default_renda = float(str(df_inputs.iloc[0]['renda_mensal']).replace(',', '.'))
    default_salarios = float(str(df_inputs.iloc[0]['salarios_mensais']).replace(',', '.'))
    default_utilities = float(str(df_inputs.iloc[0]['utilities_mensais']).replace(',', '.'))
    default_seguros = float(str(df_inputs.iloc[0]['seguros_mensais']).replace(',', '.'))
    default_contabilidade = float(str(df_inputs.iloc[0]['contabilidade_mensal']).replace(',', '.'))
    default_marketing = float(str(df_inputs.iloc[0]['marketing_mensal']).replace(',', '.'))
    default_outros = float(str(df_inputs.iloc[0]['outros_custos_fixos']).replace(',', '.'))
except Exception:
    # Valores de reserva caso ocorra algum erro na ligação inicial
    default_preco, default_clientes, default_dias = 3.50, 60, 26
    default_renda, default_salarios, default_utilities = 900.0, 1500.0, 450.0
    default_seguros, default_contabilidade, default_marketing, default_outros = 100.0, 150.0, 100.0, 100.0

st.subheader("Receita")
preco_medio = st.number_input("Gasto médio por atendimento (€)", value=default_preco, step=0.10)
clientes_dia = st.number_input("Atendimentos por dia", value=default_clientes, step=1)
dias_abertura = st.number_input("Dias de abertura por mês", value=default_dias, step=1)

st.subheader("Custos variáveis")
custo_mercadorias_pct = st.number_input("Custo de mercadorias (%)", value=30.0, step=0.5) / 100
comissoes_cartoes_pct = st.number_input("Comissões de cartões (%)", value=1.5, step=0.1) / 100

st.subheader("Custos fixos mensais")
col1, col2 = st.columns(2)
with col1:
    renda = st.number_input("Renda mensal (€)", value=default_renda)
    salarios = st.number_input("Salários mensais (€)", value=default_salarios)
    utilities = st.number_input("Utilities / Água / Luz (€)", value=default_utilities)
with col2:
    seguros = st.number_input("Seguros (€)", value=default_seguros)
    contabilidade = st.number_input("Contabilidade (€)", value=default_contabilidade)
    marketing = st.number_input("Marketing (€)", value=default_marketing)
    outros = st.number_input("Outros custos fixos (€)", value=default_outros)

# Fórmulas idênticas às da aba 'Calculos' da folha de cálculo
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
