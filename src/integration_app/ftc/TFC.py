import sympy as sp

def ftc_primitiva_conhecida(primitive: sp.Expr, a: sp.Expr, b: sp.Expr, var: sp.Symbol) -> sp.Expr:
    """
    Aplica o Teorema Fundamental do Cálculo usando uma primitiva conhecida.
    Dada uma primitiva F de f, calcula: ∫ₐᵇ f(x) dx = F(b) − F(a)

    Args:
       primitive (sp.Expr): Primitiva de f
       a (sp.Expr): Limite inferior
       b (sp.Expr): Limite superior
       var (sp.Symbol): Variável

    Returns:
        sp.Expr valor exato da integral definida
    """
    result_b = primitive.subs(var, b)
    result_a = primitive.subs(var, a)

    return result_b - result_a

def ftc_integrar(f: sp.Expr, a: sp.Expr, b: sp.Expr, var: sp.Symbol) -> sp.Expr:
    """
    Aplica o Teorema Fundamental do Cálculo integrando a função original
    Calcula a integral definida ∫ₐᵇ f(x) dx diretamente.

    Args
        f (sp.Expr): função original
        a (sp.Expr): Limite inferior
        b (sp.Expr): Limite superior
        var (sp.Symbol): Variável

    Returns:
        sp.Expr Valor exato da integral definida
    """
    return sp.integrate(f, (var, a, b))


