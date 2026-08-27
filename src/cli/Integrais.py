import sympy as sp

from ftc.TFC import ftc_primitiva_conhecida

x = sp.Symbol('x')

def integrar_com_primitiva(F: sp.Expr, a, b) -> sp.Expr:
    return ftc_primitiva_conhecida(F, a, b)

def integrar_sem_primitiva(f: sp.Expr, a, b) -> sp.Expr:
    F = sp.integrate(f, x)
    return ftc_primitiva_conhecida(F, a, b)