import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from codigo.metodos import matrizes
from codigo import ferramentas

def carregar_escada():
    # Defino o sistema de equações obtido pelo método dos laços no circuito em escada
    matriz_escada = [
        [14.0,  4.0,  4.0],
        [ 4.0,  7.0, 19.0],
        [ 4.0,  7.0, 18.0]
    ]
    vetor_fontes = [100.0, 100.0, 100.0]
    return matriz_escada, vetor_fontes

def multiplicar_matriz_vetor(M, v):
    """Multiplicação básica estruturada para resolver x = A^(-1)*b."""
    return [sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M))]

def executar_analise_escada():
    nome_script = os.path.splitext(os.path.basename(__file__))[0]
    config, pasta_saida = ferramentas.preparar_diretorios(nome_script, ["tolerancia:1e-12\n"])
    if not config: return

    A, b = carregar_escada()
    resultados = []

    print(f"\n=== EXECUÇÃO: {nome_script.upper()} (Circuito Escada) ===")
    
    # Calculo o número de condição exigido para avaliar o sistema linear
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

    # 1. Atendo à alínea específica que pede o cálculo direto usando a Matriz Inversa (x = A^(-1) * b)
    inversa_A = matrizes.obter_matriz_inversa(A)
    vetor_x_inversa = multiplicar_matriz_vetor(inversa_A, b)
    vetor_x_inversa = [x + 0.0 for x in vetor_x_inversa] # Remove -0.0
    
    print(f"-> Resolução por A^(-1) * b: Ix (Corrente 3) = {vetor_x_inversa[2]:.4f} A\n")

    # 2. Resolução através dos métodos diretos tradicionais (Gauss e LU)
    rotinas = {
        "Gauss": lambda: matrizes.resolver_gauss(A, b),
        "LU": lambda: matrizes.resolver_lu(A, b)
    }

    for nome, rotina in rotinas.items():
        vetor_i, passos, log = rotina()
        vetor_i = [x + 0.0 for x in vetor_i] # Remove -0.0
        resultados.append({
            "Metodo": nome, "I1": vetor_i[0], "I2": vetor_i[1], "Ix": vetor_i[2], 
            "Cond_A_Bruta": cond_A, "Cond_A_Escalonada": cond_A_escala
        })
        ferramentas.exportar_dados_csv(os.path.join(pasta_saida, f"{nome_script}_{nome.lower()}.csv"), log)

    ferramentas.exportar_dados_csv(os.path.join(pasta_saida, f"{nome_script}_resumo.csv"), resultados)

    for r in resultados:
        print(f"[{r['Metodo']}] -> [I1, I2, Ix] = [{r['I1']:.4f}A, {r['I2']:.4f}A, {r['Ix']:.4f}A]")

if __name__ == '__main__':
    executar_analise_escada()