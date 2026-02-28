#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAX_CEPS 60000

// =======================================================
// Carrega CEPS
// =======================================================
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

// =======================================================
// Counting Sort Estável
// =======================================================
void counting_sort(int v[], int n, int min_val, int max_val) {

    int range = max_val - min_val + 1;

    int *count = calloc(range, sizeof(int));
    int *output = malloc(n * sizeof(int));

    if (!count || !output) {
        printf("Erro de memória\n");
        system("pause");
        exit(1);
    }

    for (int i = 0; i < n; i++)
        count[v[i] - min_val]++;

    for (int i = 1; i < range; i++)
        count[i] += count[i - 1];

    for (int i = n - 1; i >= 0; i--) {
        output[count[v[i] - min_val] - 1] = v[i];
        count[v[i] - min_val]--;
    }

    for (int i = 0; i < n; i++)
        v[i] = output[i];

    free(count);
    free(output);
}

// =======================================================
// MAIN – Medição para TODO n
// =======================================================
int main() {

    static int v_original[MAX_CEPS];
    static int v_trabalho[MAX_CEPS];

    int total = carregar_ceps("../ceps/ceps.txt", v_original);

    if (total <= 0) {
        printf("Erro ao carregar CEPS\n");
        system("pause");
        return 1;
    }

    printf("Total de CEPS lidos: %d\n", total);

    FILE *saida = fopen("ceps_ordenado_counting.txt", "w");
    fprintf(saida, "n tempo_ms cep_inserido\n");
    fflush(saida);

    // ===================================================
    // Loop para TODO n de 1 até total
    // ===================================================
    for (int n = 1; n <= total; n++) {

        // Copia primeiros n elementos
        for (int i = 0; i < n; i++)
            v_trabalho[i] = v_original[i];

        // Detectar min e max
        int min_val = v_trabalho[0];
        int max_val = v_trabalho[0];

        for (int i = 1; i < n; i++) {
            if (v_trabalho[i] < min_val) min_val = v_trabalho[i];
            if (v_trabalho[i] > max_val) max_val = v_trabalho[i];
        }

        int range = max_val - min_val + 1;

        clock_t inicio = clock();
            counting_sort(v_trabalho, n, min_val, max_val);
        clock_t fim = clock();

        double tempo_ms =
            1000.0 * (double)(fim - inicio) / CLOCKS_PER_SEC;

        fprintf(saida, "%d %.6f %d\n", n, tempo_ms, v_original[n-1]);
        fflush(saida);

        // Exibir progresso
        printf("Processando %d/%d\r", n, total);
        fflush(stdout);
    }

    fclose(saida);

    printf("\nExperimento concluído.\n");
    system("pause");

    return 0;
}