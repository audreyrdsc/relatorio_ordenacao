import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

# ==========================================================
# CONFIGURAÇÃO VISUAL PROFISSIONAL
# ==========================================================

st.set_page_config(
    page_title="Radix Sort",
)

plt.style.use("seaborn-v0_8-darkgrid")  

st.markdown(
    "<h2 style='text-align: center;'>📈 Algoritmo Radix Sort</h2>",
    unsafe_allow_html=True
)

st.markdown(
    "<h3 style='text-align: center;'>🔍 Análise Experimental</h3>",
    unsafe_allow_html=True
) 
    
st.markdown("""
### 🎯 Objetivo

Este relatório apresenta a análise experimental do algoritmo **Radix Sort**,
utilizando os dados do arquivo `ceps.txt`, contendo uma sequência aleatória de `58.255` CEPs.

O Radix Sort foi implementado utilizando o **Counting Sort estável** como método interno
para ordenação de cada dígito.

### 📊 Os gráficos relacionam

- **Eixo X:** Tamanho do vetor (n)  
- **Eixo Y:** Tempo de execução (ms)
""")

# --------------------------------------------------
# COMPLEXIDADE
# --------------------------------------------------

st.markdown("### ⏱ Complexidade do algoritmo")

st.markdown("""
- Melhor caso: O(d · (n + k))
- Caso médio: O(d · (n + k))
- Pior caso: O(d · (n + k))

Onde:
- n = número de elementos
- k = base numérica (10 para CEP)
- d = número de dígitos do maior elemento

Como k é constante (10), a complexidade prática torna-se:

**O(d · n)** ≈ **O(n)**
""")

# ==========================================================
# LEITURA DOS DADOS
# ==========================================================

st.markdown("### 📂 Leitura do arquivo experimental")

@st.cache_data
def carregar_dados_radix(nome_arquivo):
    df = pd.read_csv(nome_arquivo, sep=r"\s+")  # usa cabeçalho automaticamente
    df.columns = ["n", "tempo"]  # renomeia para padronizar
    df["n"] = pd.to_numeric(df["n"], errors="coerce")
    df["tempo"] = pd.to_numeric(df["tempo"], errors="coerce")
    df = df.dropna()
    return df

try:
    df_radix = carregar_dados_radix("dados/radixsort/ceps_ordenado_radix.txt")
    st.success("Arquivo carregado com sucesso!")

except:
    st.error("Erro ao carregar o arquivo. Verifique o caminho.")
    st.stop()

# ==========================================================
# 1 - MÉTRICAS GERAIS
# ==========================================================

st.header("1. Métricas gerais de execução")

tempo_total = df_radix["tempo"].sum()
tempo_medio = df_radix["tempo"].mean()
maior_n = df_radix["n"].max()

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
# FUNÇÃO DE PLOT
# ==========================================================

def plotar_radix(df, titulo):

    x = df["n"].values
    y = df["tempo"].values

    ordem = np.argsort(x)
    x_ord = x[ordem]
    y_ord = y[ordem]

    x_novo = np.linspace(x_ord.min(), x_ord.max(), 400)

    spline = make_interp_spline(x_ord, y_ord, k=3)
    y_suave = spline(x_novo)

    # Linha média
    media = np.mean(y_ord)

    # Linha de tendência linear
    coef = np.polyfit(x_ord, y_ord, 1)
    linha_tendencia = np.poly1d(coef)
    y_tendencia = linha_tendencia(x_novo)

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(x_novo, y_suave, linewidth=0.8, label="Radix Sort")
    ax.plot(x_novo, y_tendencia, linestyle="--", linewidth=1.1, color="red", label="Tendência Linear")
    ax.axhline(media, linestyle="--", linewidth=1.1, color="green", label=f"Tempo médio = {media:.2f} ms")

    ax.set_xlabel("Tamanho do vetor (n)")
    ax.set_ylabel("Tempo de execução (ms)")
    ax.set_title(titulo)
    ax.legend()

    return fig

# ==========================================================
# 2 - GRÁFICO
# ==========================================================

st.header("2. Gráfico de execução do Radix Sort")

st.pyplot(plotar_radix(df_radix, "Radix Sort - CEPs Ordenados"))

# ==========================================================
# 3 - ANÁLISE ASSINTÓTICA
# ==========================================================

