'''
O nó da estrutura do heap que tem:
- os filhos (esquerda e direita)
- a altura que ele está
- sua linha correspondente na matriz
- sua coluna correspondente na matriz
- seu valor

tem uma função chamada posição que retorna uma tupla com a linha e a coluna do nó
'''
class No:
    def __init__(self, linha, coluna, valor):
        self.linha = linha
        self.coluna = coluna
        self.valor = valor
        self.esquerda = None
        self.direita = None
        self.altura = 1

    def posicao(self):
        return (self.linha, self.coluna)


'''
Classe da árvore que é responsável por:
- Criar a árvore e guardar os dados
- inserir elementos balanceando a arvore
- buscar um elemento
- retornar os elementos da arvore em ordem
'''
class Arvore:
    # Montagem inicial da árvore indicando o nó da raiz e o total de elementos (k_elementos)
    def __init__(self):
        self.raiz = None
        self.k_elementos = 0

    # Chama a função inserir recursivo para adicionar um novo elemento fazendo o devido balanceamento
    def inserir(self, linha, coluna, valor):
        self.raiz = self._inserir_recursivo(self.raiz, linha, coluna, valor)

    # Faz uma busca binária nos elementos da árvore para ver o valor do elemento
    def buscar(self, linha, coluna):
        no = self.raiz
        while no is not None:
            if (linha, coluna) == no.posicao():
                return no.valor
            elif (linha, coluna) < no.posicao():
                no = no.esquerda
            else:
                no = no.direita
        return 0

    # Retorna a altura do nó atual
    def _get_altura(self, no):
        if not no: 
            return 0
        else:
            return no.altura
        
    
    def _get_balanceamento(self, no):
        if not no: 
            return 0
        else:
            return self._get_altura(no.esquerda) - self._get_altura(no.direita)

    def _rotacao_direita(self, atual):
        y = atual.esquerda
        direita = y.direita
        y.direita = atual
        atual.esquerda = direita
        atual.altura = 1 + max(self._get_altura(atual.esquerda), self._get_altura(atual.direita))
        y.altura = 1 + max(self._get_altura(y.esquerda), self._get_altura(y.direita))
        return y

    def _rotacao_esquerda(self, atual):
        y = atual.direita
        esquerda = y.esquerda
        y.esquerda = atual
        atual.direita = esquerda
        atual.altura = 1 + max(self._get_altura(atual.esquerda), self._get_altura(atual.direita))
        y.altura = 1 + max(self._get_altura(y.esquerda), self._get_altura(y.direita))
        return y

    def _inserir_recursivo(self, no, linha, coluna, valor):
        if not no:
            self.k_elementos += 1
            return No(linha, coluna, valor)
        if (linha, coluna) < no.posicao():
            no.esquerda = self._inserir_recursivo(no.esquerda, linha, coluna, valor)
        elif (linha, coluna) > no.posicao():
            no.direita = self._inserir_recursivo(no.direita, linha, coluna, valor)
        else:
            no.valor = valor
            return no
        no.altura = 1 + max(self._get_altura(no.esquerda), self._get_altura(no.direita))
        balanceamento = self._get_balanceamento(no)
        if balanceamento > 1 and (linha, coluna) < no.esquerda.posicao():
            return self._rotacao_direita(no)
        if balanceamento < -1 and (linha, coluna) > no.direita.posicao():
            return self._rotacao_esquerda(no)
        if balanceamento > 1 and (linha, coluna) > no.esquerda.posicao():
            no.esquerda = self._rotacao_esquerda(no.esquerda)
            return self._rotacao_direita(no)
        if balanceamento < -1 and (linha, coluna) < no.direita.posicao():
            no.direita = self._rotacao_direita(no.direita)
            return self._rotacao_esquerda(no)
        return no

    # Retorna uma lista ordenada com todos os nós da lista
    def em_ordem(self):
        lista_nos = []
        self._em_ordem_recursivo(self.raiz, lista_nos)
        return lista_nos
    
    def _em_ordem_recursivo(self, no, lista_nos):
        if no:
            self._em_ordem_recursivo(no.esquerda, lista_nos)
            lista_nos.append(no)
            self._em_ordem_recursivo(no.direita, lista_nos)


