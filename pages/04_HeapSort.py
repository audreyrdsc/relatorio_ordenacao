import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

# ==========================================================
# CONFIGURAÇÃO VISUAL PROFISSIONAL
# ==========================================================

st.set_page_config(
    page_title="HeapSort",
)

plt.style.use("seaborn-v0_8-darkgrid")  

st.markdown(
    "<h2 style='text-align: center;'>📈 Algoritmo HeapSort</h2>",
    unsafe_allow_html=True
)

st.markdown(
    "<h3 style='text-align: center;'>🔍 Análise Experimental</h3>",
    unsafe_allow_html=True
) 
    
st.markdown("""
### 🎯 Objetivo

Este relatório apresenta a análise experimental do algoritmo HeapSort,
utilizando uma sequência aleatória de números inteiros entre `1` e `1.000.000`, para três tipos de entrada:

- Sequência Aleatória
- Sequência Crescente
- Sequência Decrescente

### 📊 Os gráficos relacionam

- **Eixo X:** Tamanho do vetor (n)  
- **Eixo Y:** Tempo de execução (ms)
""")

# --------------------------------------------------
# ITEM B - Complexidade
# --------------------------------------------------

st.markdown("### ⏱ Complexidade do algoritmo")

st.markdown("""
- Melhor caso: O(n log n)
- Caso médio: O(n log n)
- Pior caso: O(n log n)

O HeapSort constrói um heap máximo e realiza a ordenação de forma
determinística, garantindo complexidade O(n log n) independentemente
da distribuição inicial dos dados.
""")

# ==========================================================
# FUNÇÃO PARA CARREGAR DADOS
# ==========================================================
st.markdown("### 📂 Leitura dos arquivos experimentais")

@st.cache_data
def carregar_dados(nome_arquivo):
    df = pd.read_csv(nome_arquivo, sep=" ", header=None)
    df.columns = ["n", "tempo"]
    return df

try:
    df_aleatorio = carregar_dados("dados/heapsort/aleatorio.txt")
    df_crescente = carregar_dados("dados/heapsort/crescente.txt")
    df_decrescente = carregar_dados("dados/heapsort/decrescente.txt")

    st.success("Arquivos carregados com sucesso!")

except:
    st.error("Erro ao carregar os arquivos. Verifique se estão no mesmo diretório.")
    st.stop()

# ==========================================================
# 1 - MÉTRICAS GERAIS
# ==========================================================
st.header("1. Métricas gerais de execução por tipo de entrada")

col1, col2, col3 = st.columns(3)

