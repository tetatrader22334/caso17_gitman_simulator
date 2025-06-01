
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Configurações iniciais
st.set_page_config(page_title="Simulador de Financiamento", layout="centered")

st.title("📊 Simulador de Financiamento vs. Ciclo de Caixa")
st.write("""
Este simulador permite avaliar como a **necessidade de financiamento** e o **custo anual** 
variam com a **taxa de juros** e o **ciclo de caixa** (número de dias que o capital fica imobilizado).
""")
st.markdown("---")

# Entradas do usuário
taxa_juros = st.slider("Selecione a taxa de juros anual (%)", min_value=5.0, max_value=20.0, value=12.0, step=0.5)
ciclos_selecionados = st.multiselect(
    "Selecione os ciclos de caixa a comparar (em dias):",
    options=[155, 127, 87],
    default=[155, 87],
    format_func=lambda x: {
        155: "155 dias (Atual)",
        127: "127 dias (Médio)",
        87: "87 dias (Otimizado)"
    }.get(x, f"{x} dias")
)

# Constantes
financiamento_anual = 14_400_000
dias_ano = 360
financiamento_diario = financiamento_anual / dias_ano

# Cálculo e exibição
dados = []

for ciclo in ciclos_selecionados:
    necessidade_media = financiamento_diario * ciclo
    custo_anual = necessidade_media * (taxa_juros / 100)
    dados.append({
        "Ciclo de Caixa (dias)": ciclo,
        "Necessidade Média (R$)": necessidade_media,
        "Custo Anual (R$)": custo_anual
    })

df_resultados = pd.DataFrame(dados).sort_values(by="Ciclo de Caixa (dias)", ascending=False)

# Mostrar tabela
st.markdown("### 📄 Resultados da Simulação")
st.dataframe(df_resultados.style.format({
    "Necessidade Média (R$)": "R$ {:,.2f}",
    "Custo Anual (R$)": "R$ {:,.2f}"
}))

# Gráfico
st.markdown("### 📈 Comparação Gráfica")
fig, ax = plt.subplots()
bar_width = 0.35
x = range(len(df_resultados))
ax.bar(x, df_resultados["Necessidade Média (R$)"], width=bar_width, label="Necessidade Média", color="skyblue")
ax.bar([i + bar_width for i in x], df_resultados["Custo Anual (R$)"], width=bar_width, label="Custo Anual", color="salmon")
ax.set_xticks([i + bar_width / 2 for i in x])
ax.set_xticklabels(df_resultados["Ciclo de Caixa (dias)"])
ax.set_ylabel("Valor (R$)")
ax.set_title("Necessidade de Financiamento e Custo Anual")
ax.legend()
ax.grid(True, axis='y')
st.pyplot(fig)

# Exportação
csv = df_resultados.to_csv(index=False)
st.download_button("📥 Baixar resultados em CSV", csv, "simulador_financiamento.csv", "text/csv")
