#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define TOTAL 1000000

void shuffle(int *array, int n) {
    for (int i = n - 1; i > 0; i--) {
        int j = rand() % (i + 1);

        int temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
}

int main() {

    clock_t inicio = clock();   // INÍCIO DA MEDIÇÃO

    printf("Gerando arquivo ceps1000k.txt com %d CEPs unicos...\n", TOTAL);
    FILE *f = fopen("ceps1000k.txt", "w");
    if (f == NULL) {
        printf("Erro ao criar arquivo\n");
        system("pause");
        return 1;
    }

    printf("Alocando memoria para os CEPs...\n");
    int *numeros = malloc(TOTAL * sizeof(int));
    if (numeros == NULL) {
        printf("Erro de alocacao de memoria\n");
        fclose(f);
        system("pause");
        return 1;
    }

    printf("Gerando CEPs aleatorios...\n");
    srand(time(NULL));

    for (int i = 0; i < TOTAL; i++) {

        int primeiro = 1 + rand() % 9;
        int resto = rand() % 10000000;

        numeros[i] = primeiro * 10000000 + resto;
    }

    printf("Embaralhando os CEPs...\n");
    shuffle(numeros, TOTAL);

    printf("Substituindo os dois primeiros digitos por 0 ou 1 e escrevendo no arquivo...\n");
    for (int i = 0; i < TOTAL; i++) {

        int ultimos6 = numeros[i] % 1000000;

        int novo_d1 = rand() % 10;      
        int novo_d2 = 1 + rand() % 9;   

        numeros[i] = novo_d1 * 10000000
                   + novo_d2 * 1000000
                   + ultimos6;

        fprintf(f, "%08d\n", numeros[i]);
    }

    free(numeros);
    fclose(f);

    clock_t fim = clock();   // FIM DA MEDIÇÃO

    double tempo_total = (double)(fim - inicio) / CLOCKS_PER_SEC;

    int segundos = (int)tempo_total;
    int milissegundos = (int)((tempo_total - segundos) * 1000);

    printf("Arquivo ceps1000k.txt criado com sucesso!\n");
    printf("Tempo total de execucao: %d:%03d (s:ms)\n",
           segundos, milissegundos);
    
    system("pause"); // Visualizar o encerramento do programa no Windows

    return 0;
}