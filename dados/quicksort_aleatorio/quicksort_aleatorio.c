#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAX_N 1000000
#define MIN_VAL 1
#define MAX_VAL 1000000

// =====================================================
// QuickSort - pivô aleatório
// =====================================================

// Particiona o vetor usando um pivô aleatório e retorna o índice do pivô
int particiona(int v[], int left, int right) {

    int indice_pivo = left + rand() % (right - left + 1);
    int pivo = v[indice_pivo];

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

    temp = v[i + 1];
    v[i + 1] = v[right];
    v[right] = temp;

    return i + 1;
}

// Função principal do QuickSort
void quicksort_aleatorio(int v[], int left, int right) {
    if (left < right) {
        int pi = particiona(v, left, right);
        quicksort_aleatorio(v, left, pi - 1);
        quicksort_aleatorio(v, pi + 1, right);
    }
}

// Gera vetor aleatório com valores entre MIN_VAL e MAX_VAL
void sort(int v[], int n) {
    quicksort_aleatorio(v, 0, n - 1);
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