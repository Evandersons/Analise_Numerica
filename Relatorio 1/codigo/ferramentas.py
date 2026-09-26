import os
import csv

def houve_troca_sinal(f, a, b):
    """Verifica se a função muda de sinal entre os pontos a e b (Teorema de Bolzano)."""
    # Pelo Teorema de Bolzano, se f(a) e f(b) têm sinais opostos, o produto entre eles
    # é menor que zero (< 0), o que garante a existência de pelo menos uma raiz no intervalo.
    return f(a) * f(b) < 0

def calcular_derivada_numerica(f, x, passo=1e-5):
    """Aproxima a derivada de f no ponto x usando diferenças finitas para frente."""
    # Como nem sempre temos a derivada analítica explícita, usamos a inclinação
    # da reta secante com um passo infinitesimal (delta x muito pequeno) para aproximá-la.
    return (f(x + passo) - f(x)) / passo

def exportar_dados_csv(caminho_arquivo, lista_dados, cabecalhos=None):
    """Salva a lista de dicionários do histórico em um arquivo .CSV estruturado."""
    # Se a lista estiver vazia, não há nada para salvar, então encerramos a função
    if not lista_dados:
        return
    
    # Garante que a pasta de destino existe; se não existir, o Python cria automaticamente
    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
    
    # Abre o ficheiro em modo de escrita ('w') com codificação UTF-8 para evitar problemas com acentos
    with open(caminho_arquivo, mode='w', newline='', encoding='utf-8') as arquivo:
        # Se os cabeçalhos não forem passados explicitamente, usamos as chaves do primeiro dicionário
        escritor = csv.DictWriter(arquivo, fieldnames=cabecalhos or lista_dados[0].keys())
        escritor.writeheader()  # Escreve a linha de cabeçalho no CSV
        escritor.writerows(lista_dados)  # Escreve todas as linhas de dados do histórico de iterações

def preparar_diretorios(nome_script, parametros_iniciais=None):
    """Lê o arquivo .txt de configuração e garante que as pastas de saída existam."""
    # Se nenhum parâmetro padrão foi fornecido, definimos tolerância e iterações básicas
    if parametros_iniciais is None:
        parametros_iniciais = ['tolerancia:1e-4\n', 'max_iteracoes:100\n']

    # Definimos a estrutura de pastas do projeto de forma dinâmica a partir da localização atual
    diretorio_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    pasta_entradas = os.path.join(diretorio_base, 'dados', 'entradas')
    pasta_saidas = os.path.join(diretorio_base, 'dados', 'saida', nome_script)

    # Criamos as pastas de entradas e saídas caso ainda não existam
    os.makedirs(pasta_entradas, exist_ok=True)
    os.makedirs(pasta_saidas, exist_ok=True)

    # Caminho do ficheiro de configuração específico para este script (ex: exe_3_3.txt)
    arquivo_config = os.path.join(pasta_entradas, f"{nome_script}.txt")

    # Se o ficheiro de configuração ainda não existir, criamos um template básico automaticamente
    if not os.path.exists(arquivo_config):
        print(f"[{nome_script}] Criando template de configuração em: {arquivo_config}")
        with open(arquivo_config, 'w') as f:
            f.writelines(parametros_iniciais)
        # Retorna None para o dicionário de configs, forçando o script a parar e avisar o utilizador para preencher
        return None, pasta_saidas

    # Se o ficheiro já existe, fazemos a leitura linha a linha dos parâmetros
    configs = {}
    with open(arquivo_config, 'r') as f:
        for linha in f:
            linha = linha.strip()
            # Ignoramos linhas vazias ou comentários iniciados por '#'
            if linha and not linha.startswith('#') and ':' in linha:
                chave, valor = linha.split(':')
                # Convertemos os valores lidos para float para uso direto nos cálculos numéricos
                configs[chave.strip()] = float(valor.strip())

    return configs, pasta_saidas