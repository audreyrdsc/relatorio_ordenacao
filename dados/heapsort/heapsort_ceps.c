#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAX_CEPS 60000

// =====================================================
// Heapify
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

// =====================================================
// HeapSort
// =====================================================
void heapsort(int v[], int n) {

    // Construção do Max-Heap
    for (int i = n / 2 - 1; i >= 0; i--)
        heapify(v, n, i);

    // Extração
    for (int i = n - 1; i > 0; i--) {
        int temp = v[0];
        v[0] = v[i];
        v[i] = temp;

        heapify(v, i, 0);
    }
}

void sort(int v[], int n) {
    heapsort(v, n);
}

// =====================================================
// MAIN
// =====================================================
int main() {

    FILE *f = fopen("../ceps/ceps.txt", "r");
    FILE *out = fopen("ceps_ordenado_heapsort.txt", "w");

    if (!f || !out) {
        printf("Erro ao abrir arquivos.\n");
        system("pause");
        return 1;
    }

    int v[MAX_CEPS];
    int n = 0;

    while (fscanf(f, "%d", &v[n]) != EOF && n < MAX_CEPS)
        n++;

    printf("Lidos %d CEPs para ordenacao.\n", n);

    // =============================
    // Medição de tempo
    // =============================
    clock_t inicio = clock();
    sort(v, n);
    clock_t fim = clock();

    double tempo_ms = 1000.0 * (double)(fim - inicio) / CLOCKS_PER_SEC;

    // =============================
    // Saída no mesmo padrão
    // CEP  n  tempo
    // =============================
    for (int i = 0; i < n; i++) {
        fprintf(out, "%08d %d %.6f\n", v[i], n, tempo_ms);
    }

    fclose(f);
    fclose(out);

    system("pause"); //Visualizar o encerramento do programa no Windows

    return 0;
}