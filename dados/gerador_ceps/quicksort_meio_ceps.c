#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAX_CEPS 1000000

// =====================================================
// QuickSort otimizado (reduz profundidade de recursão)
// =====================================================
void quicksort_meio(int v[], int left, int right) {

    while (left < right) {

        int i = left;
        int j = right;
        int pivo = v[(left + right) / 2];

        while (i <= j) {

            while (v[i] < pivo) i++;
            while (v[j] > pivo) j--;

            if (i <= j) {
                int temp = v[i];
                v[i] = v[j];
                v[j] = temp;
                i++;
                j--;
            }
        }

        // Chama recursivamente apenas a menor partição
        if ((j - left) < (right - i)) {
            if (left < j)
                quicksort_meio(v, left, j);
            left = i;
        } else {
            if (i < right)
                quicksort_meio(v, i, right);
            right = j;
        }
    }
}

void sort(int v[], int n) {
    quicksort_meio(v, 0, n - 1);
}

int main() {

    FILE *f = fopen("ceps1000k.txt", "r");
    FILE *out = fopen("ceps_ordenado_quicksort.txt", "w");

    if (!f || !out) {
        printf("Erro ao abrir arquivos.\n");
        getchar();
        return 1;
    }

    // =============================
    // ALOCAÇÃO NO HEAP (corrige stack overflow)
    // =============================
    int *v = malloc(MAX_CEPS * sizeof(int));
    if (!v) {
        printf("Erro de alocacao de memoria.\n");
        fclose(f);
        fclose(out);
        getchar();
        return 1;
    }

    int n = 0;

    while (n < MAX_CEPS && fscanf(f, "%d", &v[n]) == 1)
        n++;

    printf("Lidos %d CEPs para ordenacao.\n", n);

    if (n == 0) {
        printf("Nenhum dado lido.\n");
        free(v);
        fclose(f);
        fclose(out);
        getchar();
        return 1;
    }

    // =============================
    // Medição de tempo
    // =============================
    clock_t inicio = clock();
    sort(v, n);
    clock_t fim = clock();

    double tempo_ms = 1000.0 * (double)(fim - inicio) / CLOCKS_PER_SEC;

    printf("Ordenacao concluida.\n");
    printf("Tempo: %.3f ms\n", tempo_ms);

    // =============================
    // Impressão no arquivo
    // =============================
    for (int i = 0; i < n; i++) {
        fprintf(out, "%08d %d %.6f\n", v[i], n, tempo_ms);
    }

    fclose(f);
    fclose(out);
    free(v);

    printf("Arquivo ceps_ordenado_quicksort.txt criado com sucesso.\n");

    printf("Pressione ENTER para sair...");
    getchar();  // pausa segura

    return 0;
}