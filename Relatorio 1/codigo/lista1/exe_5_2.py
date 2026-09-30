import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from codigo.metodos import matrizes
from codigo import ferramentas

def carregar_malha_lkt():
    # Matriz de coeficientes do circuito do Capítulo 5 (Exercício 5.2)
    M = [
        [ 20.0, -10.0,  -4.0],
        [-10.0,  25.0,  -5.0],
        [ -4.0,  -5.0,  20.0]
    ]
    V = [26.0, 0.0, 7.0]
    return M, V

def executar_convergencia_circuito():
    nome_script = os.path.splitext(os.path.basename(__file__))[0]
    config, pasta_saida = ferramentas.preparar_diretorios(nome_script, ["tolerancia:1e-2\n", "max_iteracoes:100\n"])
    if not config: return

    A, b = carregar_malha_lkt()
    tol, max_it = config.get('tolerancia', 1e-2), int(config.get('max_iteracoes', 100))
    resultados = []

    print(f"\n=== EXECUÇÃO: {nome_script.upper()} (Circuito Iterativo) ===")

    # Justificativa teórica de convergência para os iterativos
    estrita, fraca = matrizes.dominancia_diagonal(A)
    print(f" -> Convergência garantida (Critério das Linhas)? {'Sim' if estrita else 'Não (Critério falhou)'}")

    # Cálculo do número de condição
    try:
        cond_A = matrizes.numero_condicao(A)
        A_escalonada = matrizes.escalar_linhas(A)
        cond_A_escala = matrizes.numero_condicao(A_escalonada)
        print(f" -> Número de Condição cond(A) [Sem Escala]: {cond_A:.6f}")
        print(f" -> Número de Condição cond(A) [Com Escala]: {cond_A_escala:.6f}")
    except Exception as e:
        print(f"-> Erro ao calcular o condicionamento: {e}")
        cond_A = None
        cond_A_escala = None

    # Analisamos a convergência cruzando o método exato de Gauss com os iterativos Jacobi e Seidel
    rotinas = {
        "Gauss-Exato": lambda: matrizes.resolver_gauss(A, b),
        "Iterativo-Jacobi": lambda: matrizes.resolver_jacobi(A, b, tol, max_it),
        "Iterativo-Seidel": lambda: matrizes.resolver_seidel(A, b, tol, max_it)
    }

    for nome, rotina in rotinas.items():
        correntes, fator, log = rotina()
        resultados.append({
            "Metodo": nome, "Esforco": fator,
            "i1": correntes[0], "i2": correntes[1], "i3": correntes[2], 
            "Cond_A_Bruta": cond_A, "Cond_A_Escalonada": cond_A_escala
        })
        ferramentas.exportar_dados_csv(os.path.join(pasta_saida, f"{nome_script}_{nome.lower()}.csv"), log)

    ferramentas.exportar_dados_csv(os.path.join(pasta_saida, f"{nome_script}_resumo.csv"), resultados)

    for r in resultados:
        print(f"[{r['Metodo']:<18}] (Passos/Iter: {r['Esforco']:<2}) | I = [{r['i1']:.3f}, {r['i2']:.3f}, {r['i3']:.3f}]")

if __name__ == '__main__':
    executar_convergencia_circuito()