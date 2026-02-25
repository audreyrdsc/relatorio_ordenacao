#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAX_CEPS 60000

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

int main() {

    FILE *f = fopen("../ceps/ceps.txt", "r");
    FILE *out = fopen("ceps_ordenado_quicksort.txt", "w");

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
    // Impressão no mesmo formato do CountingSort
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