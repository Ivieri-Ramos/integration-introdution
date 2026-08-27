import sympy as sp

x = sp.Symbol('x')

def ftc_primitiva_conhecida(F:sp.Expr, a, b):
    """
    Aplica o Teorema Fundamental do Cálculo usando uma primitiva conhecida
        Dada uma primitiva F de f, calcula:
                              ∫ₐᵇ f(x) dx = F(b) − F(a)

       F:sp.Expr = primitiva de f
       a = limite inferior
       b = limite superior

       Retorna:
        sp.Expr = valor exato da integral definida
    """
    F_b = sp.Expr(F.subs(x, b))
    F_a = sp.Expr(F.subs(x, a))
    return F_b - F_a

def ftc_integrar(f, a, b):
    """
    Aplica o Teorema Fundamental do Cálculo integrando a função original
    Calcula a integral definida ∫ₐᵇ f(x) dx diretamente.

    f:sp.Expr = função original
    a, b = limites da integração

    Retorna:
     sp.Expr = valor exato da integral definida
    """
    return sp.integrate(f, (x, a, b))


