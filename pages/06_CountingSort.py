import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

# ==========================================================
# CONFIGURAÇÃO VISUAL PROFISSIONAL
# ==========================================================

st.set_page_config(
    page_title="Counting Sort",
)

plt.style.use("seaborn-v0_8-darkgrid")  

st.markdown(
    "<h2 style='text-align: center;'>📈 Algoritmo Counting Sort</h2>",
    unsafe_allow_html=True
)

st.markdown(
    "<h3 style='text-align: center;'>🔍 Análise Experimental</h3>",
    unsafe_allow_html=True
) 
    
st.markdown("""
### 🎯 Objetivo

Este relatório apresenta a análise experimental do algoritmo Counting Sort,
utilizando os dados do arquivo `ceps.txt`, contendo uma sequência aleatória de `58.255` CEPs.

### 📊 Os gráficos relacionam

- **Eixo X:** Tamanho do vetor (n)  
- **Eixo Y:** Tempo de execução (ms)
""")

# --------------------------------------------------
# ITEM B - COMPLEXIDADE
# --------------------------------------------------

st.markdown("""
### ⏱ Complexidade do algoritmo

- Melhor caso: **O(n + k)**
- Caso médio: **O(n + k)**
- Pior caso: **O(n + k)**

Onde:

- **n** = número de elementos  
- **k** = intervalo dos valores possíveis *(k = max − min + 1)*  

O Counting Sort realiza duas etapas principais:

1. Percorre o vetor de entrada para contabilizar as ocorrências → custo **O(n)**  
2. Inicializa e acumula o vetor de contagem → custo **O(k)**  

Assim, a complexidade total do algoritmo é:

<p style="text-align:center; font-weight:bold;">
O(n + k)
</p>

Quando o intervalo de valores é pequeno ou proporcional ao tamanho da entrada, o comportamento prático aproxima-se de:

<p style="text-align:center; font-weight:bold;">
O(n)
</p>

Entretanto, quando k ≫ n (como ocorre em conjuntos de CEPs com grande dispersão numérica),
o termo dominante passa a ser k, e o custo prático aproxima-se de:

<p style="text-align:center; font-weight:bold;">
O(k)
</p>
""", unsafe_allow_html=True)

# ==========================================================
# FUNÇÃO PARA CARREGAR DADOS
# ==========================================================
st.markdown("### 📂 Leitura do arquivo experimental")

@st.cache_data
def carregar_dados_counting(nome_arquivo):
    df = pd.read_csv(nome_arquivo, sep=r"\s+")  # lê cabeçalho automaticamente
    df.columns = ["n", "tempo", "cep"]  # padroniza nomes
    
    # Garante que colunas são numéricas
    df["n"] = pd.to_numeric(df["n"], errors="coerce")
    df["tempo"] = pd.to_numeric(df["tempo"], errors="coerce")
    df["cep"] = pd.to_numeric(df["cep"], errors="coerce")
    df = df.dropna()
    return df

try:
    df_counting = carregar_dados_counting("dados/countingsort/ceps_ordenado_counting.txt")
    st.success("Arquivo carregado com sucesso!")

except:
    st.error("Erro ao carregar o arquivo. Verifique se está no caminho correto.")
    st.stop()

# ==========================================================
# 1 - MÉTRICAS GERAIS
# ==========================================================

st.header("1. Métricas gerais de execução")

# Pega apenas a primeira linha, pois todas têm o mesmo tempo total
tempo_total = df_counting["tempo"].sum()  # tempo total em ms
tempo_medio = df_counting["tempo"].sum() / df_counting["n"].sum()  # tempo médio por elemento
maior_n = df_counting["n"].max()  # maior n ordenado

def formatar_tempo(ms_total):
    total_segundos = int(ms_total / 1000)
    horas = total_segundos // 3600
    minutos = (total_segundos % 3600) // 60
    segundos = total_segundos % 60
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Tempo Total (hh:mm:ss)", formatar_tempo(tempo_total))
with col2:
    st.metric("Tempo Médio (ms)", f"{tempo_medio:.3f}")
with col3:
    st.metric("Maior n Ordenado", f"{maior_n:,}".replace(",", "."))

# ==========================================================
# FUNÇÃO PADRONIZADA DE PLOT
# ==========================================================
def plotar_counting(df, titulo):
    x = df["n"].values
    y = df["tempo"].values

    # Interpolação para suavizar a curva
    x_novo = np.linspace(x.min(), x.max(), 300)
    spline = make_interp_spline(x, y, k=3)
    y_suave = spline(x_novo)

    # Cálculo da reta de tendência linear
    coef = np.polyfit(x_novo, y_suave, 1)        # ajuste linear
    reta_tendencia = np.poly1d(coef)
    y_tendencia = reta_tendencia(x_novo)

    # Cálculo do tempo médio
    tempo_medio = y.mean()

    # Criação do gráfico
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x_novo, y_suave, linewidth=1, label="Tempo suavizado")
    ax.plot(x_novo, y_tendencia, linestyle='--', color='red', linewidth=1.1, label="Tendência linear")
    ax.axhline(y=tempo_medio, linestyle='--', color='green', linewidth=1.1, label=f"Tempo médio = {tempo_medio:.2f} ms")  # linha do tempo médio
    ax.set_xlabel("Tamanho do vetor (n)")
    ax.set_ylabel("Tempo de execução (ms)")
    ax.set_title(titulo)
    ax.legend()

    return fig

