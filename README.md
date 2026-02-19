# ANÁLISE EXPERIMENTAL DE ALGORITMOS DE ORDENAÇÃO

## 1. Identificação

**Instituição:** Universidade Federal do Amapá (UNIFAP)  
**Curso:** Ciência da Computação  
**Disciplina:** Programação II  
**Docente:** Prof. Júlio Cezar Costa Furtado  

**Discentes:**
- Audrey Regison dos Santos Cardoso  
- João Alexandre Silva do Amaral  
- Lucas Santos Pimentel  
- Vinícius Santos Aquino Guedes  

---

## 2. Resumo

Este trabalho apresenta a implementação e a análise experimental de algoritmos clássicos de ordenação, com ênfase na comparação de desempenho empírico e comportamento assintótico.

Foram avaliados os algoritmos QuickSort (com diferentes estratégias de pivô), HeapSort, CountingSort e RadixSort, considerando diferentes distribuições de entrada e conjuntos de dados reais (CEPs). Os resultados experimentais foram comparados com suas respectivas complexidades teóricas.

---

## 3. Objetivos

### 3.1 Objetivo Geral

Avaliar experimentalmente o desempenho de algoritmos de ordenação e verificar sua aderência às complexidades assintóticas esperadas.

### 3.2 Objetivos Específicos

- Implementar algoritmos de ordenação em Python e C.
- Comparar estratégias distintas do QuickSort.
- Avaliar desempenho em entradas:
  - Aleatórias
  - Ordenadas crescentes
  - Ordenadas decrescentes
- Comparar algoritmos baseados em comparação e algoritmos lineares.
- Analisar crescimento experimental em relação à função \( O(n \log n) \).
- Aplicar algoritmos em base real de CEPs.

---

## 4. Fundamentação Teórica

Os algoritmos analisados possuem as seguintes complexidades assintóticas:

- **QuickSort (caso médio):** \( O(n \log n) \)
- **QuickSort (pior caso):** \( O(n^2) \)
- **HeapSort:** \( O(n \log n) \)
- **CountingSort:** \( O(n + k) \)
- **RadixSort:** \( O(d(n + k)) \)

Onde:
- \( n \) representa o número de elementos
- \( k \) representa o intervalo de valores
- \( d \) representa o número de dígitos

---

## 5. Metodologia

Os experimentos foram conduzidos da seguinte forma:

1. Geração de sequências com tamanhos crescentes.
2. Execução múltipla dos algoritmos para coleta de tempo médio.
3. Armazenamento dos resultados em logs.
4. Visualização gráfica utilizando Streamlit.
5. Comparação com curvas teóricas normalizadas.

Os testes foram realizados considerando diferentes tipos de entrada para avaliar impacto no desempenho.

---

## 6. Estrutura do Projeto
├── app.py  # Aplicação principal (Streamlit)
├── pages/  # Páginas dos experimentos
├── dados/  # Implementações e resultados
│ └── ceps/ # Base de dados utilizada
├── docs/   # Orientações e documentação
├── assets/ # Logotipos institucionais
├── requirements.txt
└── .gitignore
---

## 7. Tecnologias Utilizadas

- Linguagem C
- Linguagem Python
- Matplotlib
- Streamlit
- Pandas
- NumPy
- SciPy
- Plotly
- Git e GitHub

---

## 8. Ambiente de Execução

### 8.1 Criação do ambiente virtual

```bash
python -m venv .venv             # Criação do ambiente virtual
.\.venv\Scripts\Activate.ps1     # Ativação do ambiente virtual
pip install -r requirements.txt  # Instalação das bibliotecas
streamlit run app.py             # Comando para execução da aplicação
http://localhost:8501            # Exibição local
```

### 8.2 Repositório da Aplicação
```bash
https://github.com/audreyrdsc/relatorio_ordenacao.git
```



