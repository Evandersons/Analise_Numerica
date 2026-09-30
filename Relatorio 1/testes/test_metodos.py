import os
import sys
import unittest
import warnings

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from codigo.metodos import raizes as R, matrizes as M

class TestRaizes(unittest.TestCase):
    def setUp(self):
        self.f = lambda x: x**2 - 4
        self.df = lambda x: 2 * x

    def test_quatro_metodos_convergem(self):
        for raiz in (
            R.metodo_bisseccao(self.f, 0, 5, 1e-9)[0],
            R.metodo_falsa_posicao(self.f, 0, 5, 1e-9)[0],
            R.metodo_newton_raphson(self.f, self.df, 1.0, 1e-9)[0],
            R.metodo_secante(self.f, 1.0, 3.0, 1e-9)[0],
        ):
            self.assertAlmostEqual(raiz, 2.0, places=6)

    def test_sem_troca_de_sinal(self):
        with self.assertRaises(ValueError):
            R.metodo_bisseccao(self.f, 3, 5)
        with self.assertRaises(ValueError):
            R.metodo_falsa_posicao(self.f, 3, 5)

    def test_raiz_no_extremo(self):
        self.assertEqual(R.metodo_bisseccao(self.f, 2, 5)[:2], (2, 0))

    def test_nao_convergencia_avisa(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            R.metodo_bisseccao(lambda x: x - 0.3, 0, 1, 1e-30, 5)
            self.assertEqual(len(w), 1)

    def test_iteracoes_comecam_em_1(self):
        _, _, rel = R.metodo_bisseccao(self.f, 0, 5)
        self.assertEqual(rel[0]['iteracao'], 1)


class TestSistemas(unittest.TestCase):
    A = [[0.0, 2.0], [3.0, 4.0]]
    b = [4.0, 11.0]

    def test_gauss_lu_jordan_com_pivo_zero(self):
        # Testa Gauss, LU e Jordan de verdade com uma matriz que exige troca de linhas
        x_gauss = M.resolver_gauss(self.A, self.b)[0]
        self.assertAlmostEqual(x_gauss[0], 1.0)
        self.assertAlmostEqual(x_gauss[1], 2.0)

        x_lu = M.resolver_lu(self.A, self.b)[0]
        self.assertAlmostEqual(x_lu[0], 1.0)
        self.assertAlmostEqual(x_lu[1], 2.0)

        x_jordan = M.resolver_jordan(self.A, self.b)[0]
        self.assertAlmostEqual(x_jordan[0], 1.0)
        self.assertAlmostEqual(x_jordan[1], 2.0)

    def test_inversa_e_condicao(self):
        A = [[2.0, 1.0], [1.0, 3.0]]
        inv = M.obter_matriz_inversa(A)
        self.assertAlmostEqual(inv[0][0], 3 / 5)
        self.assertAlmostEqual(inv[0][1], -1 / 5)

    def test_iterativos_batem_com_exato(self):
        A = [[20.0, -10.0, -4.0], [-10.0, 25.0, -5.0], [-4.0, -5.0, 20.0]]
        b = [26.0, 0.0, 7.0]
        for fn in (M.resolver_jacobi, M.resolver_seidel):
            x = fn(A, b, 1e-10, 500)[0]
            for xi, ex in zip(x, (2.0, 1.0, 1.0)):
                self.assertAlmostEqual(xi, ex, places=6)

if __name__ == '__main__':
    unittest.main()