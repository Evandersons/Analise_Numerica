from codigo import ferramentas


def metodo_bisseccao(f, limite_inf, limite_sup, tolerancia=1e-6, max_iteracoes=100):
    # Bissecção: fico dividindo o intervalo [a, b] ao meio e guardo sempre
    # o lado onde sei que tem troca de sinal (é lá que está a raiz, pelo Bolzano).
    # É o método mais simples e o que menos falha, mas também o mais lento.
    relatorio = []

    for k in range(max_iteracoes):
        x_medio = (limite_inf + limite_sup) / 2.0  # ponto médio do intervalo atual
        f_medio = f(x_medio)

        # erro relativo usando o próprio x_medio como referência
        # (evita dividir por zero quando o intervalo cruza x = 0)
        if x_medio != 0.0:
            erro = abs((limite_sup - limite_inf) / x_medio)
        else:
            erro = abs(limite_sup - limite_inf)

        # guardo tudo pra poder montar a tabela de iterações na apresentação
        relatorio.append({
            'iteracao': k,
            'lim_inf': limite_inf,
            'lim_sup': limite_sup,
            'x_aprox': x_medio,
            'f(x)': f_medio,
            'erro_relativo': erro
        })

        # se caí certinho na raiz ou já bati a tolerância pedida, paro aqui
        if f_medio == 0.0 or erro < tolerancia:
            return x_medio, k, relatorio

        # decido de que lado do intervalo a raiz está: se f(lim_inf) e f(x_medio)
        # têm sinais opostos, a raiz está entre eles; senão, está no outro lado
        if ferramentas.houve_troca_sinal(f, limite_inf, x_medio):
            limite_sup = x_medio  # raiz entre limite_inf e x_medio
        else:
            limite_inf = x_medio  # raiz entre x_medio e limite_sup

    # se não convergiu dentro do número máximo de iterações, devolvo o melhor valor achado
    return x_medio, max_iteracoes, relatorio


def metodo_falsa_posicao(f, limite_inf, limite_sup, tolerancia=1e-6, max_iteracoes=100):
    # Falsa Posição: em vez de partir sempre no meio do intervalo (como na bissecção),
    # traço a reta que liga (a, f(a)) a (b, f(b)) e uso o ponto onde ela cruza o eixo x.
    # Na prática costuma convergir bem mais rápido, porque "mira" melhor na raiz.
    relatorio = []

    for k in range(max_iteracoes):
        # x da iteração anterior, pra medir o quanto a aproximação mudou
        x_anterior = relatorio[-1]['x_aprox'] if relatorio else limite_inf

        f_inf = f(limite_inf)
        f_sup = f(limite_sup)

        # fórmula da secante geométrica: onde a reta que une os dois pontos cruza y=0
        x_aprox = limite_sup - (f_sup * (limite_inf - limite_sup)) / (f_inf - f_sup)
        f_aprox = f(x_aprox)

        # erro relativo entre a aproximação atual e a anterior
        erro = abs(x_aprox - x_anterior) / abs(x_aprox) if x_aprox != 0.0 else 0.0

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

        # mesma lógica da bissecção pra atualizar o intervalo, só que usando x_aprox
        # em vez do ponto médio — por isso essa é a versão "clássica" (não a modificada)
        if ferramentas.houve_troca_sinal(f, limite_inf, x_aprox):
            limite_sup = x_aprox
        else:
            limite_inf = x_aprox

    return x_aprox, max_iteracoes, relatorio


def metodo_newton_raphson(f, f_linha, x_inicial, tolerancia=1e-6, max_iteracoes=100):
    # Newton-Raphson: uso a reta TANGENTE à curva no ponto atual e vejo onde ela
    # cruza o eixo x. Converge muito mais rápido que os métodos anteriores, mas
    # preciso saber a derivada exata (f_linha é passada de fora, não é aproximada).
    relatorio = []
    x_atual = x_inicial

    for k in range(1, max_iteracoes + 1):
        f_x = f(x_atual)
        derivada = f_linha(x_atual)

        # se a derivada zera, a tangente fica horizontal e o método trava
        # (dividiria por zero) — melhor parar aqui do que quebrar o programa
        if derivada == 0.0:
            print("-> Parada de Segurança: A derivada se anulou. Evitando divisão por zero.")
            break

        # a fórmula do método em si: x_(k+1) = x_k - f(x_k) / f'(x_k)
        x_proximo = x_atual - (f_x / derivada)

        erro = abs(x_proximo - x_atual) / abs(x_proximo) if x_proximo != 0.0 else abs(x_proximo - x_atual)

        relatorio.append({
            'iteracao': k,
            'x_aprox': x_proximo,
            'f(x)': f(x_proximo),
            'f_linha(x)': derivada,
            'erro_relativo': erro
        })

        if f(x_proximo) == 0.0 or erro < tolerancia:
            return x_proximo, k, relatorio

        x_atual = x_proximo

    # se a derivada zerou no meio do caminho, devolvo o último x válido em vez de quebrar
    return x_atual, max_iteracoes, relatorio


def metodo_secante(f, x0, x1, tolerancia=1e-6, max_iteracoes=100):
    # Secante: a ideia é a mesma do Newton-Raphson, mas troco a derivada exata
    # por uma reta que passa pelos DOIS últimos pontos calculados (x0 e x1).
    # Assim não preciso saber f'(x) — útil quando a derivada é difícil de obter.
    relatorio = []
    x_proximo = x1  # valor de segurança: se o método parar já na 1ª iteração, tem o que devolver

    for k in range(1, max_iteracoes + 1):
        f_x0 = f(x0)
        f_x1 = f(x1)

        variacao_y = f_x1 - f_x0
        if variacao_y == 0.0:
            # a reta secante ficou horizontal (f(x0) == f(x1)) — não dá pra continuar
            print("-> Parada de Segurança: A função achatou. A secante tornou-se horizontal.")
            break

        # mesma fórmula do Newton, só que a "derivada" vira a inclinação da reta
        # que liga os dois últimos pontos em vez de uma derivada de verdade
        x_proximo = x1 - f_x1 * (x1 - x0) / variacao_y
        f_proximo = f(x_proximo)

        erro = abs(x_proximo - x1) / abs(x_proximo) if x_proximo != 0.0 else abs(x_proximo - x1)

        relatorio.append({
            'iteracao': k,
            'x_aprox': x_proximo,
            'f(x)': f_proximo,
            'erro_relativo': erro
        })

        if f_proximo == 0.0 or erro < tolerancia:
            return x_proximo, k, relatorio

        # "desliza" a janela dos dois pontos: descarto o mais antigo (x0),
        # o que era x1 vira o novo x0, e o ponto recém-calculado vira o novo x1
        x0 = x1
        x1 = x_proximo

    return x_proximo, max_iteracoes, relatorio