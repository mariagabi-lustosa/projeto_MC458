import sys

class MatrizTradicional:
    
    #representação tradicional de matriz (arranjo bidimensional)
    
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        # aloca memória para tdos os elementos (n x m), incluindo os que sao zero  O(n * m)
        self.data = [[0.0 for _ in range(cols)] for _ in range(rows)]

    def set(self, i, j, val):
        self.data[i][j] = val

    def get(self, i, j):
        return self.data[i][j]

    # O(n * m)
    def somar(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Dimensões incompatíveis")
            
        res = MatrizTradicional(self.rows, self.cols)
        
        for i in range(self.rows):
            for j in range(self.cols):
                # soma mesmo que seja 0 + 0
                res.data[i][j] = self.data[i][j] + other.data[i][j]
        return res

   
    # percorre a matriz inteira e traz O(n*m)
   
    def multiplicar_escalar(self, scalar):
        res = MatrizTradicional(self.rows, self.cols)
        
        for i in range(self.rows):
            for j in range(self.cols):
                # multiplica mesmo que seja 0 * k
                res.data[i][j] = self.data[i][j] * scalar
        return res

   
    
    # complexidade: O(linhaA * colunaB * colunaA), que eh O(n^3) para matrizes quadradas
    def multiplicar_matriz(self, other):
        if self.cols != other.rows:
            raise ValueError("Dimensões incompatíveis para multiplicação")
        
        # resultado tem linhas de A e colunas de B
        res = MatrizTradicional(self.rows, other.cols)
        
        # loop linhas de A
        for i in range(self.rows):
            # loop colunas de B
            for j in range(other.cols):
                soma = 0.0
                # loop colunas de A (q eh a msm qntde de linhas de B)
                for k in range(self.cols):
                    # aqui não verifica se os valores são zero
                    soma += self.data[i][k] * other.data[k][j]
                res.data[i][j] = soma
        return res
    """
    def get_memory_usage(self):
        #estima o uso de memória em bytes
        # Tamanho da lista externa + tamanho das listas internas + tamanho dos floats
        # Esta é uma estimativa, pois objetos Python têm overhead.
        # Para o relatório, considere a complexidade O(N*M).
        total = sys.getsizeof(self.data)
        for row in self.data:
            total += sys.getsizeof(row)
            for val in row:
                 total += sys.getsizeof(val)
        return totals

        """



    # O(1)
    def inserir(self, i, j, valor):
        if 0 <= i < self.rows and 0 <= j < self.cols:
            self.data[i][j] = float(valor)
        else:
            print(f"Erro: Índice ({i}, {j}) fora dos limites.")

    # O(1)
   
    def acessar(self, i, j):
        if 0 <= i < self.rows and 0 <= j < self.cols:
            return self.data[i][j]
        else:
            print(f"Erro: Índice ({i}, {j}) fora dos limites.")
            return None

    #O(n*m))
    
    # criamos fisicamente uma nova matriz e copiamos item por item
    def transpor(self):
        # nova matriz com dimensões invertidas
        m_transposta = MatrizTradicional(self.cols, self.rows)
        
        # copiando dados
        for i in range(self.rows):
            for j in range(self.cols):
                # inversao, o que era [i][j] vira [j][i]
                m_transposta.data[j][i] = self.data[i][j]
        
        # atualiza a classe com os novos dadso
        self.rows = m_transposta.rows
        self.cols = m_transposta.cols
        self.data = m_transposta.data

   