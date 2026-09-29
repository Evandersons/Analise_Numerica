import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from codigo.metodos import matrizes

A = [[0.0, 2.0], [3.0, 4.0]]   # pivô zero na primeira posição: exige troca de linhas
b = [4.0, 11.0]

x_lu, _, _ = matrizes.resolver_lu(A, b)
x_gauss, _, _ = matrizes.resolver_gauss(A, b)
print("LU:   ", x_lu)      # esperado: [1.0, 2.0]
print("Gauss:", x_gauss)   # esperado: [1.0, 2.0]