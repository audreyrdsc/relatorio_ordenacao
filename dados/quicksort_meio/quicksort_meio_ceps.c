#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAX_CEPS 60000

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
    while (fscanf(f, "%d", &v[n]) == 1)
        n++;

    fclose(f);
    return n;
}

// =====================================================
// QuickSort - pivô sendo o elemento do meio
// =====================================================
void quicksort_meio(int v[], int left, int right) {

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

    if (left < j)
        quicksort_meio(v, left, j);

    if (i < right)
        quicksort_meio(v, i, right);
}

void sort(int v[], int n) {
    quicksort_meio(v, 0, n - 1);
}

// =====================================================
// MAIN – Medição para TODO n
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

    printf("Total de CEPs: %d\n", total);

    FILE *saida = fopen("ceps_quicksort_meio.txt", "w");

    if (!saida) {
        printf("Erro ao criar arquivo de saída\n");
        system("pause");
        return 1;
    }

    fprintf(saida, "n tempo_ms\n");

    // ===================================================
    // Loop incremental para todo n
    // ===================================================
    for (int n = 1; n <= total; n++) {

        // Copiar primeiros n elementos
        for (int i = 0; i < n; i++)
            v_trabalho[i] = v_original[i];

        clock_t inicio = clock();
            sort(v_trabalho, n);
        clock_t fim = clock();

        double tempo_ms =
            1000.0 * (double)(fim - inicio) / CLOCKS_PER_SEC;

        fprintf(saida, "%d %.6f\n", n, tempo_ms);
        fflush(saida);

        printf("Processando %d/%d\r", n, total);
        fflush(stdout);
    }

    fclose(saida);

    printf("\nExperimento QuickSort (pivô central) concluído.\n");
    system("pause");

    return 0;
}