import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

# ==========================================================
# CONFIGURAÇÃO VISUAL PROFISSIONAL
# ==========================================================

st.set_page_config(
    page_title="QuickSort - Pivô Aleatório",
)

plt.style.use("seaborn-v0_8-darkgrid")  

st.markdown(
    "<h2 style='text-align: center;'>📈 Algoritmo QuickSort (Pivô Aleatório)</h2>",
    unsafe_allow_html=True
)

st.markdown(
    "<h3 style='text-align: center;'>🔍 Análise Experimental</h3>",
    unsafe_allow_html=True
) 
    
st.markdown("""
### 🎯 Objetivo

Este relatório apresenta a análise experimental do algoritmo QuickSort,
com escolha de pivô aleatória, utilizando uma sequência aleatória de números inteiros entre `1` e `1.000.000`, para três tipos de entrada:

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
- Pior caso: O(n²)

Com pivô aleatório, a probabilidade de ocorrer partições extremamente
desbalanceadas é significativamente reduzida. Assim, o algoritmo tende
a manter comportamento próximo de O(n log n), independentemente da
ordenação inicial dos dados.
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
    df_aleatorio = carregar_dados("dados/quicksort_aleatorio/aleatorio.txt")
    df_crescente = carregar_dados("dados/quicksort_aleatorio/crescente.txt")
    df_decrescente = carregar_dados("dados/quicksort_aleatorio/decrescente.txt")

    st.success("Arquivos carregados com sucesso!")

except:
    st.error("Erro ao carregar os arquivos. Verifique se estão no mesmo diretório.")
    st.stop()

# ==========================================================
# 1 - MÉTRICAS GERAIS
# ==========================================================
st.header("1. Métricas gerais de execução")

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
        
mostrar_metricas(df_aleatorio, "Entrada Aleatória", col1)
mostrar_metricas(df_crescente, "Entrada Crescente", col2)
mostrar_metricas(df_decrescente, "Entrada Decrescente", col3)

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
    st.markdown("""<div style="text-align: center;"> 
            <h5> Aleatória </h5>
            </div>""", unsafe_allow_html=True)
    st.pyplot(plotar_suave(df_aleatorio, "QuickSort (Pivô Aleatório) - Entrada Aleatória"))

with col2:
    st.markdown("""<div style="text-align: center;"> 
            <h5> Crescente </h5>
            </div>""", unsafe_allow_html=True)
    st.pyplot(plotar_suave(df_crescente, "QuickSort (Pivô Aleatório) - Entrada Crescente"))

with col3:
    st.markdown("""<div style="text-align: center;"> 
            <h5> Decrescente </h5>
            </div>""", unsafe_allow_html=True)
    st.pyplot(plotar_suave(df_decrescente, "QuickSort (Pivô Aleatório) - Entrada Decrescente"))

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

ax.set_xlabel("Tamanho do vetor (n)")
ax.set_ylabel("Tempo de execução (ms)")
ax.set_title("Comparação do Tempo de Execução do QuickSort", fontsize=14)
ax.legend()

st.pyplot(fig)

# ==========================================================
# 4 - COMPARAÇÃO DE CRESCIMENTO ASSINTÓTICO
# ==========================================================
st.header("4. Comparação com crescimento assintótico")

fig, ax = plt.subplots(figsize=(10, 6))

# Dados reais
x = df_aleatorio["n"].values
y = df_aleatorio["tempo"].values

# -------------------------------
# 1️⃣ Curva experimental suavizada
# -------------------------------
x_suave = np.linspace(x.min(), x.max(), 400)

# Garantir que x esteja ordenado
ordem = np.argsort(x)
x_ord = x[ordem]
y_ord = y[ordem]

spline = make_interp_spline(x_ord, y_ord, k=3)
y_suave = spline(x_suave)

# -------------------------------
# 2️⃣ Curvas teóricas
# -------------------------------

# O(n log n)
curva_nlogn = x_suave * np.log2(x_suave)

# O(n²)
curva_n2 = x_suave ** 2

# Normalização para escala comparável
curva_nlogn = (curva_nlogn / np.max(curva_nlogn)) * np.max(y_suave)
curva_n2 = (curva_n2 / np.max(curva_n2)) * np.max(y_suave)

# -------------------------------
# 3️⃣ Plotagem
# -------------------------------

#Aleatório
x_a, y_a = suavizar(df_aleatorio["n"].values, df_aleatorio["tempo"].values)
ax.plot(x_a, y_a, label="Aleatório", linewidth=0.75)

# Crescente
x_c, y_c = suavizar(df_crescente["n"].values, df_crescente["tempo"].values)
ax.plot(x_c, y_c, label="Crescente", linewidth=0.75)

# Decrescente
x_d, y_d = suavizar(df_decrescente["n"].values, df_decrescente["tempo"].values)
ax.plot(x_d, y_d, label="Decrescente", linewidth=0.75)

# Curva O(n log n)
ax.plot(x_suave, curva_nlogn, linestyle="--", linewidth=1, label="O(n log n)")
# Curva O(n²) para comparação
ax.plot(x_suave, curva_n2, linestyle="--", linewidth=1, label="O(n²)")

ax.set_xlabel("Tamanho do vetor (n)")
ax.set_ylabel("Tempo de execução (ms)")
ax.set_title("Análise Assintótica do QuickSort", fontsize=14)
ax.legend()

st.pyplot(fig)

# ==========================================================
# TEXTO FORMAL PARA ENTREGA
# ==========================================================
st.header("5. 🧾 Análise formal dos resultados")

st.markdown("""
<div style="text-align: justify;">

### 5.1 📏 Comparação entre os Tipos de Entrada

Os resultados demonstram que o QuickSort com pivô aleatório
mantém comportamento consistente para os três tipos de entrada.

A aleatorização do pivô reduz significativamente a probabilidade
de partições desbalanceadas, tornando o algoritmo mais estável
mesmo quando os dados já estão ordenados.

### 5.2 📦 Impacto do Aumento do Tamanho do Vetor

À medida que o tamanho do vetor aumenta, o tempo de execução também cresce de forma não linear, apresentando comportamento assintótico compatível com O(n log n) na maioria das execuções práticas, com baixa tendência de degradação para O(n²).

O uso de pivô escolhido aleatoriamente contribui para que as partições tendam, estatisticamente, a ser balanceadas ao longo das chamadas recursivas. Isso reduz significativamente a probabilidade de formação sistemática de subvetores muito desproporcionais, o que mantém a profundidade da recursão próxima de log n.

Caso mais elementos sejam inseridos nas sequências, o crescimento do tempo continuará acompanhando a curva O(n log n), refletindo o aumento simultâneo do custo das partições (proporcional a n) e do número médio de níveis recursivos (proporcional a log n).

### 5.3 ✅ Conclusão

A escolha do pivô aleatório aumenta a robustez do algoritmo,
reduzindo dependência da ordem inicial dos dados e mantendo
desempenho eficiente em larga escala.

Assim, conclui-se que a escolha do pivô aleatório confere maior robustez ao algoritmo, reduzindo a sensibilidade à configuração inicial dos dados e preservando eficiência prática e teórica para grandes volumes de informação.

</div>
""", unsafe_allow_html=True)