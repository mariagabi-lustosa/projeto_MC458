class No:
    def __init__(self, linha, coluna, valor):
        self.linha = linha
        self.coluna = coluna
        self.valor = valor
        self.esquerda = None
        self.direita = None
        self.altura = 1
        

    def tupla_chave(self):
        return (self.linha, self.coluna)

class Arvore:
    def __init__(self):
        self.raiz = None
        self.k_elementos = 0

    def inserir(self, linha, coluna, valor):
        self.raiz = self._inserir_recursivo(self.raiz, linha, coluna, valor)

    def buscar(self, linha, coluna):
        no = self.raiz
        while no is not None:
            if (linha, coluna) == no.tupla_chave():
                return no.valor
            elif (linha, coluna) < no.tupla_chave():
                no = no.esquerda
            else:
                no = no.direita
        return 0
    
    def deep_copy_tree(self, no_original):
        """ Realiza uma cópia profunda recursiva da árvore (O(k)). """
        if no_original is None:
            return None
        
        # Cria um novo nó com os dados copiados
        novo_no = No(no_original.linha, no_original.coluna, no_original.valor)
        novo_no.altura = no_original.altura
        novo_no.esta_ativo = no_original.esta_ativo
        
        # Constrói recursivamente as sub-árvores
        novo_no.esquerda = self.deep_copy_tree(no_original.esquerda)
        novo_no.direita = self.deep_copy_tree(no_original.direita)
        
        return novo_no

    def _construir_balanceada_recursivo(self, elementos_ordenados):
        # Constrói AVL a partir de lista ordenada em O(k). 
        if not elementos_ordenados:
            return None
        
        meio = len(elementos_ordenados) // 2
        no = elementos_ordenados[meio]
        
        no.esquerda = self._construir_balanceada_recursivo(elementos_ordenados[:meio])
        no.direita = self._construir_balanceada_recursivo(elementos_ordenados[meio + 1:])
        
        
        no.altura = 1 + max(self._get_altura(no.esquerda), self._get_altura(no.direita))
        return no

    
    def construir_a_partir_de_lista(self, lista_elementos):
        #Insere todos os elementos de forma otimizada. O(k) 
        

        self.raiz = self._construir_balanceada_recursivo(lista_elementos)
        self.k_elementos = len(lista_elementos)


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
        if (linha, coluna) < no.tupla_chave():
            no.esquerda = self._inserir_recursivo(no.esquerda, linha, coluna, valor)
        elif (linha, coluna) > no.tupla_chave():
            no.direita = self._inserir_recursivo(no.direita, linha, coluna, valor)
        else:
            no.valor = valor
            return no
        no.altura = 1 + max(self._get_altura(no.esquerda), self._get_altura(no.direita))
        balanceamento = self._get_balanceamento(no)
        if balanceamento > 1 and (linha, coluna) < no.esquerda.tupla_chave():
            return self._rotacao_direita(no)
        if balanceamento < -1 and (linha, coluna) > no.direita.tupla_chave():
            return self._rotacao_esquerda(no)
        if balanceamento > 1 and (linha, coluna) > no.esquerda.tupla_chave():
            no.esquerda = self._rotacao_esquerda(no.esquerda)
            return self._rotacao_direita(no)
        if balanceamento < -1 and (linha, coluna) < no.direita.tupla_chave():
            no.direita = self._rotacao_direita(no.direita)
            return self._rotacao_esquerda(no)
        return no

    def em_ordem(self):
        lista_nos = []
        self._em_ordem_recursivo(self.raiz, lista_nos)
        return lista_nos
    
    def _em_ordem_recursivo(self, no, lista_nos):
        if no:
            self._em_ordem_recursivo(no.esquerda, lista_nos)
            lista_nos.append(no)
            self._em_ordem_recursivo(no.direita, lista_nos)