st.header("3. Comparação com crescimento assintótico")

x = df_radix["n"].values
y = df_radix["tempo"].values

ordem = np.argsort(x)
x_ord = x[ordem]
y_ord = y[ordem]

x_suave = np.linspace(x_ord.min(), x_ord.max(), 400)
spline = make_interp_spline(x_ord, y_ord, k=3)
y_suave = spline(x_suave)

# Curva teórica O(n) apenas escalonada
curva_linear_teorica = (x_suave / np.max(x_suave)) * np.max(y_suave)

# Linha de tendência real (regressão linear)
coef = np.polyfit(x_ord, y_ord, 1)
reta_tendencia = np.poly1d(coef)
y_tendencia = reta_tendencia(x_suave)

fig, ax = plt.subplots(figsize=(10,6))

ax.plot(x_suave, y_suave, label="Radix Sort (Experimental)", linewidth=0.8)
ax.plot(x_suave, curva_linear_teorica, linestyle="--", linewidth=1.1, color="green", label="O(n) (Teórica)")
ax.plot(x_suave, y_tendencia, linestyle="--", linewidth=1.1, color="red", label="Tendência Linear (Regressão)")

ax.set_xlabel("Tamanho do vetor (n)")
ax.set_ylabel("Tempo de execução (ms)")
ax.set_title("Análise Assintótica do Radix Sort")
ax.legend()

st.pyplot(fig)

# Exibir coeficiente angular (opcional acadêmico)
#st.caption(f"Inclinação da regressão (coeficiente angular): {coef[0]:.6f}")

# ==========================================================
# 4 - ANÁLISE FORMAL
# ==========================================================

st.header("4. 🧾 Análise formal dos resultados")

st.markdown("""
<div style="text-align: justify;">

<h3>4.1 📏 Relação entre o tamanho da sequência e o maior valor</h3>

<p>
No Radix Sort, o desempenho depende do número de dígitos do maior elemento da sequência (d),
e não diretamente do seu valor absoluto.
</p>

<p>
Como os CEPs possuem no máximo 8 dígitos, o valor de d permanece constante durante todo o experimento.
Assim, o crescimento do tempo de execução ocorre predominantemente em função de n.
</p>

<p style="text-align:center; font-weight:bold;">
T(n) = O(d · n)
</p>

<p>
Como d é constante, o comportamento prático aproxima-se de O(n).
</p>

<h3>4.2 📊 Interpretação do Comportamento Observado</h3>
<ul>
<li>
O tempo de execução apresenta crescimento aproximadamente linear à medida que o tamanho do vetor aumenta, evidenciando compatibilidade com a complexidade teórica O(d · n). Como o número de dígitos (d) dos CEPs permanece constante (até 8 dígitos), o fator dominante do crescimento é exclusivamente o tamanho da entrada (n).
</li>

<li>
Não se observa influência da magnitude absoluta do maior CEP, pois o Radix Sort não depende do intervalo total de valores (max − min). Diferentemente do Counting Sort tradicional, o algoritmo processa cada dígito individualmente, tornando o custo independente da dispersão numérica global.
</li>

<li>
O desempenho mantém estabilidade ao longo de todas as execuções, resultado do uso do Counting Sort estável em cada etapa de ordenação por dígito. A estabilidade garante que a ordenação parcial realizada em um dígito seja preservada nos dígitos subsequentes, assegurando correção e previsibilidade do tempo de execução.
</li>

<li>
Os gráficos obtidos demonstram ausência de oscilações abruptas ou crescimento exponencial, reforçando o comportamento assintótico linear observado experimentalmente. Pequenas variações são atribuídas a fatores do ambiente de execução, como alocação de memória e gerenciamento de cache, e não à estrutura do algoritmo.
</li>

</ul>



<h3>4.3 ✅ Conclusão Experimental</h3>

<p>
Os resultados confirmam que o Radix Sort apresenta crescimento linear consistente
para a base decimal utilizada.
</p>

<p>
Diferentemente do Counting Sort puro, o Radix Sort não sofre impacto da amplitude
numérica total dos dados, tornando-se mais adequado para conjuntos com grande dispersão,
como o caso dos CEPs analisados.
</p>

</div>
""", unsafe_allow_html=True)