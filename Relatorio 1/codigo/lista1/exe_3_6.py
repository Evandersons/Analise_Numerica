import math
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from codigo.metodos import raizes
from codigo import ferramentas

def executar_analise_missil():
    nome_script = os.path.splitext(os.path.basename(__file__))[0]
    
    padroes = [
        "tolerancia:1e-4\n", 
        "max_iteracoes:100\n",
        "inf_graus:30.0\n",
        "sup_graus:60.0\n",
        "x0_graus:55.0\n"
    ]
    
    config, pasta_saida = ferramentas.preparar_diretorios(nome_script, padroes)
    if not config:
        print("-> Configure o TXT e rode novamente!")
        return

    # Preparação das constantes físicas e trigonométricas do problema balístico
    theta_alvo_rad = math.radians(80) / 2.0  # Theta = 80°, logo metade é 40°
    constante_tangente = math.tan(theta_alvo_rad)
    
    # Função algébrica f(alpha) que modela a trajetória e o alvo do míssil
    equacao_missil = lambda a: math.sin(a)*math.cos(a) - constante_tangente*(0.8 - math.cos(a)**2)
    
    # Derivada analítica exata f'(alpha) deduzida por regra da cadeia e trigonométrica
    derivada_missil = lambda a: math.cos(2*a) - constante_tangente * math.sin(2*a)

    tol = config.get('tolerancia', 1e-4)
    max_it = int(config.get('max_iteracoes', 100))
    
    # Como o Python faz contas trigonométricas em radianos, converto os ângulos lidos em graus
    lim_inf = math.radians(config.get('inf_graus', 30.0))
    lim_sup = math.radians(config.get('sup_graus', 60.0))
    chute_ini = math.radians(config.get('x0_graus', 55.0))

    resultados_gerais = []
    print(f"\n=== EXECUÇÃO: {nome_script.upper()} (Lançamento de Míssil) ===")

    metodos = {
        "Bissecção": lambda: raizes.metodo_bisseccao(equacao_missil, lim_inf, lim_sup, tol, max_it),
        "Falsa Posição": lambda: raizes.metodo_falsa_posicao(equacao_missil, lim_inf, lim_sup, tol, max_it),
        "Newton-Raphson": lambda: raizes.metodo_newton_raphson(equacao_missil, derivada_missil, chute_ini, tol, max_it),
        "Secante": lambda: raizes.metodo_secante(equacao_missil, lim_inf, lim_sup, tol, max_it)
    }

    for nome_metodo, rotina in metodos.items():
        raiz_rad, iteracoes, log_exec = rotina()
        erro_final = log_exec[-1]['erro_relativo'] if log_exec else 0.0
        
        # Reconverto a raiz final de radianos para graus, para facilitar a leitura no relatório
        raiz_graus = math.degrees(raiz_rad)
        
        nome_arquivo = f"{nome_script}_{nome_metodo.replace(' ', '').replace('ç', 'c').replace('ã', 'a').lower()}.csv"
        ferramentas.exportar_dados_csv(os.path.join(pasta_saida, nome_arquivo), log_exec)
        
        resultados_gerais.append({
            "Metodo": nome_metodo,
            "Angulo_Rad": raiz_rad,
            "Angulo_Graus": raiz_graus,
            "Iteracoes": iteracoes,
            "Erro_Terminal": erro_final
        })

    ferramentas.exportar_dados_csv(os.path.join(pasta_saida, f"{nome_script}_resumo.csv"), resultados_gerais)

    print("\n[Resumo dos Resultados]")
    for res in resultados_gerais:
        print(f"{res['Metodo']:<15} | Alfa = {res['Angulo_Graus']:<8.4f} graus | Iter: {res['Iteracoes']}")

if __name__ == '__main__':
    executar_analise_missil()