'''
Essa classe cria uma estrutura com a arvore, altura da matriz, largura da matria e uma flag para indicar se a matriz está transposta.
também faz as operações necessárias:
- retornar o total de elementos
- inserir elemento
- acessar elemento
- transpor a matriz
- somar duas matrizes
- multiplicar a matriz por escalar
- multiplicar duas matrizes
- imprimir um resumo da matriz 
'''
class Estrutura2:
    def __init__(self, total_linhas, total_colunas):
        self.arvore = Arvore()
        self.m = total_linhas
        self.n = total_colunas
        self.is_transposta = False

    # Retorna o total de elementos da estrutura
    def get_k(self):
        return self.arvore.k_elementos
    
    # Retorna as dimensões da matriz, trocando a ordem se estiver transposta
    def get_dimensoes(self):
        if not self.is_transposta:
            return (self.m, self.n)
        else:
            return (self.n, self.m)

    # Adiciona um novo valor na matriz 
    def inserir(self, i, j, valor):
        if valor == 0: 
            return
        
        m, n = self.get_dimensoes()

        if i >= m or j >= n or i < 0 or j < 0:
            print(f"Erro: Índice ({i},{j}) fora da matriz {m}x{n}")
            return
        
        if not self.is_transposta:
            self.arvore.inserir(i, j, valor)
        else:
            self.arvore.inserir(j, i, valor)

    # Procura um valor na matriz, cuidando se ela é transposta ou não
    def acessar(self, i, j):
        if not self.is_transposta:
            return self.arvore.buscar(i, j)
        else:
            return self.arvore.buscar(j, i)

    # Transpõe trocando a flag
    def transpor(self):
        self.is_transposta = not self.is_transposta

    # Retorna todos os elementos
    def _percorrer_elementos(self):
        lista_elementos = []
        lista_nos = self.arvore.em_ordem()
        
        for no in lista_nos:
            if not self.is_transposta:
                lista_elementos.append((no.linha, no.coluna, no.valor))
            else:
                lista_elementos.append((no.coluna, no.linha, no.valor))
        return lista_elementos

    # Cria uma nova estrutura C que contem a soma das duas matrizes
    def somar(self, matriz_b):
        m_A, n_A = self.get_dimensoes()
        m_B, n_B = matriz_b.get_dimensoes()

        if (m_A, n_A) != (m_B, n_B):
            print("Os tamanhos são diferentes")
            return None

        matriz_C = Estrutura2(m_A, n_A)
        
        for i, j, valor in self._percorrer_elementos():
            matriz_C.inserir(i, j, valor)

        for i, j, valor_B in matriz_b._percorrer_elementos():
            valor_C_atual = matriz_C.acessar(i, j)
            matriz_C.inserir(i, j, valor_C_atual + valor_B)
        
        return matriz_C

    # Cria estutura c com a multiplicação da matriz por um escalar
    def multiplicar_por_escalar(self, escalar):
        if escalar == 0:
            return Estrutura2(self.m, self.n)

        m, n = self.get_dimensoes()
        matriz_C = Estrutura2(m, n)
        
        lista_elementos = self._percorrer_elementos()

        if escalar == 1:
            for i, j, valor in lista_elementos:
                matriz_C.inserir(i, j, valor)
        else:
            for i, j, valor in lista_elementos:
                matriz_C.inserir(i, j, valor * escalar)
        
        return matriz_C

    # faz a multiplicação das matrizes
    def multiplicar(self, matriz_b):
        m_A, n_A = self.get_dimensoes()
        m_B, n_B = matriz_b.get_dimensoes()

        if n_A != m_B:
            print("Dimensões diferente")
            return None

        matriz_C = Estrutura2(m_A, n_B)
        
        lista_A = self._percorrer_elementos()
        lista_B = matriz_b._percorrer_elementos()

        for i, k, valor_A in lista_A:
            for k_prime, j, valor_B in lista_B:
                if k == k_prime:
                    valor_C_atual = matriz_C.acessar(i, j)
                    matriz_C.inserir(i, j, valor_C_atual + (valor_A * valor_B))

        return matriz_C
    
    # imprime uma versão resumida da matriz    
    def imprimir(self, nome):
        m, n = self.get_dimensoes()
        k = self.get_k()
        print(f"Matriz {nome} {m}x{n} (k={k}):")

        if k > 20:
            print("(Mostrando os primeiros 20 elementos não-nulos)")
        
        lista_elementos = self._percorrer_elementos()
        
        if k == 0:
            print("  (Matriz Vazia)")
            return

        for i in range(min(k, 20)):
            linha, coluna, valor = lista_elementos[i]
            print(f"  ({linha}, {coluna}) = {valor:.2f}")

