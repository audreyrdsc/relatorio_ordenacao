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
// Leitura dos CEPs
// =====================================================
int carregar_ceps(const char *nome, int v[]) {

    FILE *f = fopen(nome, "r");
    if (!f) {
        printf("Erro ao abrir ceps.txt\n");
        system("pause");
        return -1;
    }

    int n = 0;
    while (n < MAX_CEPS && fscanf(f, "%d", &v[n]) == 1)
        n++;

    fclose(f);
    return n;
}

// =====================================================
// MAIN – Medição incremental
// =====================================================
int main() {

    static int v_original[MAX_CEPS];
    static int v_trabalho[MAX_CEPS];

    int total = carregar_ceps("../ceps/ceps.txt", v_original);

    if (total <= 0) {
        printf("Erro ao carregar CEPS\n");
        system("pause");
        return 1;
    }

    printf("Lidos %d CEPs para ordenacao.\n", total);

    FILE *out = fopen("ceps_heapsort.txt", "w");
    if (!out) {
        printf("Erro ao criar arquivo de saída\n");
        system("pause");
        return 1;
    }

    fprintf(out, "n tempo_ms\n");

    // ===================================================
    // Loop incremental – curva de crescimento
    // ===================================================
    for (int i = 0; i < total; i++) {

        int tamanho = i + 1;

        // Copiar primeiros 'tamanho' elementos
        for (int j = 0; j < tamanho; j++)
            v_trabalho[j] = v_original[j];

        clock_t inicio = clock();
            sort(v_trabalho, tamanho);
        clock_t fim = clock();

        double tempo_ms =
            1000.0 * (double)(fim - inicio) / CLOCKS_PER_SEC;

        fprintf(out, "%d %.6f\n", tamanho, tempo_ms);
        fflush(out);

        printf("Processando %d/%d\r", i + 1, total);
        fflush(stdout);
    }

    fclose(out);

    printf("\nExperimento HeapSort concluído.\n");
    system("pause");

    return 0;
}