import math
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from codigo.metodos import raizes
from codigo import ferramentas

def executar_analise_financiamento():
    nome_script = os.path.splitext(os.path.basename(__file__))[0]
    
    padroes = [
        "tolerancia:1e-6\n", 
        "max_iteracoes:150\n",
        "limite_inferior:1.05\n",
        "limite_superior:1.30\n",
        "chute_inicial:1.12\n"
    ]
    
    config, pasta_saida = ferramentas.preparar_diretorios(nome_script, padroes)
    if not config:
        print("-> Configure o TXT e rode novamente!")
        return

    # Dados financeiros fornecidos no enunciado (Preço à vista e entradas)
    valor_financiado = 162.0 - 22.0  # VF = 140.0
    
    # Plano A: 9 prestações de R$ 26,50
    k_plano_A = valor_financiado / 26.50
    parcelas_A = 9
    
    # Plano B: 12 prestações de R$ 21,50
    k_plano_B = valor_financiado / 21.50
    parcelas_B = 12

    # Polinômios gerados (onde x = 1 + J) e suas respectivas derivadas analíticas exatas
    planos = {
        'Plano_A': {
            'f': lambda x: k_plano_A * (x ** (parcelas_A + 1)) - (k_plano_A + 1) * (x ** parcelas_A) + 1,
            'f_linha': lambda x: k_plano_A * (parcelas_A + 1) * (x ** parcelas_A) - (k_plano_A + 1) * parcelas_A * (x ** (parcelas_A - 1))
        },
        'Plano_B': {
            'f': lambda x: k_plano_B * (x ** (parcelas_B + 1)) - (k_plano_B + 1) * (x ** parcelas_B) + 1,
            'f_linha': lambda x: k_plano_B * (parcelas_B + 1) * (x ** parcelas_B) - (k_plano_B + 1) * parcelas_B * (x ** (parcelas_B - 1))
        }
    }

    tol = config.get('tolerancia', 1e-6)
    max_it = int(config.get('max_iteracoes', 150))
    lim_inf = config.get('limite_inferior', 1.05)
    lim_sup = config.get('limite_superior', 1.30)
    chute_ini = config.get('chute_inicial', 1.12)

    resultados_gerais = []
    print(f"\n=== EXECUÇÃO: {nome_script.upper()} (Taxas de Juros) ===")

    for nome_plano, equacoes in planos.items():
        print(f"\n>> Processando {nome_plano}...")
        
        funcao_plano = equacoes['f']
        derivada_plano = equacoes['f_linha']
        
        metodos = {
            "Bissecção": lambda: raizes.metodo_bisseccao(funcao_plano, lim_inf, lim_sup, tol, max_it),
            "Falsa Posição": lambda: raizes.metodo_falsa_posicao(funcao_plano, lim_inf, lim_sup, tol, max_it),
            "Newton-Raphson": lambda: raizes.metodo_newton_raphson(funcao_plano, derivada_plano, chute_ini, tol, max_it),
            "Secante": lambda: raizes.metodo_secante(funcao_plano, lim_inf, lim_sup, tol, max_it)
        }

        for nome_metodo, rotina in metodos.items():
            raiz_calc, iteracoes, log_exec = rotina()
            erro_final = log_exec[-1]['erro_relativo'] if log_exec else 0.0
            
            # Como x = 1 + J, isolamos os juros J subtraindo 1 da raiz encontrada, convertendo para percentual
            taxa_juros = (raiz_calc - 1.0) * 100 if raiz_calc else 0.0
            
            nome_arquivo = f"{nome_script}_{nome_plano}_{nome_metodo.replace(' ', '').replace('ç', 'c').replace('ã', 'a').lower()}.csv"
            ferramentas.exportar_dados_csv(os.path.join(pasta_saida, nome_arquivo), log_exec)
            
            resultados_gerais.append({
                "Plano": nome_plano,
                "Metodo": nome_metodo,
                "Raiz_X": raiz_calc,
                "Juros_Porcentagem": taxa_juros,
                "Iteracoes": iteracoes,
                "Erro_Terminal": erro_final
            })

    ferramentas.exportar_dados_csv(os.path.join(pasta_saida, f"{nome_script}_resumo.csv"), resultados_gerais)

    print("\n[Resumo dos Resultados]")
    for res in resultados_gerais:
        print(f"{res['Plano']:<10} | {res['Metodo']:<15} | J = {res['Juros_Porcentagem']:<6.2f}% | Iter: {res['Iteracoes']}")

if __name__ == '__main__':
    executar_analise_financiamento()