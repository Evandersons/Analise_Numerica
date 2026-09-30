import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from codigo.metodos import matrizes
from codigo import ferramentas

def carregar_malha_termica():
    # Sistema 9x9 que modela a distribuição de temperaturas em uma membrana térmica quadrada
    matriz_temperaturas = [
        [-4.0,  1.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [ 1.0, -4.0,  1.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0],
        [ 0.0,  1.0, -4.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0],
        [ 1.0,  0.0,  0.0, -4.0,  1.0,  0.0,  1.0,  0.0,  0.0],
        [ 0.0,  1.0,  0.0,  1.0, -4.0,  1.0,  0.0,  1.0,  0.0],
        [ 0.0,  0.0,  1.0,  0.0,  1.0, -4.0,  0.0,  0.0,  1.0],
        [ 0.0,  0.0,  0.0,  1.0,  0.0,  0.0, -4.0,  1.0,  0.0],
        [ 0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  1.0, -4.0,  1.0],
        [ 0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  1.0, -4.0]
    ]
    vetor_calor = [-50.0, -50.0, -150.0, 0.0, 0.0, -100.0, -50.0, -50.0, -150.0]
    return matriz_temperaturas, vetor_calor

def executar_analise_termica():
    nome_script = os.path.splitext(os.path.basename(__file__))[0]
    config, pasta_saida = ferramentas.preparar_diretorios(nome_script, ["tolerancia:1e-5\n", "max_iteracoes:100\n"])
    if not config: return

    A, b = carregar_malha_termica()
    tol, max_it = config.get('tolerancia', 1e-5), int(config.get('max_iteracoes', 100))
    resultados = []

    print(f"\n=== EXECUÇÃO: {nome_script.upper()} (Malha Térmica 9x9) ===")

    # Cálculo obrigatório do número de condição
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

    # Comparamos um método direto robusto (Fatoração LU) com os iterativos (Jacobi e Seidel)
    rotinas = {
        "Gauss-LU": lambda: matrizes.resolver_lu(A, b),
        "Jacobi": lambda: matrizes.resolver_jacobi(A, b, tol, max_it),
        "Seidel": lambda: matrizes.resolver_seidel(A, b, tol, max_it)
    }

    for nome, rotina in rotinas.items():
        temps, fator, log = rotina()
        resultados.append({
            "Metodo": nome, "Esforco": fator,
            "Temp_Borda(u1)": temps[0], "Temp_Centro(u5)": temps[4], 
            "Cond_A_Bruta": cond_A, "Cond_A_Escalonada": cond_A_escala
        })
        ferramentas.exportar_dados_csv(os.path.join(pasta_saida, f"{nome_script}_{nome.lower()}.csv"), log)

    ferramentas.exportar_dados_csv(os.path.join(pasta_saida, f"{nome_script}_resumo.csv"), resultados)

    for r in resultados:
        print(f"[{r['Metodo']:<10}] Ciclos: {r['Esforco']:<3} | Borda(u1): {r['Temp_Borda(u1)']:>7.3f}°C | Centro(u5): {r['Temp_Centro(u5)']:>7.3f}°C")

if __name__ == '__main__':
    executar_analise_termica()