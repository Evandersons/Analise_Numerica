import math
import sys
import os

# Ajusto o caminho do Python para conseguir importar os módulos do nosso pacote
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from codigo.metodos import raizes
from codigo import ferramentas

def executar_analise_amplificador():
    # Pego o nome do próprio arquivo .exe para usar como identificador nas pastas e configs
    nome_script = os.path.splitext(os.path.basename(__file__))[0]
    
    # Valores padrão de tolerância, iterações e intervalos iniciais para os dois patamares de tempo
    padroes = [
        "tolerancia:1e-5\n", 
        "max_iteracoes:100\n",
        "inf_10pct:1.0\n",
        "sup_10pct:2.0\n",
        "x0_10pct:0.5\n",
        "inf_90pct:5.0\n",
        "sup_90pct:9.0\n",
        "x0_90pct:2.5\n"
    ]
    
    # Preencho o arquivo de configuração (.txt) automaticamente se ele não existir
    config, pasta_saida = ferramentas.preparar_diretorios(nome_script, padroes)
    if not config:
        print(f"-> Preencha o arquivo de configuração e rode novamente!")
        return

    # Modelagem matemática do problema: calculamos o tempo t em que a resposta 
    # atinge 10% e 90% do valor assintótico, junto com suas derivadas analíticas exatas
    equacoes = {
        'Tempo_10_pct': {
            'f': lambda t: 1 - (1 + t + (t**2)/2) * math.exp(-t) - 0.1,
            'f_linha': lambda t: (t**2 / 2) * math.exp(-t)
        },
        'Tempo_90_pct': {
            'f': lambda t: 1 - (1 + t + (t**2)/2) * math.exp(-t) - 0.9,
            'f_linha': lambda t: (t**2 / 2) * math.exp(-t)
        }
    }

    tol = config.get('tolerancia', 1e-5)
    max_it = int(config.get('max_iteracoes', 100))
    resultados_gerais = []

    print(f"\n=== EXECUÇÃO: {nome_script.upper()} (Amplificador R-C) ===")

    for nome_eq, funcoes in equacoes.items():
        print(f"\n>> Processando {nome_eq}...")
        
        funcao_objetivo = funcoes['f']
        derivada_objetivo = funcoes['f_linha']

        # Puxo os limites e chutes iniciais específicos para cada patamar (10% ou 90%)
        lim_inf = config.get('inf_10pct' if '10' in nome_eq else 'inf_90pct', 1.0)
        lim_sup = config.get('sup_10pct' if '10' in nome_eq else 'sup_90pct', 2.0)
        chute_ini = config.get('x0_10pct' if '10' in nome_eq else 'x0_90pct', 0.5)

        # Agrupo os 4 métodos numéricos de busca de raízes que vamos testar comparativamente
        metodos = {
            "Bissecção": lambda: raizes.metodo_bisseccao(funcao_objetivo, lim_inf, lim_sup, tol, max_it),
            "Falsa Posição": lambda: raizes.metodo_falsa_posicao(funcao_objetivo, lim_inf, lim_sup, tol, max_it),
            "Newton-Raphson": lambda: raizes.metodo_newton_raphson(funcao_objetivo, derivada_objetivo, chute_ini, tol, max_it),
            "Secante": lambda: raizes.metodo_secante(funcao_objetivo, lim_inf, lim_sup, tol, max_it)
        }

        for nome_metodo, rotina in metodos.items():
            # Executo o método e recupero a raiz, as iterações e o log detalhado
            raiz_calc, iteracoes_gastas, log_execucao = rotina()
            erro_final = log_execucao[-1]['erro_relativo'] if log_execucao else 0.0
            
            # Salvo o histórico individual de cada método em formato CSV
            nome_arquivo = f"{nome_script}_{nome_eq}_{nome_metodo.replace(' ', '').replace('ç', 'c').replace('ã', 'a').lower()}.csv"
            ferramentas.exportar_dados_csv(os.path.join(pasta_saida, nome_arquivo), log_execucao)
            
            resultados_gerais.append({
                "Equacao": nome_eq,
                "Metodo": nome_metodo,
                "Raiz_Encontrada": raiz_calc,
                "Iteracoes": iteracoes_gastas,
                "Erro_Terminal": erro_final
            })

    # Salvo o consolidado geral com o resumo de todos os métodos
    ferramentas.exportar_dados_csv(os.path.join(pasta_saida, f"{nome_script}_resumo.csv"), resultados_gerais)

    print("\n[Resumo dos Resultados]")
    for res in resultados_gerais:
        print(f"{res['Equacao']:<15} | {res['Metodo']:<15} | t = {res['Raiz_Encontrada']:<10.6f} | Iter: {res['Iteracoes']}")

if __name__ == '__main__':
    executar_analise_amplificador()