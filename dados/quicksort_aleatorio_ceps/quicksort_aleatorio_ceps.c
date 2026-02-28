#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAX_CEPS 60000

// =====================================================
// Particionamento com pivô aleatório (Lomuto)
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

    srand((unsigned)time(NULL));

    static int v_original[MAX_CEPS];
    static int v_trabalho[MAX_CEPS];

    int total = carregar_ceps("../ceps/ceps.txt", v_original);

    if (total <= 0) {
        printf("Erro ao carregar CEPS\n");
        system("pause");
        return 1;
    }

    printf("Lidos %d CEPs para ordenacao.\n", total);

    FILE *out = fopen("ceps_quicksort_aleatorio.txt", "w");
    if (!out) {
        printf("Erro ao criar arquivo de saída\n");
        system("pause");
        return 1;
    }

    fprintf(out, "n tempo_ms\n");

    // ===================================================
    // Loop incremental para gerar curva de crescimento
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

    printf("\nExperimento QuickSort (pivô aleatório) concluído.\n");
    system("pause");

    return 0;
}