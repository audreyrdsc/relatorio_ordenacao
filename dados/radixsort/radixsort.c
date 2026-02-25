#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAX_CEPS 60000
#define BASE 10

// ======================================================
// CountingSort estável por dígito (usado pelo RadixSort)
// ======================================================
void countingSortDigit(int v[], int n, int exp) {

    int *output = malloc(n * sizeof(int));
    int count[BASE] = {0};

    if (output == NULL) {
        printf("Erro de alocacao de memoria.\n");
        exit(1);
    }

    // Contagem das ocorrências do dígito atual
    for (int i = 0; i < n; i++) {
        int digito = (v[i] / exp) % 10;
        count[digito]++;
    }

    // Soma acumulada
    for (int i = 1; i < BASE; i++)
        count[i] += count[i - 1];

    // Construção estável (percorrendo de trás para frente)
    for (int i = n - 1; i >= 0; i--) {
        int digito = (v[i] / exp) % 10;
        output[count[digito] - 1] = v[i];
        count[digito]--;
    }

    // Copiar para o vetor original
    for (int i = 0; i < n; i++)
        v[i] = output[i];

    free(output);
}

// ======================================================
// RadixSort principal
// ======================================================
void radixSort(int v[], int n) {

    // Encontrar o maior valor
    int max = v[0];
    for (int i = 1; i < n; i++)
        if (v[i] > max)
            max = v[i];

    // Processar cada dígito (base 10)
    for (int exp = 1; max / exp > 0; exp *= 10)
        countingSortDigit(v, n, exp);
}

int main() {

    FILE *f = fopen("../ceps/ceps.txt", "r");
    FILE *out = fopen("ceps_ordenado_radix.txt", "w");

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
    radixSort(v, n);
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