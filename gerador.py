import time
import sys
import random
import pandas as pd
import matplotlib.pyplot as plt

# Importação das estruturas
from estrutura2 import Estrutura2, triples_to_heap
from tradicional import MatrizTradicional
from estrutura1 import PairedHashTable, add_matrix, scalar_mul, matrix_mul, convert_triples_to_paired_hash

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

def medir_tempo(func, *args):
    """Executa uma função e retorna o tempo decorrido."""
    inicio = time.time()
    func(*args)
    fim = time.time()
    return fim - inicio

# --- O Experimento Principal ---

def rodar_bateria_testes():
    for i in range(2,7):
        n = 10**i
        for d in sparsity_degree(i):
            triples = generate_sparse_matrix(n,d)
            
            resultados = {
                'N': [],
                'Estrutura': [],
                'Operacao': [],
                'Tempo': [],
                'Memoria': []
            }

            print(f"--- Iniciando Bateria de Testes (Densidade: {d}%) ---")
            print(f"\n>> Processando Matriz {n}x{n}...")
            
            # 1. Gerar Dados
            triple_A = generate_sparse_matrix(n,d)
            triple_B = generate_sparse_matrix(n,d)
            
            # Índices aleatórios para teste de acesso/inserção
            indices_teste = [(random.randint(0, n-1), random.randint(0, n-1)) for _ in range(20)]

            # ====================================================
            # PREPARAÇÃO DAS ESTRUTURAS
            # ====================================================
            
            # --- Tradicional ---
            trad_A = MatrizTradicional(n, n)
            for t in triple_A:
                trad_A.inserir(t[0],t[1],t[2])
                
            trad_B = MatrizTradicional(n, n)
            for t in triple_B:
                trad_B.inserir(t[0],t[1],t[2])
                
            # --- Estrutura 1 ---
            hash_A = convert_triples_to_paired_hash(triple_A)
            hash_B = convert_triples_to_paired_hash(triple_B)


            # --- Estrutura 2 ---
            heap_A = triples_to_heap(triple_A, n)
            heap_B = triples_to_heap(triple_B, n)

            estruturas = [
                ('Tradicional', trad_A, trad_B),
                ('Estrutura 1 - Hash', hash_A, hash_B),
                ('Estrutura 2 - Heap', heap_A, heap_B)
            ]

            for nome, A, B in estruturas:
                memoria_est = 0
                
                # ====================================================
                # 1. MEMÓRIA (Estimativa)
                # ====================================================
                if nome == 'Tradicional':
                    memoria_est = sys.getsizeof(A.data) + (n * sys.getsizeof(A.data[0]))
                elif nome == 'Estrutura 2 - Heap':
                    # Estimativa: k nós * ~64 bytes por nó (objeto python)
                    memoria_est = A.get_k() * 64 
                elif nome == 'Estrutura 1 - Hash':
                    # Tabelas forward + backward (listas de listas)
                    # Muito aproximado: tamanho da lista bucket + tuplas armazenadas
                    memoria_est = (sys.getsizeof(A.forward.hash_table) * 2) + (len(triple_A) * 100)
                
                # Registra memória (apenas uma vez por N)
                resultados['N'].append(n)
                resultados['Estrutura'].append(nome)
                resultados['Operacao'].append('Uso de Memória')
                resultados['Tempo'].append(0) # Irrelevante aqui
                resultados['Memoria'].append(memoria_est)

                # ====================================================
                # 2. ACESSAR ELEMENTO (Média de k acessos)
                # ====================================================
                def test_acesso():
                    for r, c in indices_teste:
                        if nome == 'Estrutura 1 - Hash':
                            A.get_val((r, c))
                        else:
                            A.get_val(r, c)
                
                t = medir_tempo(test_acesso)
                resultados['N'].append(n)
                resultados['Estrutura'].append(nome)
                resultados['Operacao'].append('Acessar Elemento')
                resultados['Tempo'].append(t)
                resultados['Memoria'].append(0)

                # ====================================================
                # 3. INSERIR/ATUALIZAR (Média de k inserções)
                # ====================================================
                def test_insercao():
                    for r, c in indices_teste:
                        val = 50
                        if nome == 'Estrutura 1 - Hash':
                            A.set_val((r, c), val)
                        else:
                            A.inserir(r, c, val)

                t = medir_tempo(test_insercao)
                resultados['N'].append(n)
                resultados['Estrutura'].append(nome)
                resultados['Operacao'].append('Inserir/Atualizar')
                resultados['Tempo'].append(t)
                resultados['Memoria'].append(0)

                # ====================================================
                # 4. TRANSPOSTA
                # ====================================================
                def test_transposta():
                    if nome == 'Tradicional':
                        # Tradicional faz in-place, então fazemos cópia para não estragar testes futuros
                        # Mas como medimos só o tempo da op, tudo bem
                        # Vamos instanciar nova pra ser justo com Hash que retorna nova
                        
                        # (Simplificação: rodamos o método transpor direto no objeto)
                        A.transpor() 
                        A.transpor() # Destranspõe para voltar ao normal
                    elif nome == 'Estrutura 2 - Heap':
                        A.transpor()
                        A.transpor() # Volta ao normal
                    elif nome == 'Estrutura 1 - Hash':
                        A.transpose() # Retorna nova, não altera in-place

                t = medir_tempo(test_transposta)
                resultados['N'].append(n)
                resultados['Estrutura'].append(nome)
                resultados['Operacao'].append('Transposta')
                resultados['Tempo'].append(t)
                resultados['Memoria'].append(0)

                # ====================================================
                # 5. SOMA DE MATRIZES (A + B)
                # ====================================================
                def test_soma():
                    if nome == 'Estrutura 1 - Hash':
                        add_matrix(A, B)
                    else:
                        A.somar(B)

                t = medir_tempo(test_soma)
                resultados['N'].append(n)
                resultados['Estrutura'].append(nome)
                resultados['Operacao'].append('Soma')
                resultados['Tempo'].append(t)
                resultados['Memoria'].append(0)

                # ====================================================
                # 6. MULTIPLICAÇÃO POR ESCALAR (A * 2.0)
                # ====================================================
                def test_escalar():
                    if nome == 'Estrutura 1 - Hash':
                        scalar_mul(2.0, A)
                    else:
                        A.multiplicar_por_escalar(2)

                t = medir_tempo(test_escalar)
                resultados['N'].append(n)
                resultados['Estrutura'].append(nome)
                resultados['Operacao'].append('Mult Escalar')
                resultados['Tempo'].append(t)
                resultados['Memoria'].append(0)

                # ====================================================
                # 7. MULTIPLICAÇÃO DE MATRIZES (A x B)
                # ====================================================
                def test_mult_matriz():
                    if nome == 'Estrutura 1 - Hash':
                        # Hash requer B transposta para otimização eficiente no algoritmo fornecido?
                        # O algoritmo fornecido usa B.forward.items() iterando linhas de B.
                        # O exemplo no main do hashmap usava matrix_mul(A, B.transpose()). 
                        # Vamos usar padrão A * B.
                        matrix_mul(A, B) 
                    else:
                        A.multiplicar(B)
            
                t = medir_tempo(test_mult_matriz)
                resultados['N'].append(n)
                resultados['Estrutura'].append(nome)
                resultados['Operacao'].append('Mult Matriz')
                resultados['Tempo'].append(t)
                resultados['Memoria'].append(0)

    return pd.DataFrame(resultados)

