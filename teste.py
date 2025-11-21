import time
import sys
import random
import pandas as pd
import matplotlib.pyplot as plt

# ==============================================================================
# IMPORTAÇÃO DAS ESTRUTURAS (Assumindo que os arquivos estão na mesma pasta)
# ==============================================================================
from estrutura2 import Estrutura2, triples_to_heap
from tradicional import MatrizTradicional
from estrutura1 import PairedHashTable, add_matrix, scalar_mul, matrix_mul, convert_triples_to_paired_hash

# ==============================================================================
# FUNÇÕES AUXILIARES
# ==============================================================================

def generate_sparse_matrix(n, sparse_percent):
    """Gera triplas (i, j, valor) para uma matriz n x n."""
    total_pos = n * n
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
        val = random.randint(1, 9)
        triples.append((i, j, val))

    return triples

def sparsity_degree(i):
    """Define as densidades (%) baseadas na potência i."""
    if i < 4:
        return [1, 5, 10, 20]
    else:
        # Para matrizes muito grandes, a densidade deve ser muito baixa
        return [1/(10**(i+2)), 1/(10**(i+1)), 1/(10**i)]

def medir_tempo(func, *args):
    """Retorna o tempo de execução em segundos."""
    inicio = time.time()
    func(*args)
    fim = time.time()
    return fim - inicio

# ==============================================================================
# EXECUÇÃO DOS TESTES
# ==============================================================================

def rodar_bateria_testes():
    # Dicionário acumulador de resultados
    resultados = {
        'N': [],
        'Densidade': [],
        'Estrutura': [],
        'Operacao': [],
        'Tempo': [],
        'Memoria': []
    }

    # Loop pelas potências de 10. 
    # OBS: range(2, 5) testa N=100, 1.000, 10.000. 
    # Aumentar para 6 ou 7 pode travar na Matriz Tradicional.
    for i in range(2, 7):
        n = 10**i
        graus_esparsidade = sparsity_degree(i)
        graus_esparsidade.sort() # Ordena para o gráfico ficar coerente

        for d in graus_esparsidade:
            print(f"\n>>> Processando: N={n} | Densidade={d}%")

            # 1. Geração dos dados brutos
            triple_A = generate_sparse_matrix(n, d)
            triple_B = generate_sparse_matrix(n, d)
            
            # Amostra de índices para teste de acesso
            indices_teste = [(random.randint(0, n-1), random.randint(0, n-1)) for _ in range(10)]

            # 2. Instanciação das Estruturas
            
            # --- Tradicional ---
            if i < 5:
                trad_A = MatrizTradicional(n, n)
                for t in triple_A: trad_A.inserir(t[0], t[1], t[2])
                trad_B = MatrizTradicional(n, n)
                for t in triple_B: trad_B.inserir(t[0], t[1], t[2])
            else:
                print(f"Erro de Memória na Tradicional para N={n}")
                trad_A = None
                trad_B = None

            # --- Estrutura 1 (Hash) ---
            hash_A = convert_triples_to_paired_hash(triple_A)
            hash_B = convert_triples_to_paired_hash(triple_B)

            # --- Estrutura 2 (Heap) ---
            heap_A = triples_to_heap(triple_A, n)
            heap_B = triples_to_heap(triple_B, n)

            # Lista para iteração
            # Se trad_A for None (estourou memória), removemos da lista de testes deste loop
            lista_estruturas = [
                ('Est. 1 - Hash', hash_A, hash_B),
                ('Est. 2 - Heap', heap_A, heap_B)
            ]
            if trad_A is not None:
                lista_estruturas.insert(0, ('Tradicional', trad_A, trad_B))

            # 3. Execução das Operações
            for nome, A, B in lista_estruturas:
                
                # --- Função auxiliar para salvar no dict ---
                def registrar(op, t, mem=0):
                    resultados['N'].append(n)
                    resultados['Densidade'].append(d)
                    resultados['Estrutura'].append(nome)
                    resultados['Operacao'].append(op)
                    resultados['Tempo'].append(t)
                    resultados['Memoria'].append(mem)

                # --- A. Estimativa de Memória ---
                memoria_est = 0
                if nome == 'Tradicional':
                    # Tamanho da lista externa + (N * tamanho da lista interna)
                    memoria_est = sys.getsizeof(A.data) + (n * sys.getsizeof(A.data[0]))
                elif nome == 'Est. 2 - Heap':
                    # Estimativa grosseira: k * tamanho do objeto nó
                    memoria_est = A.get_k() * 64 
                elif nome == 'Est. 1 - Hash':
                    # Tabelas forward/backward + tuplas
                    memoria_est = (sys.getsizeof(A.forward.hash_table) * 2) + (len(triple_A) * 100)
                
                registrar('Uso de Memória', 0, memoria_est)

                # --- B. Acesso (Leitura) ---
                def test_acesso():
                    for r, c in indices_teste:
                        if 'Hash' in nome:
                            val = A.get_val((r, c))
                        else:
                            val = A.get_val(r, c)
                registrar('Acessar Elemento', medir_tempo(test_acesso))
                print('acesso')
                
                # --- C. Inserção/Update ---
                def test_insercao():
                    for r, c in indices_teste:
                        if 'Hash' in nome:
                            A.set_val((r, c), 99)
                        else:
                            A.inserir(r, c, 99)
                registrar('Inserir Elemento', medir_tempo(test_insercao))
                print('insert')

                # --- D. Transposta ---
                # Obs: Se a operação for in-place, precisamos medir e depois desfazer
                def test_transposta():
                    if 'Hash' in nome:
                        # Hash retorna nova matriz, não é in-place
                        A.transpose()
                    else:
                        # Tradicional e Heap são in-place
                        A.transpor()
                registrar('Transposta', medir_tempo(test_transposta))
                print('transposta')

                # Desfazer alteração para não afetar próximos testes (se in-place)
                if nome != 'Est. 1 - Hash':
                    A.transpor() 

                # --- E. Soma ---
                def test_soma():
                    if 'Hash' in nome:
                        add_matrix(A, B)
                    else:
                        A.somar(B)
                registrar('Soma', medir_tempo(test_soma))
                print('soma')

                # --- F. Multiplicação Escalar ---
                def test_escalar():
                    if 'Hash' in nome:
                        scalar_mul(2.0, A)
                    else:
                        A.multiplicar_por_escalar(2)
                registrar('Mult Escalar', medir_tempo(test_escalar))
                print('escalar')

                # --- G. Multiplicação de Matrizes ---
                # CUIDADO: Tradicional é O(N^3). Pulamos se N > 500 para não travar o script
                pular_mult = (nome == 'Tradicional' and n > 500)
                
                if not pular_mult:
                    def test_mult_matriz():
                        if 'Hash' in nome:
                            matrix_mul(A, B)
                        else:
                            A.multiplicar(B)
                    registrar('Mult Matriz', medir_tempo(test_mult_matriz))
                else:
                    # Registra None ou 0 para indicar que não rodou
                    registrar('Mult Matriz', 0)
                print('mult matriz')

    return pd.DataFrame(resultados)

