#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAX_CEPS 60000

// =====================================================
// Particionamento com pivô aleatório
// =====================================================
int particiona(int v[], int left, int right) {

    int indice_pivo = left + rand() % (right - left + 1);
    int pivo = v[indice_pivo];

    // Move pivô para o final
    int temp = v[indice_pivo];
    v[indice_pivo] = v[right];
    v[right] = temp;

    int i = left - 1;

    for (int j = left; j < right; j++) {
        if (v[j] <= pivo) {
            i++;
            temp = v[i];
            v[i] = v[j];
            v[j] = temp;
        }
    }

    // Coloca pivô na posição correta
    temp = v[i + 1];
    v[i + 1] = v[right];
    v[right] = temp;

    return i + 1;
}

// =====================================================
// QuickSort recursivo
// =====================================================
void quicksort_aleatorio(int v[], int left, int right) {
    if (left < right) {
        int pi = particiona(v, left, right);
        quicksort_aleatorio(v, left, pi - 1);
        quicksort_aleatorio(v, pi + 1, right);
    }
}

void sort(int v[], int n) {
    quicksort_aleatorio(v, 0, n - 1);
}

// =====================================================
// MAIN
// =====================================================
int main() {

    srand((unsigned)time(NULL));

    FILE *f = fopen("../ceps/ceps.txt", "r");
    FILE *out = fopen("ceps_ordenado_quicksort_aleatorio.txt", "w");

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
    // Saída no mesmo padrão do CountingSort
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