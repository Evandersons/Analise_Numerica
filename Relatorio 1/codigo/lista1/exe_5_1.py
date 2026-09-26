import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from codigo.metodos import matrizes
from codigo import ferramentas

def carregar_malha_laplace():
    # Sistema 6x6 proveniente da discretização da Equação de Laplace por diferenças finitas
    matriz_laplaciana = [
        [ 4.0, -1.0,  0.0, -1.0,  0.0,  0.0],
        [-1.0,  4.0, -1.0,  0.0, -1.0,  0.0],
        [ 0.0, -1.0,  4.0,  0.0,  0.0, -1.0],
        [-1.0,  0.0,  0.0,  4.0, -1.0,  0.0],
        [ 0.0, -1.0,  0.0, -1.0,  4.0, -1.0],
        [ 0.0,  0.0, -1.0,  0.0, -1.0,  4.0]
    ]
    vetor_contorno = [100.0, 0.0, 0.0, 100.0, 0.0, 0.0]
    return matriz_laplaciana, vetor_contorno

def executar_modelo_laplace():
    nome_script = os.path.splitext(os.path.basename(__file__))[0]
    config, pasta_saida = ferramentas.preparar_diretorios(nome_script, ["tolerancia:1e-4\n", "max_iteracoes:100\n"])
    if not config: return

    A, b = carregar_malha_laplace()
    tol, max_it = config.get('tolerancia', 1e-4), int(config.get('max_iteracoes', 100))
    resultados = []

    print(f"\n=== EXECUÇÃO: {nome_script.upper()} (EDP Laplace 6x6) ===")

    # Cálculo obrigatório do número de condição
    try:
        cond_A = matrizes.numero_condicao(A)
        print(f" -> Número de Condição cond(A) [Norma Infinito]: {cond_A:.6f}")
    except Exception as e:
        print(f"-> Erro ao calcular o condicionamento: {e}")
        cond_A = None

    # Comparamos um método direto de precisão (Gauss-Jordan) com os métodos iterativos do Capítulo 5
    rotinas = {
        "Gauss-Jordan": lambda: matrizes.resolver_jordan(A, b),
        "Jacobi": lambda: matrizes.resolver_jacobi(A, b, tol, max_it),
        "Gauss-Seidel": lambda: matrizes.resolver_seidel(A, b, tol, max_it)
    }

    for nome, rotina in rotinas.items():
        solucao, fator_temporal, log = rotina()
        res = {"Metodo": nome, "Iteracoes_Ou_Passos": fator_temporal, "Cond_A": cond_A}
        for idx, val in enumerate(solucao):
            res[f"X_{idx+1}"] = val
        resultados.append(res)
        
        ferramentas.exportar_dados_csv(os.path.join(pasta_saida, f"{nome_script}_{nome.lower()}.csv"), log)

    ferramentas.exportar_dados_csv(os.path.join(pasta_saida, f"{nome_script}_resumo.csv"), resultados)

    for r in resultados:
        print(f"[{r['Metodo']:<15}] Esforço: {r['Iteracoes_Ou_Passos']:<3} | X_1 = {r['X_1']:.4f}")

if __name__ == '__main__':
    executar_modelo_laplace()