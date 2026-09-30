import warnings

def escalar_linhas(A):
    """Divide cada linha pelo seu maior valor absoluto."""
    return [[v / max(abs(u) for u in linha) for v in linha] for linha in A]

def dominancia_diagonal(A):
    """Verifica a dominância diagonal estrita e fraca."""
    estrita = all(abs(A[i][i]) > sum(abs(A[i][j]) for j in range(len(A)) if j != i) for i in range(len(A)))
    fraca = all(abs(A[i][i]) >= sum(abs(A[i][j]) for j in range(len(A)) if j != i) for i in range(len(A)))
    return estrita, fraca

def validar_dimensoes(A, b):
    # Confiro se A é quadrada e se b tem o mesmo tamanho antes de qualquer conta.
    # Evita um erro lá no meio do algoritmo por causa de dimensão errada.
    n = len(A)
    if len(b) != n:
        raise ValueError("Erro: O vetor b deve ter a mesma dimensão das linhas da matriz A.")
    for linha in A:
        if len(linha) != n:
            raise ValueError("Erro: A matriz A deve ser perfeitamente quadrada (N x N).")


def clonar_sistema(A, b):
    """Impede que as operações modifiquem o sistema original na memória."""
    # faço uma cópia porque os métodos abaixo alteram A e b linha por linha
    # (pivotamento, eliminação...) e eu não quero estragar o que a pessoa me passou
    A_clonada = [[float(valor) for valor in linha] for linha in A]
    b_clonado = [float(valor) for valor in b]
    return A_clonada, b_clonado


def resolver_triangular_superior(U, y, tol_pivo=1e-12):
    # substituição "de trás pra frente": já sei x[n-1] direto (última linha só tem
    # um termo), uso ele pra achar x[n-2], e assim vou subindo até x[0]
    n = len(U)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        soma = sum(U[i][j] * x[j] for j in range(i + 1, n))  # o que já foi resolvido
        if abs(U[i][i]) < tol_pivo:
            raise ValueError(f"Diagonal principal nula na linha {i}. Sistema sem solução única.")
        x[i] = (y[i] - soma) / U[i][i]
    return x


def resolver_triangular_inferior(L, b, tol_pivo=1e-12):
    # o espelho da função anterior: aqui ando "de frente pra trás", porque
    # L é triangular inferior (a primeira linha já dá y[0] direto)
    n = len(L)
    y = [0.0] * n
    for i in range(n):
        soma = sum(L[i][j] * y[j] for j in range(i))
        if abs(L[i][i]) < tol_pivo:
            raise ValueError(f"Diagonal principal nula na linha {i}. Sistema sem solução única.")
        y[i] = (b[i] - soma) / L[i][i]
    return y


def resolver_gauss(A, b, usar_pivotamento=True, tol_pivo=1e-12):
    # Eliminação de Gauss: zero as colunas abaixo da diagonal, uma coluna k por vez,
    # até sobrar um sistema triangular superior, que aí é só chamar a substituição.
    validar_dimensoes(A, b)
    U, y = clonar_sistema(A, b)
    n = len(U)
    historico = []

    for k in range(n - 1):
        if usar_pivotamento:
            # pivotamento parcial: troco pela linha com maior valor absoluto na coluna k
            # antes de dividir por ela. Evita usar um pivô muito pequeno, que amplifica
            # erro numérico (é exatamente o problema do slide de matrizes mal-condicionadas)
            linha_max = max(range(k, n), key=lambda i: abs(U[i][k]))
            if linha_max != k:
                U[k], U[linha_max] = U[linha_max], U[k]
                y[k], y[linha_max] = y[linha_max], y[k]

        pivo = U[k][k]
        if abs(pivo) < tol_pivo:
            raise ValueError("Pivô extremamente próximo de zero. Risco de singularidade.")

        for i in range(k + 1, n):
            # fator que, multiplicado pela linha do pivô e subtraído da linha i,
            # zera exatamente o elemento U[i][k]
            fator_multiplicacao = U[i][k] / pivo
            for j in range(k, n):
                U[i][j] -= fator_multiplicacao * U[k][j]
            y[i] -= fator_multiplicacao * y[k]

            historico.append({
                "etapa_k": k,
                "linha_processada": i,
                "fator_m": fator_multiplicacao
            })

    vetor_solucao = resolver_triangular_superior(U, y, tol_pivo)
    return vetor_solucao, n - 1, historico


