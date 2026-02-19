#include <stdio.h>
#include <stdlib.h>
#include <time.h>

Preparar versão definitiva para MAX_N = 1.000.000

#define MAX_N 100 //1000000
#define MIN_VAL 1
#define MAX_VAL 100 //1000000

// =====================================================
// HeapSort
// =====================================================

void heapify(int v[], int n, int i) {
    int maior = i;
    int esquerda = 2 * i + 1;
    int direita = 2 * i + 2;

    if (esquerda < n && v[esquerda] > v[maior])
        maior = esquerda;

    if (direita < n && v[direita] > v[maior])
        maior = direita;

    if (maior != i) {
        int temp = v[i];
        v[i] = v[maior];
        v[maior] = temp;

        heapify(v, n, maior);
    }
}

void heapsort(int v[], int n) {

    // Construção do heap (max-heap)
    for (int i = n / 2 - 1; i >= 0; i--)
        heapify(v, n, i);

    // Extração dos elementos
    for (int i = n - 1; i > 0; i--) {
        int temp = v[0];
        v[0] = v[i];
        v[i] = temp;

        heapify(v, i, 0);
    }
}

// Garante que a subárvore com raiz em i seja um max-heap
void sort(int v[], int n) {
    heapsort(v, n);
}

// Gera vetor aleatório com valores entre MIN_VAL e MAX_VAL
void gerar_aleatorio(int v[], int n) {
    for (int i = 0; i < n; i++) {
        v[i] = MIN_VAL + rand() % (MAX_VAL - MIN_VAL + 1);
    }
}

// Gera vetor crescente
void gerar_crescente(int v[], int n) {
    for (int i = 0; i < n; i++) {
        v[i] = i + 1;
    }
}

// Gera vetor decrescente
void gerar_decrescente(int v[], int n) {
    for (int i = 0; i < n; i++) {
        v[i] = n - i;
    }
}

int main() {
    static int v[MAX_N];

    srand((unsigned)time(NULL));

    FILE *arquivos[3];
    arquivos[0] = fopen("aleatorio.txt", "w");
    arquivos[1] = fopen("crescente.txt", "w");
    arquivos[2] = fopen("decrescente.txt", "w");

    if (!arquivos[0] || !arquivos[1] || !arquivos[2]) {
        printf("Erro ao criar arquivos.\n");
        return 1;
    }

    for (int tipo = 0; tipo < 3; tipo++) {

        for (int n = 1; n <= MAX_N; n++) {

            if (tipo == 0) gerar_aleatorio(v, n);
            if (tipo == 1) gerar_crescente(v, n);
            if (tipo == 2) gerar_decrescente(v, n);

            clock_t inicio = clock();
            sort(v, n);
            clock_t fim = clock();

            double tempo_ms = 1000.0 * (double)(fim - inicio) / CLOCKS_PER_SEC;

            fprintf(arquivos[tipo], "%d %.6f\n", n, tempo_ms);
        }
    }

    fclose(arquivos[0]);
    fclose(arquivos[1]);
    fclose(arquivos[2]);

    return 0;
}