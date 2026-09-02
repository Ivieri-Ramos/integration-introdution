from typing import cast

import typer

from integration_app.csv.leitor import ler_dados_csv

import integration_app.cli.view as view
from integration_app.cli.app import app
from integration_app.ftc.TFC import *
from integration_app.graphics.core import *
from integration_app.math_parser import parse_math, MathParserError
import simpson_ext

def sympy_to_exprtk(expressao: sp.Expr) -> str:
    ln_func = sp.Function('ln')
    expressao = expressao.replace(sp.log, ln_func)

    expr_str = str(expressao)

    expr_str = expr_str.replace("**", "^")
    expr_str = expr_str.replace("Abs", "abs")

    return expr_str

@app.command()
def integrar_primitiva(
        primitiva: str = typer.Option("x^3 + 2x + 1", "--primitiva", "-f", help="Primitiva F(x)"),
        limite_inferior: str = typer.Option("0", "--limite-inferior", "-a", help="Limite inferior"),
        limite_superior: str = typer.Option("2", "--limite-superior", "-b", help="Limite superior"),
        plot: str = typer.Option("", "--plot", help="Gráfico da função primitiva")
) -> None:
    """
    Calcula ∫ₐᵇ f(x) dx usando uma primitiva fornecida
    Aplica o TFC: F(b) − F(a).
    """
    try:
        funcao = parse_math(primitiva)
        a = parse_math(limite_inferior)
        b = parse_math(limite_superior)
        (var,) = funcao.free_symbols

        resultado = ftc_primitiva_conhecida(funcao, a, b, cast(sp.Symbol, var))
        mensagem = f"Primitiva de: {funcao} em [{a}, {b}] = {resultado}\n"

        if plot:
            plot_function_area(funcao, a, b, plot)

        view.show(mensagem)

    except MathParserError as e:
        view.show_error(f"Erro: {e}")
    except ValueError as e:
        view.show_error(f"Erro: {e}")


@app.command()
def integrar(
        funcao: str = typer.Option("x^3 + 2x + 1", "--funcao", "-f", help="Função f(x)"),
        limite_inferior: str = typer.Option("0", "--limite-inferior", "-a", help="Limite inferior"),
        limite_superior: str = typer.Option("2", "--limite-superior", "-b", help="Limite superior"),
        plot: str = typer.Option("", "--plot", help="Gráfico da função original")
) -> None:
    """
    Calcula ∫ₐᵇ f(x) dx sem fornecer primitiva.

    O SymPy descobre a primitiva e aplica o TFC.
    """
    try:
        f_sympy = parse_math(funcao)
        a = parse_math(limite_inferior)
        b = parse_math(limite_superior)
        (var,) = f_sympy.free_symbols

        resultado = ftc_integrar(f_sympy, a, b, cast(sp.Symbol, var))

        mensagem = f"Integral de: {funcao} em [{a}, {b}] = {resultado}\n"

        if plot:
            plot_function_area(f_sympy, a, b, plot)

        view.show(mensagem)

    except MathParserError as e:
        view.show_error(f"{e}")
    except ValueError as e:
        view.show_error(f"{e}")


@app.command()
def simpson(
        funcao: str = typer.Option("x^3 + 2x + 1", "--funcao", "-f", help="Função f(x)"),
        limite_inferior: str = typer.Option("0", "--limite-inferior", "-a", help="Limite inferior"),
        limite_superior: str = typer.Option("2", "--limite-superior", "-b", help="Limite superior"),
        intervalos: int = typer.Option(100, "--intervalos", "-n", help="Número de intervalos para calcular"),
        plot_erro: str = typer.Option("", "--plot-erro",
                                      help="Nome do arquivo para salvar o gráfico de erro (ex: erro.png)"),
        plot_parabolas: str = typer.Option("", "--plot-parabolas",
                                       help="Nome do arquivo para salvar a interpretação geométrica (ex: parabolas.png)"),
        tabela: bool = typer.Option(False, "--tabela", help="Exibe tabela de evolução do erro até N intervalos")
) -> None:
    """
    Calcula Simpson usando uma função feita em C++ em qualquer intervalo
    """
    try:
        f_sympy = parse_math(funcao)
        a = parse_math(limite_inferior)
        b = parse_math(limite_superior)
        (var,) = f_sympy.free_symbols
        exprtk_func = sympy_to_exprtk(f_sympy)

        calculo: float = simpson_ext.SimpsonIntegrator.integrate(exprtk_func, a, b, intervalos)

        resultado_tfc = ftc_integrar(f_sympy, a, b, cast(sp.Symbol, var))

        erro_abs = abs(resultado_tfc - calculo)

        if tabela:
            colunas = ["N (Intervalos)", "Valor Calculado", "Erro Absoluto", "Meta < 10⁻⁴"]
            linhas = []
            n_atual = 2

            while n_atual <= intervalos:
                calc_n = simpson_ext.SimpsonIntegrator.integrate(exprtk_func, a, b, n_atual)
                erro_n= abs(resultado_tfc - calc_n)

                erro_n = erro_n if erro_n > 0 else 1e-16

                meta_atingida = "[green]Atingiu[/green]" if erro_n < 1e-4 else "[red]Falhou[/red]"

                linhas.append([str(n_atual), f"{calc_n:.8f}", f"{erro_n:.2e}", meta_atingida])

                if n_atual * 2 > intervalos and n_atual != intervalos:
                    n_atual = intervalos
                else:
                    n_atual *= 2

            view.show_table(f"Função: {funcao}", colunas, linhas)

        if plot_erro:
            plot_simpson_error_dynamic(f_sympy, a, b, resultado_tfc, max_n=intervalos, filename=plot_erro)

        if plot_parabolas:
            plot_simpson_parabolas(f_sympy, a, b, n=intervalos, filename=plot_parabolas)

        view.show(f"Resultado de Simpson: {calculo}\nErro absoluto ao TFC: {erro_abs:.2e}")

    except MathParserError as e:
        view.show_error(f"{e}")
    except ValueError as e:
        view.show_error(f"{e}")


@app.command()
def csv(
        nome_arquivo: str = typer.Option("assets/bancos_dados_integracao_numerica.csv", "-f"),
        grafico: str = typer.Option("", "--plot", help="Nome do arquivo para salvar o gráfico")
) -> None:
    """
    Calcula Simpson a partir de dados discretos (x, y) de um arquivo .csv.
    """
    try:
        vectors = ler_dados_csv(nome_arquivo)
        result = simpson_ext.SimpsonIntegrator.integrate(vectors.vector_x, vectors.vector_y)

        view.show(f"Resultado de Simpson: {result}")

        if grafico:
            plot_csv_data(
                vectors.vector_x, vectors.vector_y, grafico,
                titulo="Análise do Banco de Dados",
                x_label="Posição (m)",
                y_label="Densidade (kg/m)"
            )

    except ValueError as e:
        view.show_error(f"{e}")