def resolver_lu(A, b, usar_pivotamento=True, tol_pivo=1e-12):
    # Fatoração LU (Doolittle) com pivotamento parcial: em vez de resolver Ax=b direto,
    # separo A em L (triangular inferior, diagonal com 1) e U (triangular superior),
    # de forma que P*A = L*U, onde P é a permutação de linhas feita pelo pivotamento.
    # Vale a pena principalmente se eu for resolver o mesmo A com vários b diferentes:
    # a fatoração é feita uma vez só, e cada b novo é só duas substituições.
    validar_dimensoes(A, b)
    n = len(A)
    U = [[float(v) for v in linha] for linha in A]
    L = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    P = list(range(n))  # guarda a ordem original das linhas depois das trocas de pivotamento
    historico = []

    for k in range(n - 1):
        if usar_pivotamento:
            linha_max = max(range(k, n), key=lambda i: abs(U[i][k]))
            if linha_max != k:
                U[k], U[linha_max] = U[linha_max], U[k]
                P[k], P[linha_max] = P[linha_max], P[k]
                # os fatores de L calculados nas colunas anteriores também precisam
                # trocar de linha aqui, senão L deixa de "casar" com U e com P
                for c in range(k):
                    L[k][c], L[linha_max][c] = L[linha_max][c], L[k][c]

        pivo = U[k][k]
        if abs(pivo) < tol_pivo:
            raise ValueError("Pivô nulo/quase nulo encontrado durante a fatoração LU.")

        for i in range(k + 1, n):
            fator = U[i][k] / pivo
            L[i][k] = fator  # aqui é a diferença pro Gauss comum: guardo o fator em vez de descartar
            for j in range(k, n):
                U[i][j] -= fator * U[k][j]

            historico.append({"etapa_k": k, "linha_processada": i, "L_ij_armazenado": fator})

    # como troquei linhas durante o processo (P), preciso aplicar a mesma troca em b
    # antes de resolver — senão estaria resolvendo L*U*x = b em vez de L*U*x = P*b
    b_permutado = [b[P[i]] for i in range(n)]
    vetor_y = resolver_triangular_inferior(L, b_permutado, tol_pivo)  # resolve L*y = P*b
    vetor_x = resolver_triangular_superior(U, vetor_y, tol_pivo)      # resolve U*x = y

    total_etapas = (n - 1) + n + n
    return vetor_x, total_etapas, historico


def resolver_jacobi(A, b, tolerancia=1e-6, max_iteracoes=100):
    n = len(A)
    # Validação contra zeros na diagonal principal
    if any(A[i][i] == 0 for i in range(n)):
        raise ZeroDivisionError("Zero na diagonal principal. O método iterativo falhará.")
        
    x_atual = [0.0] * n
    historico = []

    for k in range(1, max_iteracoes + 1):
        x_proximo = [0.0] * n
        for i in range(n):
            soma = sum(A[i][j] * x_atual[j] for j in range(n) if j != i)
            x_proximo[i] = (b[i] - soma) / A[i][i]

        erro = max(abs(x_proximo[i] - x_atual[i]) for i in range(n))
        max_x = max(abs(xi) for xi in x_proximo)
        if max_x != 0:
            erro /= max_x

        historico.append({'iteracao': k, 'x': x_proximo.copy(), 'erro': erro})

        if erro < tolerancia:
            return x_proximo, k, historico
            
        x_atual = x_proximo

    warnings.warn(f"Jacobi não convergiu em {max_iteracoes} iterações "
                  f"(erro = {historico[-1]['erro']:.3e} > {tolerancia:.1e}).")
    return x_proximo, len(historico), historico


