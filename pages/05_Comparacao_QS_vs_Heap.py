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
    page_title="Estudo Comparativo QuickSort x HeapSort"
) 

plt.style.use("seaborn-v0_8-darkgrid")

st.markdown("<h2 style='text-align: center;'>📊 Estudo Comparativo de Algoritmos de Ordenação</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>QuickSort (Pivô Central e Aleatório) 🆚 HeapSort</h4>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
Este relatório apresenta a comparação experimental entre:

- QuickSort com pivô central
- QuickSort com pivô aleatório
- HeapSort

Utilizando uma sequência aleatória de números inteiros entre 1 e 1.000.000, para três tipos de entrada:
- Aleatória
- Crescente
- Decrescente
""")

# ==========================================================
# 1 - COMPLEXIDADE TEÓRICA
# ==========================================================

st.header("1. Complexidade Teórica")

st.markdown("""
##### QuickSort

- Melhor caso: O(n log n)
- Caso médio: O(n log n)
- Pior caso: O(n²)

##### HeapSort

- Melhor caso: O(n log n)
- Caso médio: O(n log n)
- Pior caso: O(n log n)

QuickSort depende do pivô; pivô aleatório reduz a chance do pior caso.

O HeapSort é determinístico, garantindo O(n log n) independente da distribuição dos dados. 
""")

# ==========================================================
# FUNÇÃO DE LEITURA
# ==========================================================

@st.cache_data
def carregar_dados(caminho):
    df = pd.read_csv(caminho, sep=" ", header=None)
    df.columns = ["n", "tempo"]
    return df

def carregar_algoritmo(pasta):
    return {
        "aleatorio": carregar_dados(f"dados/{pasta}/aleatorio.txt"),
        "crescente": carregar_dados(f"dados/{pasta}/crescente.txt"),
        "decrescente": carregar_dados(f"dados/{pasta}/decrescente.txt"),
    }

try:
    meio = carregar_algoritmo("quicksort_meio")
    aleatorio = carregar_algoritmo("quicksort_aleatorio")
    heap = carregar_algoritmo("heapsort")
    st.success("Dados carregados com sucesso!")
except:
    st.error("Erro ao carregar os arquivos.")
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
# 2 - GRÁFICOS INDIVIDUAIS POR ALGORITMO
# ==========================================================

def grafico_individual(dados, titulo):
    fig, ax = plt.subplots(figsize=(10,6))
    for tipo, df in dados.items():
        x, y = suavizar(df["n"].values, df["tempo"].values)
        ax.plot(x, y, label=tipo.capitalize(), linewidth=0.75)
    ax.set_xlabel("Tamanho do vetor (n)")
    ax.set_ylabel("Tempo de execução (ms)")
    ax.set_title(titulo)
    ax.legend()
    st.pyplot(fig)

st.header("2. Gráficos Individuais")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div style='text-align: center;'><h5>QS (Pivô Central)</h5></div>", unsafe_allow_html=True)
    grafico_individual(meio, "QuickSort (Pivô Central)")

with col2:
    st.markdown("<div style='text-align: center;'><h5>QS (Pivô Aleatório)</h5></div>", unsafe_allow_html=True)
    grafico_individual(aleatorio, "QuickSort (Pivô Aleatório)")

with col3:
    st.markdown("<div style='text-align: center;'><h5>HeapSort</h5></div>", unsafe_allow_html=True)
    grafico_individual(heap, "HeapSort")

# ==========================================================
# 3 - GRÁFICOS COMPARATIVOS POR TIPO DE ENTRADA
# ==========================================================

st.header("3. Comparação entre algoritmos por tipo de entrada")

def grafico_comparativo(tipo):
    fig, ax = plt.subplots(figsize=(10,6))

    x1, y1 = suavizar(meio[tipo]["n"].values, meio[tipo]["tempo"].values)
    ax.plot(x1, y1, label="QuickSort - Pivô Central", linewidth=0.75)

    x2, y2 = suavizar(aleatorio[tipo]["n"].values, aleatorio[tipo]["tempo"].values)
    ax.plot(x2, y2, label="QuickSort - Pivô Aleatório", linewidth=0.75)

    x3, y3 = suavizar(heap[tipo]["n"].values, heap[tipo]["tempo"].values)
    ax.plot(x3, y3, label="HeapSort", linewidth=0.75)

    ax.set_xlabel("Tamanho do vetor (n)")
    ax.set_ylabel("Tempo de execução (ms)")
    ax.set_title(f"Comparação - Entrada {tipo.capitalize()}")
    ax.legend()
    st.pyplot(fig)
    
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div style='text-align: center;'><h5>Aleatória</h5></div>", unsafe_allow_html=True)
    grafico_comparativo("aleatorio")

with col2:
    st.markdown("<div style='text-align: center;'><h5>Crescente</h5></div>", unsafe_allow_html=True)
    grafico_comparativo("crescente")

with col3:
    st.markdown("<div style='text-align: center;'><h5>Decrescente</h5></div>", unsafe_allow_html=True)
    grafico_comparativo("decrescente")

# =======================================================================
# 4 - ANÁLISE ASSINTÓTICA INTERATIVO - COMPARAÇÃO DE CRESCIMENTO COMPLETA
# =======================================================================

st.header("4. Análise Assintótica - Interativo")

fig = go.Figure()

# =======================================
# QuickSort Central, Aleatório e HeapSort
# =======================================
for nome, alg in zip(["QS Central", "QS Aleatório", "HeapSort"], [meio, aleatorio, heap]):
    for tipo in ["aleatorio", "crescente", "decrescente"]:
        df = alg[tipo]
        x_suave, y_suave = suavizar(df["n"].values, df["tempo"].values)
        fig.add_trace(go.Scatter(
            x=x_suave,
            y=y_suave,
            mode='lines',
            name=f"{nome} - {tipo}",
            hovertemplate='n: %{x}<br>Tempo: %{y:.2f} ms',
            line=dict(width=0.5)  # <--- largura fina
        ))

# =========================
# Curvas Teóricas
# =========================
df_ref = meio["aleatorio"]
x_ref = df_ref["n"].values
x_suave, _ = suavizar(x_ref, df_ref["tempo"].values)

curva_nlogn = x_suave * np.log2(x_suave)
curva_nlogn = (curva_nlogn / np.max(curva_nlogn)) * np.max(df_ref["tempo"].values)
fig.add_trace(go.Scatter(x=x_suave, y=curva_nlogn, mode='lines', 
                         name="O(n log n)", line=dict(dash='dash', width=1)))

curva_n2 = x_suave**2
curva_n2 = (curva_n2 / np.max(curva_n2)) * np.max(df_ref["tempo"].values)
fig.add_trace(go.Scatter(x=x_suave, y=curva_n2, mode='lines', 
                         name="O(n²)", line=dict(dash='dash', width=1)))

# =========================
# Layout
# =========================
fig.update_layout(
    xaxis_title="Tamanho do vetor (n)",
    yaxis_title="Tempo de execução (ms)",
    title=dict(
        text="Comparação Assintótica - QuickSort x HeapSort",
        x=0.5,            # posição horizontal centralizada
        xanchor='center'   # âncora do texto no centro
    ),
    legend_title="Algoritmos",
    hovermode="x unified"
)

# =========================
# Mostrar no Streamlit
# =========================
st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# 5 - ANÁLISE FORMAL
# ==========================================================

st.header("5. Análise Comparativa Formal")

st.markdown("""
<div style="text-align: justify;">

<h3>Comparação Geral</h3>
<p>Observa-se que:</p>
<ul>
<li>HeapSort apresenta estabilidade total independente da entrada.</li>
<li>QuickSort com pivô aleatório é mais robusto que o pivô central.</li>
<li>QuickSort com pivô central pode ser sensível a entradas já ordenadas.</li>
<li>Todos os algoritmos crescem aproximadamente como O(n log n) para entradas grandes.</li>
</ul>

<h3>Conclusão</h3>
<p>Os resultados experimentais confirmam a teoria:</p>
<ul>
<li>HeapSort garante O(n log n) sempre.</li>
<li>QuickSort aleatório reduz a chance do pior caso.</li>
<li>QuickSort central é eficiente na maioria das entradas, mas pode degradar em casos específicos.</li>
</ul>

<p>Os resultados experimentais obtidos nos testes com diferentes tipos de entrada confirmam as expectativas teóricas sobre o comportamento dos algoritmos de ordenação analisados. O <strong>HeapSort</strong> demonstrou estabilidade consistente em todas as situações, mantendo a complexidade <strong>O(n log n)</strong> independentemente da distribuição dos dados, evidenciando sua robustez frente a sequências ordenadas, desordenadas ou parcialmente ordenadas.</p>

<p>O <strong>QuickSort com pivô aleatório</strong> apresentou desempenho muito próximo do ótimo em praticamente todos os cenários, comprovando que a escolha aleatória do pivô reduz significativamente a probabilidade de ocorrência do pior caso clássico <strong>O(n²)</strong>, promovendo partições mais balanceadas e, consequentemente, um tempo de execução eficiente mesmo em entradas adversas.</p>

<p>Já o <strong>QuickSort com pivô central</strong> mostrou-se eficiente na maioria das entradas, especialmente em sequências aleatórias ou moderadamente desordenadas. Entretanto, em casos específicos, como sequências já ordenadas ou quase ordenadas, pode ocorrer degradação no desempenho, aproximando-se do pior caso <strong>O(n²)</strong> devido ao desequilíbrio das partições.</p>

<p>Em síntese, a análise prática evidencia que a escolha do algoritmo e da estratégia de seleção do pivô deve considerar o tipo de entrada e a necessidade de previsibilidade do tempo de execução. Enquanto o HeapSort oferece garantia de desempenho consistente, o QuickSort aleatório combina alta eficiência com baixo risco de degradação, e o QuickSort central continua sendo uma solução adequada para entradas comuns, embora menos robusta em padrões específicos.</p>

</div>
""", unsafe_allow_html=True)