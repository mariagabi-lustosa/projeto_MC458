import csv


class HashTable:
    def __init__(self, size):
        # size é a quantidade de buckets (slots) na hashtable
        self.size = size
        # cria uma lista de listas vazias, cada qual servindo como bucket pra armazenar pares chave-valor
        self.hash_table = [[] for _ in range(size)] 


    def set_val(self, key, val):
        # calcula o índice do bucket em que o par chave-valor deve ser armazenado
        hashed_key = hash(key) % self.size 
        # recupera a lista naquele índice
        bucket = self.hash_table[hashed_key] 

        # verificando se a chave ainda está no bucket
        for index, (record_key, _) in enumerate(bucket): 
            if record_key == key:
                bucket[index] = (key, val) # update da chave existente
                return

        # colisões são resolvidas usando chaining (vários pares chave-valor podem coexistir num mesmo bucket)
        bucket.append((key, val))


    def get_val(self, key):
        hashed_key = hash(key) % self.size
        bucket = self.hash_table[hashed_key]
        # encontra o bucket no qual a chave deveria estar

        # procura a chave no bucket
        for record_key, record_val in bucket: 
            if record_key == key:
                return record_val # se encontra, retorna o valor
        return 0                  # para matriz esparsa, posição não armazenada = 0


    def delete_val(self, key):
        # identifica o bucket em que a chave deve existir
        hashed_key = hash(key) % self.size 
        bucket = self.hash_table[hashed_key]

        # procura a chave no valor
        for index, (record_key, _) in enumerate(bucket):
            if record_key == key: # remove o par chave-valor
                bucket.pop(index)
                return


    def __str__(self):
        '''
        itera sobre todos os buckets, convertendo cada um para uma string

        mostra o conteúdo em todos os buckets, tornando mais fácil de visualizar a distribuição de dados e colisões
        '''
        return "".join(str(bucket) for bucket in self.hash_table)


class PairedHashTable:
    '''
    Paired hashmap para matrizes esparsas.

    forward:  (i, j) -> val   (matriz normal A)
    backward: (j, i) -> val   (matriz transposta A^T)
    '''
    def __init__(self, size):
        self.size = size
        self.forward = HashTable(size)
        self.backward = HashTable(size)


    def set_val(self, key, val):
        '''
        key deve ser uma tupla (i, j).
        Atualiza as duas hash tables de forma consistente.
        '''
        i, j = key

        if val == 0:
            # em matrizes esparsas, podemos remover entradas que viram 0
            self.forward.delete_val((i, j))
            self.backward.delete_val((j, i))
        else:
            self.forward.set_val((i, j), val)
            self.backward.set_val((j, i), val)


    def get_val(self, key):
        '''
        A[i, j] normal.
        '''
        return self.forward.get_val(key)


    def get_val_T(self, key):
        '''
        Valor da transposta: A^T[i, j] = A[j, i].
        Aqui usamos a tabela backward diretamente.
        '''
        return self.backward.get_val(key)


    def delete_val(self, key):
        i, j = key
        self.forward.delete_val((i, j))
        self.backward.delete_val((j, i))


    def __str__(self):
        return "forward: " + str(self.forward) + "\nbackward: " + str(self.backward)


def convert_triples_to_paired_hash(triplas):
    '''
    Converte uma lista de triplas (i, j, val) em uma PairedHashTable.
    Isso é O(k), com k = número de elementos não nulos.
    '''
    k = len(triplas)          # quantidade de elementos não nulos
    size = max(1, 2 * k)      # tamanho da hash table

    ht = PairedHashTable(size)

    for i, j, val in triplas:
        if val != 0:          # só para garantir
            ht.set_val((i, j), val)

    return ht


def load_triples_from_csv(filename):
    '''
    Lê um arquivo CSV no formato row,col,value.
    Devolve uma lista de triplas (i, j, val).
    '''
    triples = []
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        header = next(reader, None)  # pula o cabeçalho

        for row in reader:
            if not row:
                continue
            i = int(row[0])
            j = int(row[1])
            val = int(row[2])
            triples.append((i, j, val))

    return triples


'''
Teste com matriz esparsa
'''
if __name__ == "__main__":
    filename = "sparse_n100_p20.csv"

    triples = load_triples_from_csv(filename)
    ht = convert_triples_to_paired_hash(triples)

    # matriz sem transpor
    print("Acessos na matriz A:")
    print(ht.get_val((0, 0)))
    print(ht.get_val((10, 19)))
    print(ht.get_val((40, 90)))

    # matriz transposta
    print("\nAcessos na matriz A^T:")
    print(ht.get_val_T((0, 0)))
    print(ht.get_val_T((19, 10)))
    print(ht.get_val_T((90, 40)))