# ==========================================================
# 2 - GRÁFICO DE EXECUÇÃO
# ==========================================================
st.header("2. Gráfico de execução do Counting Sort")
st.pyplot(plotar_counting(df_counting, "Counting Sort - CEPs Ordenados"))

# ==========================================================
# 3 - ANÁLISE ASSINTÓTICA
# ==========================================================
st.header("3. Comparação com crescimento assintótico")

x = df_counting["n"].values
y = df_counting["tempo"].values

# Suavização da curva
x_suave = np.linspace(x.min(), x.max(), 400)
ordem = np.argsort(x)
x_ord = x[ordem]
y_ord = y[ordem]

spline = make_interp_spline(x_ord, y_ord, k=3)
y_suave = spline(x_suave)

# Cálculo da reta de tendência linear
coef = np.polyfit(x_suave, y_suave, 1)      # coeficiente da reta
reta_tendencia = np.poly1d(coef)
y_tendencia = reta_tendencia(x_suave)

# Curva O(n)
curva_n = x_suave
curva_n = (curva_n / np.max(curva_n)) * np.max(y_suave)

# Criação do gráfico
fig, ax = plt.subplots(figsize=(10,6))
ax.plot(x_suave, y_suave, label="Counting Sort", linewidth=0.75)
ax.plot(x_suave, curva_n, linestyle="--", color="green", linewidth=1.1, label="O(n + k) ≈ O(n)")
ax.plot(x_suave, y_tendencia, linestyle="--", color="red", linewidth=1.1, label="Tendência linear (Regressão)")  # reta de tendência

ax.set_xlabel("Tamanho do vetor (n)")
ax.set_ylabel("Tempo de execução (ms)")
ax.set_title("Análise Assintótica do Counting Sort", fontsize=14)
ax.legend()

st.pyplot(fig)

# ==========================================================
# 4 - TEXTO FORMAL
# ==========================================================
st.header("4. 🧾 Análise formal dos resultados")

st.markdown("""
<div style="text-align: justify;">

<h3>4.1 📏 Relação entre o tamanho da sequência e o maior valor</h3>

<p>
A análise experimental do Counting Sort evidencia uma relação direta entre o tamanho da sequência de entrada (n) e o maior valor presente na sequência, que determina o intervalo k = (max − min + 1).
</p>

<p>
Observou-se que, à medida que novos CEPs são considerados, o maior valor da sequência cresce rapidamente, atingindo valores próximos de 100 milhões ainda nas primeiras milhares de inserções. Dessa forma, o intervalo k torna-se muito superior ao tamanho n da sequência.
</p>

<p>
Matematicamente, como a complexidade do Counting Sort é:
</p>

<p style="text-align:center; font-weight:bold;">
T(n) = O(n + k)
</p>

<p>
Quando k ≫ n, o termo dominante passa a ser k. No experimento realizado, verificou-se exatamente esse comportamento: o tempo de execução não cresceu proporcionalmente a n, mas manteve-se relativamente estável após o maior valor da base ser atingido.
</p>

<p>
Isso demonstra que o desempenho do Counting Sort depende fortemente da amplitude dos valores e não apenas da quantidade de elementos.
</p>

<h3>4.2 📊 Interpretação do Comportamento Observado</h3>

<p>Os gráficos evidenciam que:</p>

<ul>
<li>O tempo de execução apresenta crescimento limitado mesmo com aumento significativo de n;</li>
<li>Após a estabilização do maior valor da sequência, o custo do algoritmo torna-se praticamente constante;</li>
<li>A ordem inicial dos dados não influencia o desempenho, pois o Counting Sort não realiza comparações.</li>
</ul>

<p>
Assim, conclui-se que, no conjunto de CEPs analisado, o algoritmo apresentou comportamento compatível com:
</p>

<p style="text-align:center; font-weight:bold;">
T(n) ≈ O(k)
</p>

<p>
devido à grande dispersão numérica dos dados.
</p>

<h3>4.3 ✅ Conclusão Experimental</h3>

<p>
Os resultados empíricos confirmam a dependência estrutural do Counting Sort em relação ao intervalo dos valores. Para conjuntos de dados com grande dispersão numérica, como os CEPs utilizados, o custo de inicialização e processamento do vetor de contagem domina o tempo total de execução.
</p>

<p>
Portanto, embora o algoritmo possua complexidade linear teórica, sua eficiência prática depende diretamente da relação entre o tamanho da entrada e o maior valor presente na sequência.
</p>

</div>
""", unsafe_allow_html=True)