'''
O nó da estrutura da arvore binaria de busca balanceada que tem:
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
            
            
    # Função pública para iniciar a atualização
    def atualizar_valores(self, escalar):
        self._atualizar_valores_recursivo(self.raiz, escalar)

    # Função recursiva que percorre todos os nós (O(K))
    def _atualizar_valores_recursivo(self, no, escalar):
        if no is not None:
            no.valor *= escalar
            self._atualizar_valores_recursivo(no.esquerda, escalar)
            self._atualizar_valores_recursivo(no.direita, escalar)


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
    def get_val(self, i, j):
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

    # Retorna uma matriz com a soma das duas matrizes
    def somar(self, matriz_b):
        m_A, n_A = self.get_dimensoes()
        m_B, n_B = matriz_b.get_dimensoes()

        if (m_A, n_A) != (m_B, n_B):
            print("Os tamanhos são diferentes")
            return None

        # Dicionário temporário para acumular valores: Chave=(i,j), Valor=soma
        soma_temp = {}

        for i, j, valor in self._percorrer_elementos():
            soma_temp[(i, j)] = valor

        for i, j, valor_b in matriz_b._percorrer_elementos():
            if (i, j) in soma_temp:
                soma_temp[(i, j)] += valor_b
            else:
                soma_temp[(i, j)] = valor_b

        matriz_C = Estrutura2(m_A, n_A)
        
        for (i, j), valor_final in soma_temp.items():
            if valor_final != 0:
                matriz_C.inserir(i, j, valor_final)

        return matriz_C

    # Cria estutura c com a multiplicação da matriz por um escalar
    def multiplicar_por_escalar(self, escalar):
        if escalar == 1:
            return

        if escalar == 0:
            self.arvore.raiz = None
            self.arvore.k_elementos = 0
            return

        self.arvore.atualizar_valores(escalar)

    # Retorna uma matriz com a multiplicação de duas matrizes
    def multiplicar(self, matriz_b):
        m_A, n_A = self.get_dimensoes()
        m_B, n_B = matriz_b.get_dimensoes()

        if n_A != m_B:
            print("Dimensões incompatíveis para multiplicação.")
            return None

        linhas_b = {}
        for k, j, valor_b in matriz_b._percorrer_elementos():
            if k not in linhas_b:
                linhas_b[k] = []
            linhas_b[k].append((j, valor_b))

        # Dicionário temporário para somar os produtos antes de criar a árvore
        resultados_temp = {}

        lista_A = self._percorrer_elementos()
        
        for i, k, valor_a in lista_A:
            if k in linhas_b:
                for j, valor_b in linhas_b[k]:
                    chave_c = (i, j)
                    produto = valor_a * valor_b
                    
                    if chave_c in resultados_temp:
                        resultados_temp[chave_c] += produto
                    else:
                        resultados_temp[chave_c] = produto

        matriz_C = Estrutura2(m_A, n_B)
        for (i, j), valor in resultados_temp.items():
            matriz_C.inserir(i, j, valor)

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

def triples_to_tree(triples, n):
    tree = Estrutura2(n, n)
    for t in triples:
        tree.inserir(t[0], t[1], t[2])
    return tree
    