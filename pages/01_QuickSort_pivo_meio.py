import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

# ==========================================================
# CONFIGURAÇÃO VISUAL PROFISSIONAL
# ==========================================================
plt.style.use("seaborn-v0_8-darkgrid")

st.title("📊 Análise Experimental do QuickSort com Pivô no Elemento do Meio")
st.markdown("""
### Disciplina: Programação II  
### Experimento: Avaliação de Desempenho do Algoritmo QuickSort

Este relatório apresenta a análise experimental do algoritmo QuickSort
utilizando três tipos de entrada:

- Sequência Aleatória
- Sequência Crescente
- Sequência Decrescente

Os gráficos relacionam:

- **Eixo X:** Tamanho do vetor (n)  
- **Eixo Y:** Tempo de execução (ms)
""")

# ==========================================================
# FUNÇÃO PARA CARREGAR DADOS
# ==========================================================
@st.cache_data
def carregar_dados(nome_arquivo):
    df = pd.read_csv(nome_arquivo, sep=" ", header=None)
    df.columns = ["n", "tempo"]
    return df

df_aleatorio = carregar_dados("dados/quicksort_meio/aleatorio.txt")
df_crescente = carregar_dados("dados/quicksort_meio/crescente.txt")
df_decrescente = carregar_dados("dados/quicksort_meio/decrescente.txt")

# ==========================================================
# MÉTRICAS GERAIS
# ==========================================================
st.header("1. Métricas Gerais de Execução")

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
        st.metric("Tempo Médio (ms)", f"{tempo_medio:,.4f}")
        st.metric("Maior n Ordenado", f"{maior_n:,}")
        
mostrar_metricas(df_aleatorio, "Entrada Aleatória", col1)
mostrar_metricas(df_crescente, "Entrada Crescente", col2)
mostrar_metricas(df_decrescente, "Entrada Decrescente", col3)

# ==========================================================
# FUNÇÃO PADRONIZADA DE PLOT
# ==========================================================
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

def plotar_suave(df, titulo):
    x = df["n"].values
    y = df["tempo"].values

    # Criar mais pontos no eixo X para suavização
    x_novo = np.linspace(x.min(), x.max(), 300)

    # Interpolação spline cúbica
    spline = make_interp_spline(x, y, k=3)
    y_suave = spline(x_novo)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x_novo, y_suave, linewidth=2)
    ax.set_xlabel("Tamanho do vetor (n)")
    ax.set_ylabel("Tempo de execução (ms)")
    ax.set_title(titulo)
    
    return fig



# ==========================================================
# GRÁFICOS INDIVIDUAIS
# ==========================================================
st.header("2. Gráficos Individuais")

col1, col2, col3 = st.columns(3)

with col1:
    st.pyplot(plotar_suave(df_aleatorio, "QuickSort - Entrada Aleatória"))

with col2:
    st.pyplot(plotar_suave(df_crescente, "QuickSort - Entrada Crescente"))

with col3:
    st.pyplot(plotar_suave(df_decrescente, "QuickSort - Entrada Decrescente"))

# ==========================================================
# GRÁFICO COMPARATIVO
# ==========================================================
import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt

# ==========================================================
# FUNÇÃO AUXILIAR PARA SUAVIZAR
# ==========================================================
def suavizar(x, y):
    x_novo = np.linspace(x.min(), x.max(), 300)
    spline = make_interp_spline(x, y, k=3)
    y_suave = spline(x_novo)
    return x_novo, y_suave

# ==========================================================
# GRÁFICO COMPARATIVO SUAVIZADO
# ==========================================================
st.header("3. Comparação Entre os Tipos de Entrada")

fig, ax = plt.subplots(figsize=(10, 6))

# Aleatório
x_a, y_a = suavizar(df_aleatorio["n"].values, df_aleatorio["tempo"].values)
ax.plot(x_a, y_a, label="Aleatório", linewidth=2)

# Crescente
x_c, y_c = suavizar(df_crescente["n"].values, df_crescente["tempo"].values)
ax.plot(x_c, y_c, label="Crescente", linewidth=2)

# Decrescente
x_d, y_d = suavizar(df_decrescente["n"].values, df_decrescente["tempo"].values)
ax.plot(x_d, y_d, label="Decrescente", linewidth=2)

ax.set_xlabel("Tamanho do vetor (n)", fontsize=12)
ax.set_ylabel("Tempo de execução (ms)", fontsize=12)
ax.set_title("Comparação do Tempo de Execução do QuickSort", fontsize=14)
ax.legend(fontsize=11)

st.pyplot(fig)

st.header("4. Comparação com Crescimento Assintótico O(n log n)")

fig, ax = plt.subplots(figsize=(10, 6))

# Dados reais
x = df_aleatorio["n"].values
y = df_aleatorio["tempo"].values

# -------------------------------
# 1️⃣ Curva experimental suavizada
# -------------------------------
x_suave = np.linspace(x.min(), x.max(), 400)
spline = make_interp_spline(x, y, k=3)
y_suave = spline(x_suave)

# -------------------------------
# 2️⃣ Curva teórica O(n log n)
# -------------------------------
curva_teorica = x_suave * np.log2(x_suave)

# Normalização para escala comparável
curva_teorica = (
    curva_teorica / np.max(curva_teorica)
) * np.max(y_suave)

# -------------------------------
# 3️⃣ Plotagem
# -------------------------------
#ax.scatter(x, y, alpha=0.4)  # pontos reais
ax.plot(x_suave, y_suave, linewidth=2, label="Tempo Real (suavizado)")
ax.plot(
    x_suave,
    curva_teorica,
    linestyle="--",
    linewidth=2,
    label="Proporcional a n log n"
)

ax.set_xlabel("Tamanho do vetor (n)")
ax.set_ylabel("Tempo de execução (ms)")
ax.set_title("Análise Assintótica do QuickSort")
ax.legend()

st.pyplot(fig)

# ==========================================================
# TEXTO FORMAL PARA ENTREGA
# ==========================================================
st.header("5. Análise Formal dos Resultados")

st.markdown("""
### 5.1 Comparação entre os Tipos de Entrada

A análise experimental demonstra que o algoritmo QuickSort com pivô no elemento do meio
apresenta comportamento consistente para os três tipos de entrada analisados.

Observa-se que:

- Para entradas aleatórias, o crescimento do tempo segue padrão compatível com O(n log n).
- Para entradas crescentes e decrescentes, não houve degradação significativa do desempenho.
- O pivô central promove partições relativamente equilibradas, evitando o pior caso clássico O(n²).

### 5.2 Impacto do Aumento do Tamanho do Vetor

À medida que o tamanho do vetor aumenta, o tempo de execução cresce de forma não linear,
seguindo aproximadamente o comportamento n log n.

Caso mais elementos fossem inseridos nas sequências, espera-se que:

- O tempo total aumente proporcionalmente a n log n.
- A diferença entre os tipos de entrada permaneça pequena.
- O algoritmo continue eficiente, desde que as partições permaneçam balanceadas.

### 5.3 Conclusão Experimental

Os resultados empíricos confirmam a complexidade média teórica do QuickSort.
A escolha do pivô como elemento central mostrou-se adequada para evitar
desbalanceamentos extremos nas entradas ordenadas.

Assim, conclui-se que o algoritmo apresenta desempenho eficiente
e crescimento assintótico compatível com O(n log n).
""")