# ==============================================================================
# GERAÇÃO DOS GRÁFICOS (POR I)
# ==============================================================================

def gerar_graficos_por_i(df):
    """Gera um gráfico para cada N e para cada Operação, variando a densidade."""
    
    dimensoes = df['N'].unique()
    # Ignoramos memória aqui pois a escala é diferente, e ignoramos operações que deram 0 (ex: mult tradicional)
    operacoes = [op for op in df['Operacao'].unique() if op != 'Uso de Memória']

    for n in dimensoes:
        df_n = df[df['N'] == n]
        print(f"Gerando gráficos para Dimensão N={n}...")

        for op in operacoes:
            df_op = df_n[df_n['Operacao'] == op]
            
            # Se todos os tempos forem 0 (ex: Mult Matriz Tradicional pulada), não plota
            if df_op['Tempo'].sum() == 0:
                continue

            plt.figure(figsize=(10, 6))
            
            # Plota uma linha para cada estrutura
            estruturas = df_op['Estrutura'].unique()
            for est in estruturas:
                subset = df_op[df_op['Estrutura'] == est].sort_values(by='Densidade')
                
                # Se tiver dados válidos (tempo > 0)
                if subset['Tempo'].max() > 0:
                    plt.plot(subset['Densidade'], subset['Tempo'], marker='o', label=est)

            plt.title(f"Dimensão N={n} | Operação: {op}")
            plt.xlabel("Densidade da Matriz (%)")
            plt.ylabel("Tempo (segundos)")
            plt.legend()
            plt.grid(True, linestyle='--', alpha=0.7)
            
            # Salva o arquivo
            nome_limpo = op.lower().replace(" ", "_").replace("/", "_")
            nome_arquivo = f"grafico_N{n}_{nome_limpo}.png"
            plt.savefig(nome_arquivo)
            plt.close()

    # --- Gráfico Extra: Memória ---
    # Memória muda com N, mas vamos plotar N vs Memória para uma densidade fixa (ex: a menor)
    # Ou fazer Memória vs Densidade para cada N (como pedido)
    print("Gerando gráficos de memória...")
    for n in dimensoes:
        df_mem = df[(df['N'] == n) & (df['Operacao'] == 'Uso de Memória')]
        
        plt.figure(figsize=(10, 6))
        for est in df_mem['Estrutura'].unique():
            subset = df_mem[df_mem['Estrutura'] == est].sort_values(by='Densidade')
            plt.plot(subset['Densidade'], subset['Memoria'], marker='s', linestyle='--', label=est)
            
        plt.title(f"Dimensão N={n} | Uso de Memória Estimado")
        plt.xlabel("Densidade (%)")
        plt.ylabel("Bytes (Estimado)")
        plt.yscale('log') # Importante pois Tradicional gasta muito mais
        plt.legend()
        plt.grid(True, alpha=0.5)
        plt.savefig(f"grafico_N{n}_memoria.png")
        plt.close()
        
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
    print("--- Iniciando Benchmark Completo ---")
    df_resultado = rodar_bateria_testes()
    
    print("\n--- Tabela de Resultados (Amostra) ---")
    print(df_resultado.head(10))
    df_resultado.to_csv('resultados.csv', index=False)
    
    print("\n--- Gerando Gráficos ---")
    gerar_graficos_por_i(df_resultado)
    gerar_graficos_separados(df_resultado)
    
    print("\nConcluído! Verifique os arquivos .png na pasta.")