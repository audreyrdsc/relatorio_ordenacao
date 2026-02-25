import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Análise de Algoritmos de Ordenação",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"  # <-- Sidebar começa fechada
)

# Cabeçalho com logos e informações
col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    col_left, col_center, col_right = st.columns([1,2,1])
    with col_center:
        st.image("./assets/unifap_logo.jpg", width=40)

with col2:
    st.markdown("""
    <div style="text-align: center;">
        <h3>Universidade Federal do Amapá</h3>
        <h5>Curso: Ciência da Computação</h5>
        <h5>Disciplina: Programação II</h5>
        <h5>Professor: Dr. Júlio Cezar Costa Furtado</h5>
    </div>
    """, unsafe_allow_html=True)
    
with col3:
    col_left, col_center, col_right = st.columns([1,2,1])
    with col_center:
        st.image("./assets/ccc_logo.png", width=100)

st.markdown("<br>", unsafe_allow_html=True)


# Componente da equipe
st.markdown("""
<div style="text-align: center;">
    <h5>👥 Componentes da equipe:</h5>
    <p>
        Audrey Regison dos Santos Cardoso<br>
        João Alexandre Silva do Amaral<br>
        Lucas Santos Pimentel<br>
        Vinícius Santos Aquino Guedes
    </p>
</div>
""", unsafe_allow_html=True)

# Espaço
st.markdown("<br>", unsafe_allow_html=True)

# Título centralizado
st.markdown(
    "<h4 style='text-align: center;'>📈 Análise Experimental de Algoritmos de Ordenação</h4>",
    unsafe_allow_html=True
)

# Espaço
st.markdown("<br>", unsafe_allow_html=True)

# Introdução
st.markdown("""
- Este relatório tem por objetivo proporcionar uma análise experimental comparativa de algoritmos de ordenação,
com base em dados reais coletados durante execuções práticas.

- Os resultados apresentados a seguir foram obtidos a partir de testes realizados com diferentes tipos de entrada, incluindo sequências aleatórias, crescentes, decrescentes e lista de CEPs.
""")

# Espaço
st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
- A análise inclui gráficos comparativos de tempo de execução, bem como uma discussão sobre a complexidade dos algoritmos testados.

- O intuito é fornecer uma visão clara e objetiva do desempenho de cada algoritmo, auxiliando na compreensão de suas características e comportamentos em diferentes cenários.
""")

# Espaço
st.markdown("<br>", unsafe_allow_html=True)

# Lista de algoritmos formatada corretamente
st.markdown("""
##### ⏱ Os algoritmos testados foram:

- 📈 QuickSort com pivô central  
- 📈 QuickSort com pivô aleatório  
- 📈 HeapSort  
- 📈 Counting Sort  
- 📈 Radix Sort  
""")


# TESTES
#if st.button("☰ Alternar Menu"):
#    st.session_state.sidebar_open = not st.session_state.sidebar_open

#st.sidebar.title("☷ 🏠 Menu")

# Inserir imagens de assets
#logo_unifap = st.image("./assets/unifap_logo.jpg", width=200)
#logo_ccc = st.image("./assets/ccc_logo.png", width=200)