import streamlit as st
import matplotlib.pyplot as plt

# Parâmetros fixos
financiamento_anual = 14_400_000
dias_ano = 360
financiamento_diario = financiamento_anual / dias_ano

# Título do app
st.title("Simulador de Financiamento vs. Ciclo de Caixa")

# Entradas do usuário
taxa_juros = st.slider("Selecione a taxa de juros anual (%)", 5.0, 20.0, 12.0, 0.5)
ciclo_caixa = st.selectbox("Escolha o ciclo de caixa (em dias):", [155, 87], index=0, format_func=lambda x: f"{x} dias (Atual)" if x == 155 else f"{x} dias (Otimizado)")

# Cálculos
necessidade_media = financiamento_diario * ciclo_caixa
custo_anual = necessidade_media * (taxa_juros / 100)

# Resultados
st.markdown("### Resultados da Simulação")
st.write(f"**Necessidade média de financiamento:** R$ {necessidade_media:,.2f}")
st.write(f"**Custo anual estimado:** R$ {custo_anual:,.2f}")

# Gráfico
fig, ax = plt.subplots()
ax.bar(["Dívida Média", "Custo Anual"], [necessidade_media, custo_anual], color=["skyblue", "salmon"])
ax.set_ylabel("Valor (R$)")
ax.set_title("Impacto do Ciclo de Caixa e da Taxa de Juros")
ax.grid(True, axis='y')
st.pyplot(fig)
