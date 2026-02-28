import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import plotly.graph_objects as go

# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(
    page_title="Estudo Comparativo - Counting vs Radix"
)

plt.style.use("seaborn-v0_8-darkgrid")

st.markdown("<h2 style='text-align: center;'>📊 Estudo Comparativo de Algoritmos de Ordenação</h2>", unsafe_allow_html=True)

st.markdown(
    "<h4 style='text-align: center;'>Counting Sort 🆚 Radix Sort</h4>",
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
Este relatório apresenta a comparação experimental entre:

- Counting Sort
- Radix Sort

Utilizando os dados do arquivo `ceps.txt`, contendo uma sequência aleatória de `58.255` CEPs.
""")

# ==========================================================
# 1 - COMPLEXIDADE TEÓRICA
# ==========================================================

st.header("1. Complexidade Teórica")

st.markdown("""
##### Counting Sort
- Complexidade: O(n + k)
- Onde:
    - n = número de elementos
    - k = intervalo (max - min)

Counting Sort é eficiente quando o intervalo k não é muito maior que n.

---

##### Radix Sort
- Complexidade: O(d · (n + b))
- Onde:
    - d = número de dígitos
    - b = base (10 nesse caso)

Para inteiros com número fixo de dígitos, Radix tende a se comportar como O(n).
""")

# ==========================================================
# LEITURA DOS DADOS
# ==========================================================

@st.cache_data
def carregar_dados(caminho):
    df = pd.read_csv(caminho, sep=" ")
    df = df.dropna()
    df.columns = df.columns.str.strip()
    return df

try:
    counting = carregar_dados("dados/countingsort/ceps_ordenado_counting.txt")
    radix = carregar_dados("dados/radixsort/ceps_ordenado_radix.txt")
    st.success("Dados carregados com sucesso!")
except:
    st.error("Erro ao carregar arquivos.")
    st.stop()

# ==========================================================
# FUNÇÃO DE SUAVIZAÇÃO
# ==========================================================

def suavizar(x, y):
    ordem = np.argsort(x)
    x = x[ordem]
    y = y[ordem]

    x_novo = np.linspace(x.min(), x.max(), 400)
    spline = make_interp_spline(x, y, k=3)
    y_novo = spline(x_novo)

    return x_novo, y_novo

# ==========================================================
# 2 - GRÁFICOS INDIVIDUAIS
# ==========================================================

st.header("2. Gráficos Individuais")

col1, col2 = st.columns(2)

# ==========================================================
# COUNTING SORT
# ==========================================================
with col1:
    st.markdown("<div style='text-align:center'><h5>Counting Sort</h5></div>", unsafe_allow_html=True)

    x_raw = counting["n"].values
    y_raw = counting["tempo_ms"].values

    x, y = suavizar(x_raw, y_raw)

    # Tendência linear
    coef = np.polyfit(x, y, 1)
    reta = np.poly1d(coef)
    y_tendencia = reta(x)

    # Tempo médio
    tempo_medio = np.mean(y_raw)

    fig, ax = plt.subplots(figsize=(8,5))

    ax.plot(x, y, linewidth=0.8, label="Curva Suavizada")
    ax.plot(x, y_tendencia, linestyle="--", linewidth=1.1, color="red", label="Tendência Linear")
    ax.axhline(tempo_medio, linestyle="--", linewidth=1.1, color="green",label=f"Tempo Médio = {tempo_medio:.4f} ms")

    ax.set_xlabel("Tamanho do vetor (n)")
    ax.set_ylabel("Tempo (ms)")
    ax.set_title("Counting Sort")
    ax.legend()

    st.pyplot(fig)


# ==========================================================
# RADIX SORT
# ==========================================================
with col2:
    st.markdown("<div style='text-align:center'><h5>Radix Sort</h5></div>", unsafe_allow_html=True)

    x_raw = radix["n"].values
    y_raw = radix["tempo_ms"].values

    x, y = suavizar(x_raw, y_raw)

    # Tendência linear
    coef = np.polyfit(x, y, 1)
    reta = np.poly1d(coef)
    y_tendencia = reta(x)

    # Tempo médio
    tempo_medio = np.mean(y_raw)

    fig, ax = plt.subplots(figsize=(8,5))

    ax.plot(x, y, linewidth=0.8, label="Curva Suavizada")
    ax.plot(x, y_tendencia, linestyle="--", linewidth=1.1, color="red", label="Tendência Linear")
    ax.axhline(tempo_medio, linestyle="--", linewidth=1.1, color="green", label=f"Tempo Médio = {tempo_medio:.4f} ms")

    ax.set_xlabel("Tamanho do vetor (n)")
    ax.set_ylabel("Tempo (ms)")
    ax.set_title("Radix Sort")
    ax.legend()

    st.pyplot(fig)

# ==========================================================
# 3 - GRÁFICO COMPARATIVO
# ==========================================================

st.header("3. Comparação entre algoritmos")

fig, ax = plt.subplots(figsize=(10,6))

x1, y1 = suavizar(counting["n"].values, counting["tempo_ms"].values)
x2, y2 = suavizar(radix["n"].values, radix["tempo_ms"].values)

ax.plot(x1, y1, label="Counting Sort", linewidth=0.8)
ax.plot(x2, y2, label="Radix Sort", color="red", linewidth=0.8)

ax.set_xlabel("Tamanho do vetor (n)")
ax.set_ylabel("Tempo (ms)")
ax.set_title("Counting vs Radix")
ax.legend()

st.pyplot(fig)

# ==========================================================
# 4 - ANÁLISE ASSINTÓTICA INTERATIVA
# ==========================================================

st.header("4. Análise Assintótica - Interativo")

fig = go.Figure()

# Curva Counting
x_suave, y_suave = suavizar(counting["n"].values, counting["tempo_ms"].values)
fig.add_trace(go.Scatter(
    x=x_suave,
    y=y_suave,
    mode='lines',
    name="Counting Sort",
    line=dict(width=0.8, dash='solid', color='royalblue')
))

# Curva Radix
x_suave2, y_suave2 = suavizar(radix["n"].values, radix["tempo_ms"].values)
fig.add_trace(go.Scatter(
    x=x_suave2,
    y=y_suave2,
    mode='lines',
    name="Radix Sort",
    line=dict(width=0.8, dash='solid', color='darkgreen')
))

# Curva O(n)
curva_n = x_suave
curva_n = (curva_n / np.max(curva_n)) * np.max(y_suave)
fig.add_trace(go.Scatter(
    x=x_suave,
    y=curva_n,
    mode='lines',
    name="O(n)",
    line=dict(width=1, dash='dash', color='orange')
))

fig.update_layout(
    title=dict(
        text="Comparação Assintótica - Counting vs Radix",
        x=0.5,            # posição horizontal centralizada
        xanchor='center'   # âncora do texto no centro
    ),
    xaxis_title="Tamanho do vetor (n)",
    yaxis_title="Tempo (ms)",
    hovermode="x unified",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# 5 - ANÁLISE FORMAL
# ==========================================================

st.header("5. Análise Comparativa Formal")

st.markdown("""
<div style="text-align: justify;">

<h3>Observações Experimentais</h3>

<ul>
<li>Ambos os algoritmos apresentam crescimento aproximadamente linear ao longo do aumento do tamanho da entrada.</li>
<li>O <strong>Counting Sort</strong> depende diretamente da amplitude do intervalo de valores (<em>k</em>).</li>
<li>O <strong>Radix Sort</strong> mantém crescimento mais uniforme, especialmente quando os dados possuem número fixo de dígitos.</li>
</ul>

<h3>Diferença Estrutural</h3>

<h4>Counting Sort</h4>
<ul>
<li>Aloca um vetor auxiliar proporcional ao intervalo (<em>range = max - min</em>).</li>
<li>Apresenta maior consumo de memória quando o intervalo é amplo.</li>
<li>É sensível à dispersão dos valores no conjunto de dados.</li>
</ul>

<h4>Radix Sort</h4>
<ul>
<li>Executa múltiplas passagens, uma para cada dígito significativo.</li>
<li>Utiliza internamente o Counting Sort como algoritmo estável por dígito.</li>
<li>Apresenta melhor escalabilidade para inteiros de tamanho fixo.</li>
<li>Distribui o custo ao longo das iterações, reduzindo impacto do intervalo global.</li>
</ul>

<h3>Conclusão</h3>

<p>
A análise experimental evidencia que ambos os algoritmos apresentam crescimento 
aproximadamente linear, corroborando o comportamento assintótico esperado de 
complexidade <strong>O(n)</strong> no contexto analisado.
</p>

<p>
O <strong>Counting Sort</strong> demonstra excelente desempenho quando o intervalo 
de valores (<em>k</em>) é limitado e proporcional ao tamanho da entrada (<em>n</em>). 
Nessas condições, seu custo O(n + k) mantém-se eficiente, com baixa constante 
multiplicativa e execução bastante rápida.
</p>

<p>
O <strong>Radix Sort</strong>, por sua vez, apresenta maior estabilidade estrutural, 
uma vez que seu desempenho depende do número fixo de dígitos dos elementos. 
Como os CEPs possuem tamanho numérico padronizado, o número de iterações 
permanece constante, resultando em crescimento linear uniforme e previsível.
</p>

<p>
Os resultados experimentais confirmam que, para conjuntos de dados numéricos 
com representação de tamanho fixo, o Radix Sort tende a apresentar maior 
regularidade no tempo de execução, enquanto o Counting Sort se destaca 
quando o intervalo de valores é adequadamente controlado.
</p>

<p>
Para CEPs (valores numéricos de tamanho fixo), Radix Sort tende a apresentar desempenho mais estável.
Counting Sort é excelente quando o intervalo é controlado.
Os resultados experimentais confirmam comportamento próximo de O(n).
</p>

<p>
Conclui-se, portanto, que ambos os algoritmos são adequados ao problema proposto, 
sendo a escolha entre eles dependente principalmente da amplitude dos dados, 
do custo espacial aceitável e das características estruturais do conjunto analisado.
</p>

</div>
""", unsafe_allow_html=True)