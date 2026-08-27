import sympy as sp
from src.cli.app import app
import src.cli.view as view
import typer

from src.ftc.TFC import x, ftc_primitiva_conhecida
from src.math_parser import parse_math, MathParserError

def to_expr(valor: str) -> sp.Expr:
    return parse_math(valor)

@app.command()
def integrar_com_primitiva(
        primitiva: str = typer.Option("x**3/3", "--primitiva", "-F", help="Primitiva F(x)"),
        limite_inferior: str = typer.Option("0", "--limite-inferior", "-a", help="Limite inferior"),
        limite_superior: str = typer.Option("1", "--limite-superior", "-b", help="Limite superior"),
) -> None:
    """
    Calcula ∫ₐᵇ f(x) dx usando uma primitiva fornecida
    Aplica o TFC: F(b) − F(a).
    :param primitiva: A primitiva F(x)
    :param limite_inferior: Limite a
    :param limite_superior: Limite b
    """
    try:
        F = to_expr(primitiva)
        a = to_expr(limite_inferior)
        b = to_expr(limite_superior)
        resultado = ftc_primitiva_conhecida(F, a, b)
        mensagem = f"∫_{{{a}}}^{{{b}}} f(x) dx = {resultado}"

        view.show(mensagem)

    except MathParserError as e:
        view.show_error(f"Erro: {e}")
    except ValueError as e:
        view.show_error(f"Erro: {e}")

@app.command()
def integrar(
        funcao: str = typer.Option("x**2", "--funcao", "-f", help="Função f(x)"),
        limite_inferior: str = typer.Option("0", "--limite-inferior", "-a", help="Limite inferior"),
        limite_superior: str = typer.Option("1", "--limite-superior", "-b", help="Limite superior"),
        mostrar_primitiva: bool = typer.Option(False, "--mostrar-primitiva", help="Mostra a primitiva"),
) -> None:
    """
    Calcula ∫ₐᵇ f(x) dx sem fornecer primitiva.

    O SymPy descobre a primitiva e aplica o TFC.
    """
    try:
        f_sympy = to_expr(funcao)
        a = to_expr(limite_inferior)
        b = to_expr(limite_superior)

        F = sp.integrate(f_sympy, x)
        resultado = ftc_primitiva_conhecida(F, a, b)

        mensagem = f"∫_{{{a}}}^{{{b}}} {funcao} dx = {resultado}"
        if mostrar_primitiva:
            mensagem = f"Primitiva encontrada: F(x) = {F}\n" + mensagem

        view.show(mensagem)

    except MathParserError as e:
        view.show_error(f"Erro: {e}")
    except ValueError as e:
        view.show_error(f"Erro: {e}")
