import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from codigo.metodos import matrizes
from codigo import ferramentas

def carregar_malha_probabilidade():
    """Matriz esparsa de adjacência do labirinto (9x9) baseada nas equações de Markov."""
    matriz_transicao = [
        [ 4.0, -1.0,  0.0, -1.0,  0.0,  0.0,  0.0,  0.0,  0.0], # P1
        [-1.0,  4.0, -1.0,  0.0, -1.0,  0.0,  0.0,  0.0,  0.0], # P2
        [ 0.0, -1.0,  4.0,  0.0,  0.0, -1.0,  0.0,  0.0,  0.0], # P3
        [-1.0,  0.0,  0.0,  4.0, -1.0,  0.0, -1.0,  0.0,  0.0], # P4
        [ 0.0, -1.0,  0.0, -1.0,  4.0, -1.0,  0.0, -1.0,  0.0], # P5
        [ 0.0,  0.0, -1.0,  0.0, -1.0,  4.0,  0.0,  0.0, -1.0], # P6
        [ 0.0,  0.0,  0.0, -1.0,  0.0,  0.0,  4.0, -1.0,  0.0], # P7
        [ 0.0,  0.0,  0.0,  0.0, -1.0,  0.0, -1.0,  4.0, -1.0], # P8
        [ 0.0,  0.0,  0.0,  0.0,  0.0, -1.0,  0.0, -1.0,  4.0]  # P9
    ]
    vetor_fronteira = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0]
    return matriz_transicao, vetor_fronteira

def executar_probabilidades_labirinto():
    nome_script = os.path.splitext(os.path.basename(__file__))[0]
    config, pasta_saida = ferramentas.preparar_diretorios(nome_script, ["tolerancia:1e-12\n"])
    if not config: return

    A, b = carregar_malha_probabilidade()
    resultados = []

    print(f"\n=== EXECUÇÃO: {nome_script.upper()} (Labirinto 9x9) ===")
    
    # 1. Cálculo obrigatório do número de condição
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

    # Resolvemos o sistema esparso por métodos diretos (Eliminação de Gauss e Fatoração LU)
    rotinas = {
        "Gauss": lambda: matrizes.resolver_gauss(A, b),
        "LU": lambda: matrizes.resolver_lu(A, b)
    }

    for nome, rotina in rotinas.items():
        vetor_prob, passos, log = rotina()
        res = {"Metodo": nome, "Passos": passos, "Cond_A_Bruta": cond_A, "Cond_A_Escalonada": cond_A_escala}
        for i, val in enumerate(vetor_prob):
            res[f"No_{i+1}"] = val
        resultados.append(res)
        ferramentas.exportar_dados_csv(os.path.join(pasta_saida, f"{nome_script}_{nome.lower()}.csv"), log)

    ferramentas.exportar_dados_csv(os.path.join(pasta_saida, f"{nome_script}_resumo.csv"), resultados)

    for r in resultados:
        p_str = ", ".join([f"{r[f'No_{i+1}']:.3f}" for i in range(9)])
        print(f"[{r['Metodo']}] -> P = [{p_str}]")

if __name__ == '__main__':
    executar_probabilidades_labirinto()