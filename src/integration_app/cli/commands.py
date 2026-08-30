import sympy as sp
from src.cli.app import app
import src.cli.view as view
import typer

from src.ftc.TFC import ftc_primitiva_conhecida
from src.math_parser import parse_math, MathParserError

def to_expr(valor: str) -> sp.Expr:
    return parse_math(valor)

@app.command()
def integrar_primitiva(
        primitiva: str = typer.Option("x**3/3", "--primitiva", "-F", help="Primitiva F(x)"),
        limite_inferior: str = typer.Option("0", "--limite-inferior", "-a", help="Limite inferior"),
        limite_superior: str = typer.Option("1", "--limite-superior", "-b", help="Limite superior"),
        variavel : str = typer.Option("x", "--variavel", "-v", help="Variavel de integração"),
) -> None:
    """
    Calcula ∫ₐᵇ f(x) dx usando uma primitiva fornecida
    Aplica o TFC: F(b) − F(a).
    :param primitiva: A primitiva F(x)
    :param limite_inferior: Limite a
    :param limite_superior: Limite b
    :param variavel: Variavel (ex : x, y, t)
    """
    try:
        F = to_expr(primitiva)
        a = to_expr(limite_inferior)
        b = to_expr(limite_superior)
        v = sp.Symbol(variavel)
        resultado = ftc_primitiva_conhecida(F, a, b, v)
        mensagem = f"∫_{{{a}}}^{{{b}}} f({variavel}) d{variavel} = {resultado}"

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
        variavel : str = typer.Option("x", "--variavel", "-v", help="Variavel de integração"),
) -> None:
    """
    Calcula ∫ₐᵇ f(x) dx sem fornecer primitiva.

    O SymPy descobre a primitiva e aplica o TFC.
    """
    try:
        f_sympy = to_expr(funcao)
        a = to_expr(limite_inferior)
        b = to_expr(limite_superior)
        v = sp.Symbol(variavel)

        F = sp.integrate(f_sympy, v)
        resultado = ftc_primitiva_conhecida(F, a, b, v)

        mensagem = f"∫_{{{a}}}^{{{b}}} {funcao} d{variavel} = {resultado}"
        if mostrar_primitiva:
            mensagem = f"Primitiva encontrada: F({variavel}) = {F}\n" + mensagem

        view.show(mensagem)

    except MathParserError as e:
        view.show_error(f"Erro: {e}")
    except ValueError as e:
        view.show_error(f"Erro: {e}")
