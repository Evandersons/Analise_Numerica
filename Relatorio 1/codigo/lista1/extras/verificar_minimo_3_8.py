# Verificação: onde f(x) tem seu ponto mínimo entre x=1 e a raiz correta?
valor_financiado = 162.0 - 22.0

planos = {
    "Plano A": (valor_financiado / 26.50, 9),
    "Plano B": (valor_financiado / 21.50, 12),
}

for nome, (k, P) in planos.items():
    f = lambda x: k * x**(P + 1) - (k + 1) * x**P + 1

    # testa 1.5 mil pontos entre 1.0000 e 1.1500, de 0.0001 em 0.0001
    pontos = [1.0 + i * 0.0001 for i in range(1501)]
    x_min = min(pontos, key=f)

    print(f"{nome}: mínimo perto de x = {x_min:.4f}, com f(x) = {f(x_min):.4f}")