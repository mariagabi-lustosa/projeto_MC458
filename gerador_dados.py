import time
import sys
import random
import pandas as pd
import matplotlib.pyplot as plt
from estrutura_2_teste import Estrutura2, No, Arvore, MatrizTradicional

# --- IMPORTANTE: ---
# Certifique-se de que suas classes Estrutura2, Arvore, No e MatrizTradicional 
# estão coladas aqui em cima ou importadas de outro arquivo.
# from seu_arquivo import Estrutura2, MatrizTradicional 

# --- Funções Auxiliares ---

def gerar_dados_aleatorios(n, m, densidade):
    # gera uma lista de triplas (i, j, valor) para popular as matrizes
    k = int(n * m * densidade)
    dados = []
    elementos_vistos = set()
    
    while len(dados) < k:
        i = random.randint(0, n - 1)
        j = random.randint(0, m - 1)
        if (i, j) not in elementos_vistos:
            val = random.uniform(1, 100)
            dados.append((i, j, val))
            elementos_vistos.add((i, j))
    return dados

def popular_matriz_esparsa(matriz, dados):
    for i, j, val in dados:
        matriz.inserir(i, j, val)

def popular_matriz_densa(matriz, dados):
    for i, j, val in dados:
        matriz.inserir(i, j, val) # ja que que MatrizTradicional tem "inserir(i, j, val)"

# --- O Experimento ---

def rodar_experimento():
    # 1. Configurações do Teste
    tamanhos = [10, 50, 100, 200, 500] # N x N (Cuidado com Dense > 1000)
    densidade = 0.05 # 5% de elementos não nulos
    
    resultados = []

    print(f"--- Iniciando Experimentos (Densidade: {densidade*100}%) ---")

    for N in tamanhos:
        print(f"Testando matriz {N}x{N}...")
        
        # Gerar dados brutos
        dados_A = gerar_dados_aleatorios(N, N, densidade)
        dados_B = gerar_dados_aleatorios(N, N, densidade)

        # --- PREPARAÇÃO ---
        
        # Esparsa
        esparsa_A = Estrutura2(N, N)
        esparsa_B = Estrutura2(N, N)
        popular_matriz_esparsa(esparsa_A, dados_A)
        popular_matriz_esparsa(esparsa_B, dados_B)
        
        # Tradicional
        densa_A = MatrizTradicional(N, N)
        densa_B = MatrizTradicional(N, N)
        popular_matriz_densa(densa_A, dados_A)
        popular_matriz_densa(densa_B, dados_B)

        # --- MEDIÇÃO DE TEMPO (Multiplicação) ---
        
        # Tempo Esparsa
        inicio = time.time()
        esparsa_A.multiplicar(esparsa_B) # Ou multiplicar_otimizado se tiver
        tempo_esparsa = time.time() - inicio

        # Tempo Tradicional
        inicio = time.time()
        densa_A.multiplicar_matriz(densa_B) # Método ingênuo O(N^3)
        tempo_densa = time.time() - inicio

        # --- MEDIÇÃO DE MEMÓRIA (Estimativa) ---
        # Nota: sys.getsizeof é aproximado. Para Esparsa, melhor usar k * tamanho_fixo
        # Aqui usamos uma simplificação para fins didáticos
        mem_esparsa = esparsa_A.get_k() * 64 # Estimativa grosseira de bytes por nó
        mem_densa = sys.getsizeof(densa_A.data) + (N * sys.getsizeof(densa_A.data[0])) 

        resultados.append({
            "Tamanho (N)": N,
            "Tempo Esparsa (s)": tempo_esparsa,
            "Tempo Tradicional (s)": tempo_densa,
            "Memória Esparsa (bytes)": mem_esparsa,
            "Memória Tradicional (bytes)": mem_densa
        })

    return pd.DataFrame(resultados)

# --- Gerar Gráficos ---

def plotar_resultados(df):
    # Gráfico 1: Tempo de Execução
    plt.figure(figsize=(10, 5))
    plt.plot(df["Tamanho (N)"], df["Tempo Esparsa (s)"], marker='o', label='Esparsa (Hash Map/AVL)')
    plt.plot(df["Tamanho (N)"], df["Tempo Tradicional (s)"], marker='x', label='Tradicional (Lista de Listas)')
    plt.xlabel('Tamanho da Matriz (NxN)')
    plt.ylabel('Tempo (segundos)')
    plt.title('Desempenho: Multiplicação de Matrizes')
    plt.legend()
    plt.grid(True)
    plt.savefig('grafico_tempo.png') # Salva no seu computador
    print("Gráfico de tempo salvo como 'grafico_tempo.png'")
    plt.show()

    # Gráfico 2: Uso de Memória
    plt.figure(figsize=(10, 5))
    plt.plot(df["Tamanho (N)"], df["Memória Esparsa (bytes)"], marker='o', label='Esparsa')
    plt.plot(df["Tamanho (N)"], df["Memória Tradicional (bytes)"], marker='x', label='Tradicional')
    plt.xlabel('Tamanho da Matriz (NxN)')
    plt.ylabel('Memória Estimada (Bytes)')
    plt.title('Uso de Memória')
    plt.legend()
    plt.yscale('log') # Escala logarítmica ajuda a ver a diferença brutal
    plt.grid(True)
    plt.savefig('grafico_memoria.png')
    print("Gráfico de memória salvo como 'grafico_memoria.png'")
    plt.show()

if __name__ == "__main__":
    # 1. Rodar e obter Tabela
    df_resultados = rodar_experimento()
    
    # 2. Exibir Tabela no Terminal
    print("\n--- TABELA DE RESULTADOS ---")
    print(df_resultados.to_string(index=False))
    
    # 3. Gerar Gráficos
    plotar_resultados(df_resultados)