'''
Essa função recebe a matriz e cria uma estrutura com a árvore e em seguida adiciona todos os elementos não nulos
'''
def matriz_para_arvore(matriz):
    linhas = len(matriz)
    if linhas == 0: 
        print('Matriz vazia')
        return Estrutura2(0, 0)
    
    colunas = len(matriz[0])
    heap = Estrutura2(linhas, colunas)

    for i in range(linhas):
        for j in range(colunas):
            if matriz[i][j] != 0:
                heap.inserir(i, j, matriz[i][j])
    return heap

# Para teste das funções
def main():
    matriz_A = [
        [5, 0, 0],
        [0, 0, 1],
        [2, 0, 0]
    ]
    matriz_B = [
        [3, 1, 0],
        [3, 0, 0],
        [0, 0, 4]
    ]
    
    matriz_A = matriz_para_arvore(matriz_A)
    matriz_B = matriz_para_arvore(matriz_B)

    matriz_A.imprimir("A")
    matriz_B.imprimir("B")

    while True:

        print("\n--- OPERAÇÕES ---")
        print("1. Somar (C = A + B)")
        print("2. Multiplicar por Escalar (C = A * k)")
        print("3. Multiplicar Matrizes (C = A * B)")
        print("4. Transpor Matriz A (A = A^T)")
        print("5. Acessar elemento A[i, j]")
        print("6. Inserir elemento em A[i, j]")
        print("sair - Encerrar o programa")
        
        escolha = input("\nEscolha uma operação: ").strip().lower()

        if escolha == '1':
            resultado = matriz_A.somar(matriz_B)
            if resultado:
                resultado.imprimir("soma")
                
        elif escolha == '2':
            try:
                escalar_str = input("Digite o valor do escalar (k): ")
                escalar = float(escalar_str)
                resultado = matriz_A.multiplicar_por_escalar(escalar)
                resultado.imprimir(f"A multiplicada por {escalar}")
            except ValueError:
                print("valor invalido")

        elif escolha == '3':
            resultado = matriz_A.multiplicar(matriz_B)
            if resultado:
                resultado.imprimir("AxB")

        elif escolha == '4':
            matriz_A.transpor()
            matriz_A.imprimir("A transposta")

        elif escolha == '5':
            try:
                i = int(input("Digite a linha (i): "))
                j = int(input("Digite a coluna (j): "))
                valor = matriz_A.acessar(i, j)
                print(f"Valor A[{i},{j}] = {valor}")
            except ValueError:
                print("Indice invalido")

        elif escolha == '6':
            try:
                i = int(input("Digite a linha (i): "))
                j = int(input("Digite a coluna (j): "))
                valor = float(input("Digite o valor: "))
                matriz_A.inserir(i, j, valor)
                print(f"Valor A[{i},{j}] inserido.")
            except ValueError:
                print("Indice invalido")

        elif escolha == 'sair':
            break
        
        else:
            print("Opção inválida")


if __name__ == "__main__":
    main()