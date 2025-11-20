import csv
from collections import defaultdict

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

   def items(self):
       '''
       Itera sobre todos os pares (key, val) armazenados.
       '''
       result = []
       for bucket in self.hash_table:
           for key, val in bucket:
               result.append((key,val))
       return result

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
       Retorna A[i, j], onde key = (i, j).
       Para posições não armazenadas, retorna 0 (matriz esparsa).
       '''
       return self.forward.get_val(key)

   def transpose(self):
       '''
       Matriz transposta está armazenada em backward, então para retornar
       A^T basta ter um objeto que troca as tabelas forward e backward
       de lugar.
       '''
       T = PairedHashTable(self.size)
       T.forward = self.backward # A^T
       T.backward = self.forward # (A^T)^T = A
       return T

   def __str__(self):
       return "forward: " + str(self.forward) + "\nbackward: " + str(self.backward)
  
   def items(self):
       '''
       Retorna lista de ((i,j), valor) da matriz A (não transposta).
       '''
       return self.foward.items()
  
def add_matrix(A, B):
   '''
   C = A + B
   '''
   # obtendo a quantidade de elementos não nulos em A e B
   A_elements = A.forward.items() # lista de ((i,j), val)
   B_elements = B.forward.items()

   kA = len(A_elements)
   kB = len(B_elements)

   worse_k = kA + kB
   len_hash = max(1, 2*worse_k)

   C = PairedHashTable(len_hash)

   # copiando elementos não nulos de A para C
   for (i,j), A_val in A_elements:
       C.set_val((i,j), A_val)

   for (i,j), B_val in B_elements:
       current_val = C.get_val((i,j))
       new_val = current_val + B_val
       C.set_val((i,j), new_val)

   return C

def scalar_mul(alpha, A):
   '''
   C = alpha * A
   '''
   A_elements = A.forward.items()
   k = len(A_elements)

   len_hash = max(1, 2*k)
   C = PairedHashTable(len_hash)

   for (i,j), val in A_elements:
       new_val = alpha * val
       C.set_val((i,j), new_val)
  
   return C

def matrix_mul(A, B):
   '''
   C = A x B


   Aqui, supomos que A e B têm dimensões compatíveis.
   Cada matriz é representada por seus elementos não nulos.
   '''
   # elementos não nulos de A e B
   A_elements = A.forward.items() # lista de ((i, k), valA)
   B_elements = B.forward.items() # lista de ((k, j), valB)

   rows_B = defaultdict(list) # para cada k -> lista de (j, B_val)

   for (k,j), B_val in B_elements:
       rows_B[k].append((j, B_val))

   kA =  len(A_elements)
   total_B = len(B_elements)
   n_rows_B = len(rows_B)

   if n_rows_B > 0:
       dB = total_B / n_rows_B # média de não nulos por linha de B
   else:
       dB = 0

   estimate_kC = int(kA * max(1, dB))
   len_hash_C = max(1, 2 * estimate_kC)

   C = PairedHashTable(len_hash_C)

   # para cada elemento não nulo A[i,k], combina com todos B[k,j] da linha k
   # C[i,j] += A[i,k] * B[k,j]
   for (i,k), A_val in A_elements:
       # pega a linha k de B (se não existir, retorna lista vazia)
       row_B_k = rows_B.get(k, [])

       for j, B_val in row_B_k:
           C_key = (i,j)
           current_val = C.get_val(C_key)
           new_val = current_val + A_val * B_val
           C.set_val(C_key, new_val)

   return C
                
def convert_triples_to_paired_hash(triplas):
   '''
   Converte uma lista de triplas (i, j, val) em uma PairedHashTable.
   Isso é O(k), com k = número de elementos não nulos.
   '''
   k = len(triplas)          # quantidade de elementos não nulos
   size = max(1, 2 * k)      # tamanho da hash table

   ht = PairedHashTable(size)

   for i, j, val in triplas:
       if val != 0:
           ht.set_val((i, j), val)

   return ht