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
    page_title="Estudo Comparativo - Algoritmos de Ordenação"
)

plt.style.use("seaborn-v0_8-darkgrid")

st.markdown("<h2 style='text-align: center;'>📊 Estudo Comparativo de Algoritmos de Ordenação</h2>", unsafe_allow_html=True)

st.markdown(
    "<h4 style='text-align: center;'>Counting | Radix | QuickSort | HeapSort</h4>",
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
Este relatório apresenta a comparação experimental entre:

- Counting Sort
- Radix Sort
- QuickSort (Pivô Central)
- QuickSort (Pivô Aleatório)
- HeapSort

Utilizando os dados do arquivo `ceps.txt`, contendo uma sequência aleatória de `58.255` CEPs.
""")

# ==========================================================
# 1 - COMPLEXIDADE TEÓRICA
# ==========================================================

st.header("1. Complexidade Teórica")

st.markdown("""
| Algoritmo | Melhor Caso | Caso Médio | Pior Caso |
|------------|-------------|-------------|------------|
| Counting Sort | O(n + k) | O(n + k) | O(n + k) |
| Radix Sort | O(d·n) | O(d·n) | O(d·n) |
| QuickSort (Central) | O(n log n) | O(n log n) | O(n²) |
| QuickSort (Aleatório) | O(n log n) | O(n log n) | O(n²) (probabilidade baixa) |
| HeapSort | O(n log n) | O(n log n) | O(n log n) |
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
    quick_central = carregar_dados("dados/quicksort_meio_ceps/ceps_quicksort_meio.txt")
    quick_random = carregar_dados("dados/quicksort_aleatorio_ceps/ceps_quicksort_aleatorio.txt")
    heap = carregar_dados("dados/heapsort_ceps/ceps_heapsort.txt")
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
# 2 - GRÁFICOS INDIVIDUAIS (3 COLUNAS x 2 LINHAS)
# ==========================================================

st.header("2. Gráficos Individuais")

algoritmos = [
    ("Counting Sort", counting),
    ("Radix Sort", radix),
    ("QuickSort (Central)", quick_central),
    ("QuickSort (Aleatório)", quick_random),
    ("HeapSort", heap)
]

# Criar 2 linhas com 3 colunas cada
rows = [st.columns(3), st.columns(3)]

for i, (nome, df) in enumerate(algoritmos):

    row = rows[i // 3]
    col = row[i % 3]

    with col:

        st.markdown(
            f"<div style='text-align:center'><h5>{nome}</h5></div>",
            unsafe_allow_html=True
        )

        x_raw = df["n"].values
        y_raw = df["tempo_ms"].values

        x, y = suavizar(x_raw, y_raw)

        # Tendência linear
        coef = np.polyfit(x, y, 1)
        reta = np.poly1d(coef)
        y_tendencia = reta(x)

        # Tempo médio
        tempo_medio = np.mean(y_raw)

        fig, ax = plt.subplots(figsize=(5,4))

        ax.plot(x, y, linewidth=0.5, label=nome)
        ax.plot(x, y_tendencia, linestyle="--", linewidth=1.0, color="red", label="Tendência Linear")
        ax.axhline(
            tempo_medio,
            linestyle="--",
            linewidth=1.0,
            color="green",
            label=f"Média = {tempo_medio:.3f} ms"
        )

        ax.set_xlabel("n")
        ax.set_ylabel("Tempo (ms)")
        ax.legend(fontsize=7)

        st.pyplot(fig)

# ==========================================================
# 3 - GRÁFICO COMPARATIVO GERAL
# ==========================================================

st.header("3. Comparação Geral dos Algoritmos")

fig, ax = plt.subplots(figsize=(10,6))

algoritmos = {
    "Counting Sort": counting,
    "Radix Sort": radix,
    "QuickSort (Central)": quick_central,
    "QuickSort (Aleatório)": quick_random,
    "HeapSort": heap
}

cores = {
    "Counting Sort": "blue",
    "Radix Sort": "darkgreen",
    "QuickSort (Central)": "firebrick",
    "QuickSort (Aleatório)": "purple",
    "HeapSort": "orange"
}

for nome, df in algoritmos.items():
    x, y = suavizar(df["n"].values, df["tempo_ms"].values)
    ax.plot(
        x,
        y,
        linewidth=0.5,
        label=nome,
        color=cores[nome]
    )

ax.set_xlabel("Tamanho do vetor (n)")
ax.set_ylabel("Tempo (ms)")
ax.set_title("Comparação Geral de Desempenho")
ax.legend()

st.pyplot(fig)

# ==========================================================
# 4 - ANÁLISE ASSINTÓTICA INTERATIVA
# ==========================================================

st.header("4. Análise Assintótica - Interativo")

fig = go.Figure()

cores_plotly = {
    "Counting Sort": "royalblue",
    "Radix Sort": "green",
    "QuickSort (Central)": "firebrick",
    "QuickSort (Aleatório)": "purple",
    "HeapSort": "white"
}

for nome, df in algoritmos.items():
    x_suave, y_suave = suavizar(df["n"].values, df["tempo_ms"].values)

    fig.add_trace(go.Scatter(
        x=x_suave,
        y=y_suave,
        mode='lines',
        name=nome,
        line=dict(
            width=0.5,
            dash='solid',
            color=cores_plotly[nome]
        )
    ))

# ----------------------------------------------------------
# Curvas teóricas assintóticas
# ----------------------------------------------------------

# Base de referência para normalização
x_base, y_base = suavizar(counting["n"].values, counting["tempo_ms"].values)
tempo_max = np.max(y_base)

# 🔸 Curva O(n)
curva_n = (x_base / np.max(x_base)) * tempo_max

fig.add_trace(go.Scatter(
    x=x_base,
    y=curva_n,
    mode='lines',
    name="O(n)",
    line=dict(width=1.5, dash='dash', color='orange')
))

# 🔸 Curva O(n log n)
curva_nlogn = x_base * np.log2(x_base)
curva_nlogn = (curva_nlogn / np.max(curva_nlogn)) * tempo_max

fig.add_trace(go.Scatter(
    x=x_base,
    y=curva_nlogn,
    mode='lines',
    name="O(n log n)",
    line=dict(width=1.5, dash='dash', color="lightgreen")
))

# 🔸 Curva O(n²)
curva_n2 = x_base**2
curva_n2 = (curva_n2 / np.max(curva_n2)) * tempo_max

fig.add_trace(go.Scatter(
    x=x_base,
    y=curva_n2,
    mode='lines',
    name="O(n²)",
    line=dict(width=1.5, dash='dash', color="lightcoral")
))

fig.update_layout(
    title=dict(
        text="Comparação Assintótica - Counting | Radix | QuickSort | HeapSort",
        x=0.5,
        xanchor='center'
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

<h3>Resultados Observados</h3>

<p>
Os algoritmos lineares (Counting e Radix) apresentam crescimento aproximadamente linear.
Já QuickSort e HeapSort exibem crescimento típico de O(n log n).
</p>

<h3>Diferenças Estruturais</h3>

<ul>
    <li><strong>Counting Sort:</strong> desempenho depende do intervalo (k). Pode consumir mais memória.</li>
    <li><strong>Radix Sort:</strong> depende do número fixo de dígitos (d). Crescimento estável.</li>
    <li><strong>QuickSort (Central):</strong> pode sofrer degradação caso o pivô gere partições desbalanceadas.</li>
    <li><strong>QuickSort (Aleatório):</strong> reduz probabilidade de pior caso, mantendo comportamento médio O(n log n).</li>
    <li><strong>HeapSort:</strong> desempenho garantido O(n log n), porém com constante maior que QuickSort.</li>
</ul>

<h3>Conclusão</h3>

<p>
Counting e Radix apresentaram melhor desempenho assintótico no conjunto de CEPs devido à natureza numérica fixa dos dados.
</p>

<p>
QuickSort com pivô aleatório demonstrou maior estabilidade comparado ao pivô central,
reduzindo oscilações no tempo de execução.
</p>

<p>
HeapSort manteve comportamento previsível, porém com tempo ligeiramente superior devido ao custo de manutenção do heap.
</p>

<p>
Os resultados experimentais confirmam a teoria: algoritmos lineares superam algoritmos O(n log n)
quando suas premissas estruturais são atendidas.
</p>

</div>
""", unsafe_allow_html=True)
