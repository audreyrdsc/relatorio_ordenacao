import streamlit as st

st.set_page_config(
    page_title="Análise Experimental de Algoritmos",
    layout="wide"
)

st.title("Sistema de Análise Experimental de Algoritmos de Ordenação")

st.markdown("""# 📚
## Disciplina: Programação II  
## Curso: Ciência da Computação  

Este sistema permite a análise experimental comparativa de algoritmos de ordenação,
com base em dados reais coletados durante execuções práticas.

Selecione uma opção abaixo para visualizar os resultados.
""")

#opcao = st.radio(
#    "Selecione o experimento desejado:",
#    [
#        "QuickSort com pivô central",
#        "QuickSort com pivô aleatório",
#        "Comparação (QuickSort pivô central vs aleatório)",
#        "HeapSort",
#        "Comparação (QuickSort vs HeapSort)",
#        "CountingSort",
#        "RadixSort",
#        "Comparação (CountingSort vs RadixSort)",
#        "Comparação Geral (CountingSort vs RadixSort vs QuickSort vs HeapSort - CEPS)"
#    ]
#)

#st.divider()

#if opcao == "QuickSort com pivô central":
#    st.switch_page("quicksort_meio.py")

#elif opcao == "QuickSort com pivô aleatório":
#    st.switch_page("quicksort_aleatorio.py")

#elif opcao == "Comparação (QuickSort pivô central vs aleatório)":
#    st.switch_page("comparacao_qs.py")

#elif opcao == "HeapSort":
#    st.switch_page("heapsort.py")

#elif opcao == "Comparação (QuickSort vs HeapSort)":
#    st.switch_page("comparacao_qs_heap.py")

#elif opcao == "CountingSort":
#    st.switch_page("countingsort.py")

#elif opcao == "RadixSort":
#    st.switch_page("radixsort.py")

#elif opcao == "Comparação (CountingSort vs RadixSort)":
#    st.switch_page("comparacao_counting_radix.py")

#elif opcao == "Comparação Geral (CountingSort vs RadixSort vs QuickSort vs HeapSort - CEPS)":
#    st.switch_page("comparacao_geral_ceps.py")