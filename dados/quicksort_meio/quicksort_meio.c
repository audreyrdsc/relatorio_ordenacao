#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAX_N 1000000
#define MIN_VAL 1
#define MAX_VAL 1000000

// =====================================================
// QuickSort - pivô sendo o elemento do meio
// =====================================================

//Função principal do QuickSort
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

// Gera vetor aleatório com valores entre MIN_VAL e MAX_VAL
void sort(int v[], int n) {
    quicksort_meio(v, 0, n - 1);
}

// Gera vetor aleatório com valores entre MIN_VAL e MAX_VAL
void gerar_aleatorio(int v[], int n) {
    for (int i = 0; i < n; i++) {
        v[i] = MIN_VAL + rand() % (MAX_VAL - MIN_VAL + 1);
    }
}

// Gera vetor crescente
void gerar_crescente(int v[], int n) {
    for (int i = 0; i < n; i++) {
        v[i] = i + 1;
    }
}

// Gera vetor decrescente
void gerar_decrescente(int v[], int n) {
    for (int i = 0; i < n; i++) {
        v[i] = n - i;
    }
}

int main() {
    static int v[MAX_N];

    srand((unsigned)time(NULL));

    FILE *arquivos[3];
    arquivos[0] = fopen("aleatorio.txt", "w");
    arquivos[1] = fopen("crescente.txt", "w");
    arquivos[2] = fopen("decrescente.txt", "w");

    if (!arquivos[0] || !arquivos[1] || !arquivos[2]) {
        printf("Erro ao criar arquivos.\n");
        return 1;
    }

    for (int tipo = 0; tipo < 3; tipo++) {

        for (int n = 1; n <= MAX_N; n++) {

            if (tipo == 0) {
                printf("Gerando vetor aleatorio de tamanho %d...\n", n);
                gerar_aleatorio(v, n);
            } 
                
            if (tipo == 1) {
                printf("Gerando vetor crescente de tamanho %d...\n", n);
                gerar_crescente(v, n);
            }
            if (tipo == 2) {
                printf("Gerando vetor decrescente de tamanho %d...\n", n);
                gerar_decrescente(v, n);
            }    

            clock_t inicio = clock();
            sort(v, n);
            clock_t fim = clock();

            double tempo_ms = 1000.0 * (double)(fim - inicio) / CLOCKS_PER_SEC;
            

            fprintf(arquivos[tipo], "%d %.6f\n", n, tempo_ms);
        }
    }

    fclose(arquivos[0]);
    fclose(arquivos[1]);
    fclose(arquivos[2]);

    return 0;
}