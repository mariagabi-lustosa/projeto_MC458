import random
import csv


def generate_sparse_matrix(n, sparse_percent):
    '''
    Gera uma matriz esparsa n x n com a % de esparsidade dada.
    Retorna uma lista de triplas (i, j, value)
    '''
    total_pos = n*n

    # quantidade de elementos não nulos
    frac = sparse_percent / 100.0
    k = int(total_pos * frac)

    if k == 0 and sparse_percent > 0:
        k = 1

    choosen_pos = set()
    while len(choosen_pos) < k:
        index = random.randrange(total_pos)
        choosen_pos.add(index)

    triples = []
    for index in choosen_pos:
        i = index // n
        j = index % n
        value = random.randint(1, 9)
        triples.append((i,j,value))

    return triples


def sparsity_degree(i):
    '''
    Retorna os graus de esparcidade em %, seguindo as regras:
    - para i = 2, 3 -> 5%, 10%, 20%
    - para i >= 4 -> 1/10^(i+2)%, 1/10^(i+1)%, 1/10^i%
    '''
    if i < 4:
        return [1,5,10,20]
    else:
        return [1/(10**(i+2)), 1/(10**(i+1)), 1/(10**i)]
    

def save_triples_to_csv(triples, n, sparse_percent):
    '''
    Salva uma lista de triplas (i, j, value) em um arquivo CSV.

    Nome do arquivo: sparse_n{n}_p{percent}.csv
    Ex.: n=100, percent=5   -> sparse_n100_p5.csv
         n=10000, percent=1e-06 -> sparse_n10000_p1e-06.csv
    '''

    percent_str = f"{sparse_percent:.10g}"      # string para o percentual no nome do arquivo
    percent_str = percent_str.replace('.', '_') # trocar ponto por underline pra evitar confusão

    filename = f"sparse_n{n}_p{percent_str}.csv"

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['row', 'col', 'value']) # cabeçalho

        for row, col, value in triples:          # dados
            writer.writerow([row, col, value])

    print(f"Arquivo salvo: {filename}")


if __name__ == "__main__":
    i = 2
    n = 10**i

    for d in sparsity_degree(i):
        triples = generate_sparse_matrix(n,d)
        save_triples_to_csv(triples, n, d)