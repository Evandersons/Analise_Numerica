import warnings


def _erro_relativo(x_novo, x_antigo):
    # Critério de parada ÚNICO para os quatro métodos: |x_k - x_(k-1)| / |x_k|.
    # Se a raiz for 0, cai para o erro absoluto (evita divisão por zero).
    if x_antigo is None:
        return float('inf')  # 1ª iteração dos métodos de intervalo: ainda não há x anterior
    if x_novo != 0.0:
        return abs(x_novo - x_antigo) / abs(x_novo)
    return abs(x_novo - x_antigo)


def _validar_intervalo(f, a, b):
    """Confere o Teorema de Bolzano. Devolve (f(a), f(b), raiz_exata_ou_None)."""
    if a >= b:
        raise ValueError(f"Intervalo inválido: limite_inf={a} deve ser menor que limite_sup={b}.")
    fa, fb = f(a), f(b)
    # raiz exatamente num extremo: f(a)*f(b) < 0 daria falso, então trato antes
    if fa == 0.0:
        return fa, fb, a
    if fb == 0.0:
        return fa, fb, b
    if fa * fb > 0:
        raise ValueError(f"Sem troca de sinal em [{a}, {b}]: f(a)={fa:.6g}, f(b)={fb:.6g}. "
                         "Não há garantia de raiz no intervalo.")
    return fa, fb, None


def metodo_bisseccao(f, limite_inf, limite_sup, tolerancia=1e-6, max_iteracoes=100):
    # Bissecção: divido [a, b] ao meio e fico com o lado onde há troca de sinal.
    # Convenção deste módulo: k = 1, 2, 3... = número de iterações realizadas.
    fa, fb, raiz_exata = _validar_intervalo(f, limite_inf, limite_sup)
    if raiz_exata is not None:
        return raiz_exata, 0, []

    relatorio = []
    x_anterior = None

    for k in range(1, max_iteracoes + 1):
        x_medio = (limite_inf + limite_sup) / 2.0
        f_medio = f(x_medio)
        erro = 0.0 if f_medio == 0.0 else _erro_relativo(x_medio, x_anterior)

        relatorio.append({
            'iteracao': k,
            'lim_inf': limite_inf,
            'lim_sup': limite_sup,
            'x_aprox': x_medio,
            'f(x)': f_medio,
            'erro_relativo': erro
        })

        if f_medio == 0.0 or erro < tolerancia:
            return x_medio, k, relatorio

        # guardo f nos extremos para não reavaliar a função à toa
        if fa * f_medio < 0:
            limite_sup, fb = x_medio, f_medio
        else:
            limite_inf, fa = x_medio, f_medio
        x_anterior = x_medio

    warnings.warn(f"Bissecção não convergiu em {max_iteracoes} iterações "
                  f"(erro relativo = {erro:.3e} > {tolerancia:.1e}).")
    return x_medio, len(relatorio), relatorio


def metodo_falsa_posicao(f, limite_inf, limite_sup, tolerancia=1e-6, max_iteracoes=100):
    # Falsa Posição (clássica): usa o ponto onde a reta que liga (a,f(a)) a (b,f(b))
    # cruza o eixo x. Um dos extremos pode ficar "preso", por isso o intervalo
    # não encolhe até zero e o critério de parada é o de x_k vs x_(k-1).
    fa, fb, raiz_exata = _validar_intervalo(f, limite_inf, limite_sup)
    if raiz_exata is not None:
        return raiz_exata, 0, []

    relatorio = []
    x_anterior = None

    for k in range(1, max_iteracoes + 1):
        # fa e fb têm sinais opostos (garantido pela validação), então fa - fb != 0
        x_aprox = (limite_inf * fb - limite_sup * fa) / (fb - fa)
        f_aprox = f(x_aprox)
        erro = 0.0 if f_aprox == 0.0 else _erro_relativo(x_aprox, x_anterior)

        relatorio.append({
            'iteracao': k,
            'lim_inf': limite_inf,
            'lim_sup': limite_sup,
            'x_aprox': x_aprox,
            'f(x)': f_aprox,
            'erro_relativo': erro
        })

        if f_aprox == 0.0 or erro < tolerancia:
            return x_aprox, k, relatorio

        if fa * f_aprox < 0:
            limite_sup, fb = x_aprox, f_aprox
        else:
            limite_inf, fa = x_aprox, f_aprox
        x_anterior = x_aprox

    warnings.warn(f"Falsa Posição não convergiu em {max_iteracoes} iterações "
                  f"(erro relativo = {erro:.3e} > {tolerancia:.1e}).")
    return x_aprox, len(relatorio), relatorio


def metodo_newton_raphson(f, f_linha, x_inicial, tolerancia=1e-6, max_iteracoes=100):
    # Newton-Raphson: x_(k+1) = x_k - f(x_k)/f'(x_k), com f' analítica passada de fora.
    relatorio = []
    x_atual = x_inicial

    for k in range(1, max_iteracoes + 1):
        f_x = f(x_atual)
        derivada = f_linha(x_atual)

        if derivada == 0.0:
            warnings.warn(f"Newton parou na iteração {k}: f'({x_atual}) = 0 (tangente horizontal).")
            return x_atual, len(relatorio), relatorio

        x_proximo = x_atual - f_x / derivada
        f_proximo = f(x_proximo)
        erro = _erro_relativo(x_proximo, x_atual)

        relatorio.append({
            'iteracao': k,
            'x_aprox': x_proximo,
            'f(x)': f_proximo,
            'f_linha(x)': derivada,
            'erro_relativo': erro
        })

        if f_proximo == 0.0 or erro < tolerancia:
            return x_proximo, k, relatorio

        x_atual = x_proximo

    warnings.warn(f"Newton não convergiu em {max_iteracoes} iterações "
                  f"(erro relativo = {erro:.3e} > {tolerancia:.1e}).")
    return x_atual, len(relatorio), relatorio


def metodo_secante(f, x0, x1, tolerancia=1e-6, max_iteracoes=100):
    # Secante: como o Newton, mas a derivada vira a inclinação da reta pelos
    # dois últimos pontos. Não exige troca de sinal, só dois chutes distintos.
    if x0 == x1:
        raise ValueError("Secante precisa de dois pontos iniciais distintos (x0 != x1).")

    relatorio = []
    x_proximo = x1
    f_x0, f_x1 = f(x0), f(x1)

    for k in range(1, max_iteracoes + 1):
        variacao_y = f_x1 - f_x0
        if variacao_y == 0.0:
            warnings.warn(f"Secante parou na iteração {k}: f(x0) == f(x1) (reta horizontal).")
            return x_proximo, len(relatorio), relatorio

        x_proximo = x1 - f_x1 * (x1 - x0) / variacao_y
        f_proximo = f(x_proximo)
        erro = _erro_relativo(x_proximo, x1)

        relatorio.append({
            'iteracao': k,
            'x_aprox': x_proximo,
            'f(x)': f_proximo,
            'erro_relativo': erro
        })

        if f_proximo == 0.0 or erro < tolerancia:
            return x_proximo, k, relatorio

        # desliza a janela e reaproveita f já calculado (1 avaliação nova por iteração)
        x0, f_x0 = x1, f_x1
        x1, f_x1 = x_proximo, f_proximo

    warnings.warn(f"Secante não convergiu em {max_iteracoes} iterações "
                  f"(erro relativo = {erro:.3e} > {tolerancia:.1e}).")
    return x_proximo, len(relatorio), relatorio