def formatar_tempo(ms_total):
    total_segundos = ms_total / 1000
    horas = int(total_segundos // 3600)
    minutos = int((total_segundos % 3600) // 60)
    segundos = int(total_segundos % 60)
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

def mostrar_metricas(df, titulo, coluna):

    with coluna:
        st.subheader(titulo)

        if df is None or df.empty:
            st.warning("Dados não disponíveis.")
            return

        tempo_total = df["tempo"].sum()
        tempo_medio = df["tempo"].mean()
        maior_n = df["n"].max()

        st.metric("Tempo Total (h:m:s)", formatar_tempo(tempo_total))
        st.metric("Tempo Médio (ms)", f"{tempo_medio:,.2f}")
        st.metric("Maior n Ordenado", f"{maior_n:,}".replace(",", "."))
        
mostrar_metricas(df_aleatorio, "Aleatória", col1)
mostrar_metricas(df_crescente, "Crescente", col2)
mostrar_metricas(df_decrescente, "Decrescente", col3)

# ==========================================================
# FUNÇÃO PADRONIZADA DE PLOT
# ==========================================================
def plotar_suave(df, titulo):
    x = df["n"].values
    y = df["tempo"].values

    x_novo = np.linspace(x.min(), x.max(), 300)
    spline = make_interp_spline(x, y, k=3)
    y_suave = spline(x_novo)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x_novo, y_suave, linewidth=1)
    ax.set_xlabel("Tamanho do vetor (n)")
    ax.set_ylabel("Tempo de execução (ms)")
    ax.set_title(titulo)
    
    return fig

# ==========================================================
# 2 - GRÁFICOS INDIVIDUAIS
# ==========================================================
st.header("2. Gráficos individuais por tipo de entrada")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div style='text-align: center;'><h5>Aleatória</h5></div>", unsafe_allow_html=True)
    st.pyplot(plotar_suave(df_aleatorio, "HeapSort - Entrada Aleatória"))

with col2:
    st.markdown("<div style='text-align: center;'><h5>Crescente</h5></div>", unsafe_allow_html=True)
    st.pyplot(plotar_suave(df_crescente, "HeapSort - Entrada Crescente"))

with col3:
    st.markdown("<div style='text-align: center;'><h5>Decrescente</h5></div>", unsafe_allow_html=True)
    st.pyplot(plotar_suave(df_decrescente, "HeapSort - Entrada Decrescente"))

# ==========================================================
# FUNÇÃO AUXILIAR PARA SUAVIZAR
# ==========================================================
def suavizar(x, y):
    x_novo = np.linspace(x.min(), x.max(), 300)
    spline = make_interp_spline(x, y, k=3)
    y_suave = spline(x_novo)
    return x_novo, y_suave

# ==========================================================
# 3 - GRÁFICO COMPARATIVO SUAVIZADO
# ==========================================================
st.header("3. Comparação entre os tipos de entrada")

fig, ax = plt.subplots(figsize=(10, 6))

x_a, y_a = suavizar(df_aleatorio["n"].values, df_aleatorio["tempo"].values)
ax.plot(x_a, y_a, label="Aleatório", linewidth=0.75)

x_c, y_c = suavizar(df_crescente["n"].values, df_crescente["tempo"].values)
ax.plot(x_c, y_c, label="Crescente", linewidth=0.75)

x_d, y_d = suavizar(df_decrescente["n"].values, df_decrescente["tempo"].values)
ax.plot(x_d, y_d, label="Decrescente", linewidth=0.75)

ax.set_xlabel("Tamanho do vetor (n)", fontsize=12)
ax.set_ylabel("Tempo de execução (ms)", fontsize=12)
ax.set_title("Comparação do Tempo de Execução do HeapSort", fontsize=14)
ax.legend(fontsize=11)

st.pyplot(fig)

# ==========================================================
# 4 - COMPARAÇÃO DE CRESCIMENTO ASSINTÓTICO
# ==========================================================
st.header("4. Comparação com crescimento assintótico")

fig, ax = plt.subplots(figsize=(10, 6))

x = df_aleatorio["n"].values
y = df_aleatorio["tempo"].values

x_suave = np.linspace(x.min(), x.max(), 400)
ordem = np.argsort(x)
x_ord = x[ordem]
y_ord = y[ordem]

spline = make_interp_spline(x_ord, y_ord, k=3)
y_suave = spline(x_suave)

curva_nlogn = x_suave * np.log2(x_suave)
curva_n2 = x_suave ** 2
curva_nlogn = (curva_nlogn / np.max(curva_nlogn)) * np.max(y_suave)
curva_n2 = (curva_n2 / np.max(curva_n2)) * np.max(y_suave)

x_a, y_a = suavizar(df_aleatorio["n"].values, df_aleatorio["tempo"].values)
ax.plot(x_a, y_a, label="Aleatório", linewidth=0.75)

x_c, y_c = suavizar(df_crescente["n"].values, df_crescente["tempo"].values)
ax.plot(x_c, y_c, label="Crescente", linewidth=0.75)

x_d, y_d = suavizar(df_decrescente["n"].values, df_decrescente["tempo"].values)
ax.plot(x_d, y_d, label="Decrescente", linewidth=0.75)

ax.plot(x_suave, curva_nlogn, linestyle="--", linewidth=1, label="O(n log n)")
ax.plot(x_suave, curva_n2, linestyle="--", linewidth=1, label="O(n²)")

ax.set_xlabel("Tamanho do vetor (n)")
ax.set_ylabel("Tempo de execução (ms)")
ax.set_title("Análise Assintótica do HeapSort")
ax.legend()

st.pyplot(fig)

# ==========================================================
# TEXTO FORMAL PARA ENTREGA
# ==========================================================
st.header("5. 🧾 Análise formal dos resultados")

st.markdown("""
<div style="text-align: justify;">

### 5.1 📏 Comparação entre os Tipos de Entrada

A análise experimental demonstra que o algoritmo HeapSort apresenta comportamento consistente
para os três tipos de entrada analisados, devido à construção determinística do heap.

Observa-se que:

- O tempo de execução segue padrão compatível com O(n log n) para todos os tipos de entrada.
- Entradas crescentes ou decrescentes não afetam o desempenho.
- O algoritmo é eficiente mesmo em grandes volumes de dados, sem degradação.

### 5.2 📦 Impacto do Aumento do Tamanho do Vetor

À medida que o tamanho do vetor aumenta, o tempo de execução cresce de forma previsível,
seguindo O(n log n).

Caso mais elementos fossem inseridos nas sequências, espera-se que:

- O tempo total aumente proporcionalmente a O(n log n).
- A diferença entre os tipos de entrada permaneça mínima.
- O algoritmo continue eficiente independentemente da ordenação inicial.

### 5.3 ✅ Conclusão Experimental
Os resultados empíricos confirmam a complexidade teórica do HeapSort, 
evidenciando que o algoritmo mantém desempenho consistente para diferentes tipos de entrada, 
sejam aleatórios, ordenados de forma crescente ou decrescente. 

Observou-se que o tempo de execução cresce de forma previsível e proporcional a O(n log n), 
mesmo com o aumento do tamanho do vetor. 

Essa estabilidade se deve à construção determinística do heap e à forma como os elementos são reorganizados durante a ordenação. 

Assim, o HeapSort demonstra ser uma solução robusta e confiável para ordenação de grandes volumes de dados, 
oferecendo previsibilidade de desempenho e eficiência consistente independentemente da distribuição inicial dos valores.

</div>
""", unsafe_allow_html=True)