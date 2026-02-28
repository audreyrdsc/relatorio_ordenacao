#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAX_CEPS 60000
#define BASE 10

// =======================================================
// Leitura dos CEPs
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
// Counting Sort ESTÁVEL por dígito (usado no Radix)
// =======================================================
void counting_sort_digito(int v[], int n, int exp) {

    static int output[MAX_CEPS];
    int count[BASE] = {0};

    for (int i = 0; i < n; i++) {
        int digito = (v[i] / exp) % 10;
        count[digito]++;
    }

    for (int i = 1; i < BASE; i++)
        count[i] += count[i - 1];

    for (int i = n - 1; i >= 0; i--) {
        int digito = (v[i] / exp) % 10;
        output[count[digito] - 1] = v[i];
        count[digito]--;
    }

    for (int i = 0; i < n; i++)
        v[i] = output[i];
}

// =======================================================
// Radix Sort
// =======================================================
void radix_sort(int v[], int n) {

    int max = v[0];
    for (int i = 1; i < n; i++)
        if (v[i] > max)
            max = v[i];

    for (int exp = 1; max / exp > 0; exp *= 10)
        counting_sort_digito(v, n, exp);
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

    printf("Total de CEPs: %d\n", total);

    FILE *saida = fopen("ceps_ordenado_radix.txt", "w");
    fprintf(saida, "n tempo_ms\n");

    for (int n = 1; n <= total; n++) {

        for (int i = 0; i < n; i++)
            v_trabalho[i] = v_original[i];

        clock_t inicio = clock();
            radix_sort(v_trabalho, n);
        clock_t fim = clock();

        double tempo_ms =
            1000.0 * (double)(fim - inicio) / CLOCKS_PER_SEC;

        fprintf(saida, "%d %.6f\n", n, tempo_ms);
        fflush(saida);

        printf("Processando %d/%d\r", n, total);
        fflush(stdout);
    }

    fclose(saida);

    printf("\nExperimento Radix concluido.\n");
    system("pause");

    return 0;
}