import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(
    page_title="QuickSort - Estudo Comparativo"
) 

plt.style.use("seaborn-v0_8-darkgrid")

# Título principal
st.markdown("<h2 style='text-align: center;'>📊 Estudo Comparativo do QuickSort</h2>", unsafe_allow_html=True)

# Subtítulo
st.markdown(
    "<h4 style='text-align: center;'>🧾 (Pivô Central vs Pivô Aleatório)</h4>",
    unsafe_allow_html=True
)

# Espaço
st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
Este relatório apresenta a comparação experimental entre:

- QuickSort com pivô central
- QuickSort com pivô aleatório

Para três tipos de entrada:
- Aleatória
- Crescente
- Decrescente
""")

# ==========================================================
# 1 - COMPLEXIDADE TEÓRICA
# ==========================================================

st.header("1. Complexidade Teórica")

st.markdown("""
### QuickSort

- Melhor caso: O(n log n)
- Caso médio: O(n log n)
- Pior caso: O(n²)

A escolha do pivô influencia diretamente o balanceamento das partições.
O pivô aleatório reduz significativamente a probabilidade de ocorrência do pior caso.
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

# Função para plotar gráficos individuais
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

# Título centralizado
st.header("2. Gráficos Individuais")

# Gráficos lado a lado
col1, col2 = st.columns(2)

with col1:
    #st.subheader("QuickSort - Pivô Central")
    st.markdown("""<div style="text-align: center;"> <h5> QuickSort - Pivô Central </h5></div>""", unsafe_allow_html=True)
    grafico_individual(meio, "QuickSort (Pivô Central)")

with col2:
    st.markdown("""<div style="text-align: center;"> <h5> QuickSort - Pivô Aleatório </h5></div>""", unsafe_allow_html=True)
    grafico_individual(aleatorio, "QuickSort - Pivô Aleatório")


# ==========================================================
# 3 - GRÁFICOS COMPARATIVOS POR TIPO DE ENTRADA
# ==========================================================

st.header("3. Comparação entre algoritmos por tipo de entrada")

def grafico_comparativo(tipo):
    fig, ax = plt.subplots(figsize=(10,6))

    # Pivô central
    x1, y1 = suavizar(meio[tipo]["n"].values, meio[tipo]["tempo"].values)
    ax.plot(x1, y1, label="Pivô Central", linewidth=0.75)

    # Pivô aleatório
    x2, y2 = suavizar(aleatorio[tipo]["n"].values, aleatorio[tipo]["tempo"].values)
    ax.plot(x2, y2, label="Pivô Aleatório", linewidth=0.75)

    ax.set_xlabel("Tamanho do vetor (n)")
    ax.set_ylabel("Tempo de execução (ms)")
    ax.set_title(f"Comparação - Entrada {tipo.capitalize()}")
    ax.legend()
    st.pyplot(fig)
    