def resolver_seidel(A, b, tolerancia=1e-6, max_iteracoes=100):
    n = len(A)
    # Validação contra zeros na diagonal principal
    if any(A[i][i] == 0 for i in range(n)):
        raise ZeroDivisionError("Zero na diagonal principal. O método iterativo falhará.")
        
    x = [0.0] * n
    historico = []

    for k in range(1, max_iteracoes + 1):
        x_anterior = x.copy()
        for i in range(n):
            soma = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x[i] = (b[i] - soma) / A[i][i]

        erro = max(abs(x[i] - x_anterior[i]) for i in range(n))
        max_x = max(abs(xi) for xi in x)
        if max_x != 0:
            erro /= max_x

        historico.append({'iteracao': k, 'x': x.copy(), 'erro': erro})

        if erro < tolerancia:
            return x, k, historico

    warnings.warn(f"Gauss-Seidel não convergiu em {max_iteracoes} iterações "
                  f"(erro = {historico[-1]['erro']:.3e} > {tolerancia:.1e}).")
    return x, len(historico), historico


def resolver_jordan(A, b, usar_pivotamento=True, tol_pivo=1e-12):
    # Gauss-Jordan: em vez de parar no sistema triangular (como no Gauss comum),
    # continuo zerando TAMBÉM acima da diagonal, até sobrar a matriz identidade.
    # Vantagem: y já sai pronto como solução final, sem precisar de substituição depois
    # — é por isso que uso essa função tanto pra resolver sistema quanto pra inverter matriz.
    validar_dimensoes(A, b)
    U, y = clonar_sistema(A, b)
    n = len(U)
    historico = []

    for k in range(n):
        if usar_pivotamento:
            linha_max = max(range(k, n), key=lambda i: abs(U[i][k]))
            if linha_max != k:
                U[k], U[linha_max] = U[linha_max], U[k]
                y[k], y[linha_max] = y[linha_max], y[k]

        pivo = U[k][k]
        if abs(pivo) < tol_pivo:
            raise ValueError("Pivô próximo de zero. Risco de singularidade.")

        # normalizo a linha inteira do pivô pra ele virar exatamente 1
        pivo_inv = 1.0 / pivo
        U[k] = [valor * pivo_inv for valor in U[k]]
        y[k] *= pivo_inv

        # zero a coluna k em TODAS as outras linhas, acima e abaixo — é essa a
        # diferença pro Gauss comum, que só zera abaixo da diagonal
        for i in range(n):
            if i != k:
                fator = U[i][k]
                U[i] = [U[i][j] - fator * U[k][j] for j in range(n)]
                y[i] -= fator * y[k]
                historico.append({"etapa": k, "linha_alvo": i, "fator_m": fator})

    return y, n, historico


def obter_matriz_inversa(A, tol_pivo=1e-12):
    """Calcula a inversa de A resolvendo Ax = I coluna por coluna via Gauss-Jordan."""
    # a ideia: A * A^-1 = I, então a coluna j da inversa é exatamente a solução
    # de A*x = e_j (e_j é a coluna j da matriz identidade). Resolvo isso n vezes,
    # uma pra cada coluna da identidade.
    n = len(A)
    identidade = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    matriz_inversa = []

    for j in range(n):
        coluna_id = [identidade[i][j] for i in range(n)]
        solucao_coluna, _, _ = resolver_jordan(A, coluna_id, True, tol_pivo)
        matriz_inversa.append(solucao_coluna)  # cada item aqui é uma COLUNA da inversa, não uma linha

    # como guardei coluna por coluna, preciso transpor pra virar linha por linha
    # (formato "normal" de matriz que o resto do código espera)
    return [[matriz_inversa[j][i] for j in range(n)] for i in range(n)]


def norma_infinito_matriz(A):
    """||A||∞ = máximo, entre as linhas, da soma dos valores absolutos."""
    # somo os valores absolutos de cada linha e fico com o maior resultado
    return max(sum(abs(valor) for valor in linha) for linha in A)


def norma_infinito_vetor(x):
    """||x||∞ = maior valor absoluto entre os componentes do vetor."""
    return max(abs(valor) for valor in x)


def numero_condicao(A, tol_pivo=1e-12):
    """Cond[A] = ||A|| · ||A^-1||, usando a norma infinito."""
    # quanto maior esse número, mais "instável" é o sistema: um pequeno erro
    # nos dados de entrada (arredondamento, medição...) pode virar um erro
    # bem maior na solução final — é o assunto de matrizes mal-condicionadas
    A_inversa = obter_matriz_inversa(A, tol_pivo)
    norma_A = norma_infinito_matriz(A)
    norma_A_inv = norma_infinito_matriz(A_inversa)
    return norma_A * norma_A_inv