# --- Geração dos Gráficos ---

def gerar_graficos_separados(df):
    # Lista das operações (exceto memória que é separada)
    operacoes = [op for op in df['Operacao'].unique() if op != 'Uso de Memória']
    
    # 1. Gráfico de Memória
    df_mem = df[df['Operacao'] == 'Uso de Memória']
    plt.figure(figsize=(8, 5))
    for est in df_mem['Estrutura'].unique():
        subset = df_mem[df_mem['Estrutura'] == est]
        plt.plot(subset['N'], subset['Memoria'], marker='o', label=est)
    
    plt.title("Comparação: Uso de Memória Estimado")
    plt.xlabel("Dimensão da Matriz (N)")
    plt.ylabel("Bytes (Log Scale)")
    plt.yscale('log') # Escala logarítmica pois tradicional explode rápido
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.tight_layout()
    plt.savefig("comparacao_memoria.png")
    print("Gerado: comparacao_memoria.png")
    plt.close()

    # 2. Gráficos de Tempo (Um por operação)
    for op in operacoes:
        df_op = df[df['Operacao'] == op]
        plt.figure(figsize=(8, 5))
        
        for est in df_op['Estrutura'].unique():
            subset = df_op[df_op['Estrutura'] == est]
            plt.plot(subset['N'], subset['Tempo'], marker='o', label=est)
        
        plt.title(f"Desempenho: {op}")
        plt.xlabel("Dimensão da Matriz (N)")
        plt.ylabel("Tempo (segundos)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        
        # Sanitiza nome do arquivo
        nome_arq = f"comparacao_{op.lower().replace(' ', '_').replace('/', '_')}.png"
        plt.savefig(nome_arq)
        print(f"Gerado: {nome_arq}")
        plt.close()

if __name__ == "__main__":
    df = rodar_bateria_testes()
    print("\n--- DADOS BRUTOS (Amostra) ---")
    print(df.head(15))
    
    gerar_graficos_separados(df)
    print("\nTodos os gráficos foram gerados com sucesso.")