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


def convert_matrix_hashtable(A):
    '''
    Converte uma matriz (lista de listas) em um PairedHashTable.
    Continua sendo O(n^2) para percorrer a matriz,
    mas depois você consegue acessar A e A^T em O(1) por chave.
    '''
    rows = len(A)
    if rows > 0:
        columns = len(A[0])
    else:
        columns = 0

    # quantidade de elementos não nulos
    k = 0 
    for i in range(rows):
        for j in range(columns):
            if A[i][j] != 0:
                k += 1
    
    # escolher o tamanho da hash table
    size = max(1, 2 * k) 

    # agora usamos PairedHashTable
    ht = PairedHashTable(size)

    for i in range(rows):
        for j in range(columns):
            val = A[i][j]
            if val != 0:
                ht.set_val((i, j), val)

    return ht


'''
teste com matriz esparsa
'''
A = [[0, 0, 5],
     [0, 0, 0],
     [7, 0, 0]]

ht = convert_matrix_hashtable(A)

# A sem transpor
print(ht.get_val((0, 2)))  # 5
print(ht.get_val((2, 0)))  # 7
print(ht.get_val((1, 1)))  # 0

# A transposta (usando backward)
print("--- transposta ---")
print(ht.get_val_T((2, 0)))  # A^T[2,0] = A[0,2] = 5
print(ht.get_val_T((0, 2)))  # A^T[0,2] = A[2,0] = 7