import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from codigo.metodos import matrizes
from codigo import ferramentas

def carregar_modelo_eletrico():
    """Retorna a matriz de resistências e o vetor de tensões do circuito."""
    # Monto o sistema 3x3 com base nas Leis de Kirchhoff aplicadas as malhas do circuito
    matriz_resistencias = [
        [ 8.0, -4.0, -2.0],
        [-4.0,  6.0, -2.0],
        [-2.0, -2.0, 10.0]
    ]
    vetor_tensoes = [10.0, 0.0, 4.0]
    return matriz_resistencias, vetor_tensoes

def executar_analise_malhas():
    nome_script = os.path.splitext(os.path.basename(__file__))[0]
    config, pasta_saida = ferramentas.preparar_diretorios(nome_script, ["tolerancia:1e-12\n"])
    if not config: return

    A, b = carregar_modelo_eletrico()
    tol = config.get('tolerancia', 1e-12)
    resultados = []

    print(f"\n=== EXECUÇÃO: {nome_script.upper()} (Circuito LKT 3x3) ===")
    
    # Calculo o número de condição da matriz
    # para medir a sensibilidade e estabilidade numérica deste circuito
    try:
        cond_A = matrizes.numero_condicao(A)
        print(f" -> Número de Condição cond(A) [Norma Infinito]: {cond_A:.6f}")
    except Exception as e:
        print(f"-> Erro ao calcular o condicionamento: {e}")
        cond_A = None

    # Agrupo os métodos diretos que vamos comparar para resolver as correntes
    rotinas_diretas = {
        "Eliminação de Gauss": lambda: matrizes.resolver_gauss(A, b, tol_pivo=tol),
        "Fatoração LU": lambda: matrizes.resolver_lu(A, b, tol_pivo=tol)
    }

    for nome, rotina in rotinas_diretas.items():
        try:
            vetor_corrente, passos, log = rotina()
            resultados.append({
                "Metodo": nome, "Corrente_1": vetor_corrente[0], 
                "Corrente_2": vetor_corrente[1], "Corrente_3": vetor_corrente[2], 
                "Passos": passos, "Cond_A": cond_A
            })
            # Salvo o passo a passo detalhado em CSV para constar no relatório
            ferramentas.exportar_dados_csv(os.path.join(pasta_saida, f"{nome_script}_{nome.replace(' ', '').lower()}.csv"), log)
        except Exception as e:
            print(f"-> Falha no método {nome}: {e}")

    ferramentas.exportar_dados_csv(os.path.join(pasta_saida, f"{nome_script}_resumo.csv"), resultados)

    print("\n[Vetor de Correntes Resultante]")
    for r in resultados:
        print(f"{r['Metodo']:<25} | I = [{r['Corrente_1']:.4f}A, {r['Corrente_2']:.4f}A, {r['Corrente_3']:.4f}A] | Etapas: {r['Passos']}")

if __name__ == '__main__':
    executar_analise_malhas()