# Gráficos lado a lado
#st.markdown("""### Diferentes entradas""")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""<div style="text-align: center;"> 
                <h5> Aleatória </h5>
                </div>""", unsafe_allow_html=True)
    grafico_comparativo("aleatorio")

with col2:
    st.markdown("""<div style="text-align: center;"> 
                <h5> Crescente </h5>
                </div>""", unsafe_allow_html=True)
    grafico_comparativo("crescente")

with col3:
    #st.subheader("Decrescente")
    st.markdown("""<div style="text-align: center;"> <h5> Decrescente </h5></div>""", unsafe_allow_html=True)
    grafico_comparativo("decrescente")
    
# ==========================================================
# 4 - ANÁLISE ASSINTÓTICA (ALEATÓRIO COMO REFERÊNCIA)
# ==========================================================
st.header("4. Análise Assintótica - QuickSort")

fig, ax = plt.subplots(figsize=(10,6))

# =========================
# QUICKSort - Pivô Central
# =========================
for tipo in ["aleatorio", "crescente", "decrescente"]:
    
    df = meio[tipo]
    x = df["n"].values
    y = df["tempo"].values
    
    x_suave, y_suave = suavizar(x, y)
    
    ax.plot(x_suave, y_suave,
            linewidth=0.5,
            label=f"Central - {tipo}")

# =========================
# QuickSort - Pivô Aleatório
# =========================
for tipo in ["aleatorio", "crescente", "decrescente"]:
    
    df = aleatorio[tipo]
    x = df["n"].values
    y = df["tempo"].values
    
    x_suave, y_suave = suavizar(x, y)
    
    ax.plot(x_suave, y_suave,
            #linestyle="--",
            linewidth=0.5,
            label=f"Aleatório - {tipo}")

# =========================
# Curvas Assintóticas Teóricas
# =========================

# Usando o maior conjunto como base
df_ref = meio["aleatorio"]
x_ref = df_ref["n"].values
x_suave, _ = suavizar(x_ref, df_ref["tempo"].values)

# O(n log n)
curva_nlogn = x_suave * np.log2(x_suave)
curva_nlogn = (curva_nlogn / np.max(curva_nlogn)) * np.max(df_ref["tempo"].values)
ax.plot(x_suave, curva_nlogn, linestyle="--", label="O(n log n)")

# O(n²)
curva_n2 = x_suave**2
curva_n2 = (curva_n2 / np.max(curva_n2)) * np.max(df_ref["tempo"].values)
ax.plot(x_suave, curva_n2, linestyle="--", label="O(n²)")

# =========================

ax.set_xlabel("Tamanho do vetor (n)")
ax.set_ylabel("Tempo de execução (ms)")
ax.set_title("Comparação Assintótica - QuickSort")
ax.legend()

st.pyplot(fig)

# ==========================================================
# 5 - ANÁLISE FORMAL
# ==========================================================

st.header("5. Análise Comparativa Formal")

st.markdown("""
<div style="text-align: justify;">

<h3>Comparação Geral</h3>

<p>
Observa-se que:
</p>

<ul>
<li>O QuickSort com pivô aleatório apresenta maior estabilidade entre os diferentes tipos de entrada.</li>
<li>O pivô central pode apresentar pequenas variações dependendo da distribuição inicial dos dados.</li>
<li>Em todos os cenários, o crescimento aproxima-se de O(n log n).</li>
</ul>

<h3>Custo adicional do pivô aleatório</h3>

<p>
Quando você usa pivô aleatório, cada chamada recursiva precisa:
</p>

<ul>
<li>Gerar um número aleatório (rand() ou equivalente)</li>
<li>Calcular índice dentro do intervalo</li>
<li>Possivelmente trocar elementos</li>
</ul>

<p>
Isso adiciona overhead constante em cada partição. QuickSort realiza aproximadamente log(n) partições no caso médio. Logo, mesmo um pequeno custo extra por chamada se acumula bastante.
</p>

<p>
O pivô central:
</p>

<ul>
<li>Apenas calcula (inicio + fim)/2</li>
<li>Não chama gerador pseudoaleatório</li>
<li>Tem menos instruções</li>
</ul>

<h3>Conclusão</h3>

<p>
A escolha do pivô é determinante para o desempenho prático do QuickSort, pois afeta diretamente o equilíbrio das partições e, consequentemente, seu comportamento assintótico.
</p>

<p>
Quando se utiliza o elemento central como pivô, o algoritmo pode apresentar bom desempenho em diversos cenários, mas continua suscetível a certos padrões de entrada que geram partições desbalanceadas, aproximando o custo do pior caso O(n²).
</p>

<p>
Em contrapartida, a seleção aleatória do pivô reduz significativamente a probabilidade de divisões muito desiguais, favorecendo partições mais equilibradas e preservando, com maior consistência, o comportamento esperado de O(n log n), independentemente da organização inicial dos dados.
</p>

<p>
Os resultados experimentais confirmam essa análise: o QuickSort com pivô aleatório mostrou menor sensibilidade ao tipo de entrada e maior estabilidade no crescimento do tempo de execução, evidenciando maior robustez frente a diferentes distribuições de dados.
</p>

</div>
""", unsafe_allow_html=True)