#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAX_CEPS 60000
#define MAX_VAL 100000000

void countingSort(int v[], int n) {
    int *count = calloc(MAX_VAL, sizeof(int));
    int *output = malloc(n * sizeof(int));

    if (count == NULL || output == NULL) {
        printf("Erro de alocacao de memoria.\n");
        exit(1);
    }

    for (int i = 0; i < n; i++)
        count[v[i]]++;

    for (int i = 1; i < MAX_VAL; i++)
        count[i] += count[i - 1];

    for (int i = n - 1; i >= 0; i--) {
        output[count[v[i]] - 1] = v[i];
        count[v[i]]--;
    }

    for (int i = 0; i < n; i++)
        v[i] = output[i];

    free(count);
    free(output);
}

int main() {

    FILE *f = fopen("../ceps/ceps.txt", "r");
    FILE *out = fopen("ceps_ordenado_counting.txt", "w");

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
        countingSort(v, n);
    clock_t fim = clock();

    double tempo_ms = 1000.0 * (double)(fim - inicio) / CLOCKS_PER_SEC;

    // =============================
    // Impressão no mesmo arquivo
    // Formato: CEP  n  tempo
    // =============================
    for (int i = 0; i < n; i++) {
        fprintf(out, "%08d %d %.6f\n", v[i], n, tempo_ms);
    }

    fclose(f);
    fclose(out);

    system("pause"); //Visualizar o encerramento do programa no Windows

    return 0;
}