class Estrutura2:
    def __init__(self, total_linhas, total_colunas):
        self.arvore = Arvore()
        self.m = total_linhas
        self.n = total_colunas
        self.is_transposta = False

    def get_k(self):
        return self.arvore.k_elementos
    
    def get_dimensoes(self):
        if not self.is_transposta:
            return (self.m, self.n)
        else:
            return (self.n, self.m)

    def inserir(self, i, j, valor):
        if valor == 0: 
            return
        m_real, n_real = self.get_dimensoes()
        if i >= m_real or j >= n_real or i < 0 or j < 0:
            print(f"Erro: Índice ({i},{j}) fora da matriz {m_real}x{n_real}")
            return
        if not self.is_transposta:
            self.arvore.inserir(i, j, valor)
        else:
            self.arvore.inserir(j, i, valor)

    def acessar(self, i, j):
        if not self.is_transposta:
            return self.arvore.buscar(i, j)
        else:
            return self.arvore.buscar(j, i)

    def transpor(self):
        self.is_transposta = not self.is_transposta
        self.m, self.n = self.n, self.m

    def _percorrer_elementos(self):
        lista_elementos = []
        lista_nos = self.arvore.em_ordem()
        
        for no in lista_nos:
            if not self.is_transposta:
                lista_elementos.append((no.linha, no.coluna, no.valor))
            else:
                lista_elementos.append((no.coluna, no.linha, no.valor))
        return lista_elementos

    def somar(self, outra_matriz):
        m_A, n_A = self.get_dimensoes()
        m_B, n_B = outra_matriz.get_dimensoes()

        if (m_A, n_A) != (m_B, n_B):
            print("Os tamanhos são diferentes")
            return None

        matriz_C = Estrutura2(m_A, n_A)
        
        for i, j, valor in self._percorrer_elementos():
            matriz_C.inserir(i, j, valor)

        for i, j, valor_B in outra_matriz._percorrer_elementos():
            valor_C_atual = matriz_C.acessar(i, j)
            matriz_C.inserir(i, j, valor_C_atual + valor_B)
        
        return matriz_C
    
   
    def _aplicar_escalar_recursivo(self, no, escalar):
        
        if no:
            
            no.valor *= escalar
            
            
            self._aplicar_escalar_recursivo(no.esquerda, escalar)
            self._aplicar_escalar_recursivo(no.direita, escalar)

    # obter elementos ativos 
    def _obter_nos_ativos_ordenados(self):
        lista_ativos = []
        
        for no in self.arvore.em_ordem(): 
            if abs(no.valor) > 1e-9:
                lista_ativos.append(no)
        return lista_ativos
    
    def deep_copy(self):
        # percorre todos os nós da arvore e criar novos nós (e a nova estrutura da árvore) em tempo linear.
        m_real, n_real = self.get_dimensoes()
        nova_matriz = Estrutura2(m_real, n_real)
        
        # Copia as dimensões originais (m e n sem transposta) e o estado da transposta
        nova_matriz.m = self.m
        nova_matriz.n = self.n
        nova_matriz.is_transposta = self.is_transposta 

        # copia a arvore
        nova_matriz.arvore.raiz = nova_matriz.arvore.deep_copy_tree(self.arvore.raiz)
        nova_matriz.arvore.k_elementos = self.arvore.k_elementos
        
        return nova_matriz

    def multiplicar_por_escalar(self, escalar):
      
        if abs(escalar) < 1e-9:
            # Se multiplicar por zero, retorna matriz vazia 
            return Estrutura2(self.m, self.n)

        # cria um clone da arvore
        m, n = self.get_dimensoes()
        matriz_C = self.deep_copy() 
        
        
        matriz_C._aplicar_escalar_recursivo(matriz_C.arvore.raiz, escalar)
        nos_ativos = matriz_C._obter_nos_ativos_ordenados()
        matriz_C.arvore.construir_a_partir_de_lista(nos_ativos)
        
        return matriz_C

    def multiplicar(self, outra_matriz):
        m_A, n_A = self.get_dimensoes()
        m_B, n_B = outra_matriz.get_dimensoes()

        if n_A != m_B:
            print("Dimensões diferente")
            return None

        matriz_C = Estrutura2(m_A, n_B)
        
        lista_A = self._percorrer_elementos()
        lista_B = outra_matriz._percorrer_elementos()

        for i, k, valor_A in lista_A:
            for k_prime, j, valor_B in lista_B:
                if k == k_prime:
                    valor_C_atual = matriz_C.acessar(i, j)
                    matriz_C.inserir(i, j, valor_C_atual + (valor_A * valor_B))

        return matriz_C
    
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


def matriz_para_arvore(matriz):
    linhas = len(matriz)
    if linhas == 0: 
        print('Matriz vazia')
        return Estrutura2(0, 0)
    
    colunas = len(matriz[0])
    matriz_esparsa = Estrutura2(linhas, colunas)

    for i in range(linhas):
        for j in range(colunas):
            if matriz[i][j] != 0:
                matriz_esparsa.inserir(i, j, matriz[i][j])
    return matriz_esparsa

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