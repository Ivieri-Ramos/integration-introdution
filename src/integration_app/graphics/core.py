import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sympy as sp
import simpson_ext

os.makedirs("output", exist_ok=True)
OUTPUT: str = "output/"

def plot_function_area(func_sp: sp.Expr, a_sym: sp.Expr, b_sym: sp.Expr, filename: str) -> None:
    a, b = float(a_sym), float(b_sym)
    (var,) = func_sp.free_symbols
    func_num = sp.lambdify(var, func_sp, "numpy")

    x_vals = np.linspace(a, b, 500)
    y_vals = func_num(x_vals)

    plt.figure(figsize=(7, 6))
    plt.plot(x_vals, y_vals, color="blue", linewidth=2, label=f"f({var})")
    plt.fill_between(x_vals, y_vals, alpha=0.3, color="skyblue", label="Área Integrada")

    plt.title(f"Integral de {func_sp} no intervalo [{a}, {b}]")
    plt.xlabel(str(var))
    plt.ylabel("f(x)")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()
    plt.tight_layout()

    plt.savefig(OUTPUT + filename, dpi=300)
    plt.close()


def plot_csv_data(x_vals: list[float], y_vals: list[float], filename: str,
                  titulo: str = "Integração de Dados Discretos",
                  x_label: str = "Eixo X", y_label: str = "Eixo Y") -> None:
    plt.figure(figsize=(8, 6))

    plt.plot(x_vals, y_vals, marker='o', color='purple', linestyle='-', linewidth=2, label="Dados Coletados")

    plt.fill_between(x_vals, y_vals, alpha=0.3, color='mediumpurple', label="Área (Valor da Integral)")

    plt.title(titulo)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()
    plt.tight_layout()

    plt.savefig(OUTPUT + filename, dpi=300)
    plt.close()


def plot_simpson_error_dynamic(func_sympy: sp.Expr, a_sym: sp.Expr, b_sym: sp.Expr, exact_value: sp.Expr, max_n: int,
                               filename: str, tol: float = 1e-4) -> None:
    a, b, exato = float(a_sym), float(b_sym), float(exact_value)
    (var,) = func_sympy.free_symbols
    func_num = sp.lambdify(var, func_sympy, "numpy")

    n_values = []
    n_atual = 2
    while n_atual <= max_n:
        n_values.append(n_atual)
        n_atual *= 2

    if max_n not in n_values:
        n_values.append(max_n)
        n_values.sort()

    erros = []

    for n in n_values:
        x_n = np.linspace(a, b, n + 1)
        y_n = func_num(x_n)
        res_simpson = simpson_ext.SimpsonIntegrator.integrate(x_n, y_n)
        erro_absoluto = abs(res_simpson - exato)
        erros.append(erro_absoluto if erro_absoluto > 0 else 1e-16)

    plt.figure(figsize=(7, 6))
    plt.loglog(n_values, erros, marker="o", color="red", linestyle="-", linewidth=2)
    plt.axhline(y=tol, color='black', linestyle=':', linewidth=2, label=f'Tolerância')

    plt.title(f"Convergência de Erro ({func_sympy})")
    plt.xlabel("Número de Intervalos (n)")
    plt.ylabel("Erro Absoluto")
    plt.grid(True, which="both", linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT + filename, dpi=300)
    plt.close()


def plot_simpson_parabolas(func_sympy: sp.Expr, a_sym: sp.Expr, b_sym: sp.Expr, n: int, filename: str) -> None:
    """
    Plota a função real e sobrepõe as parábolas criadas pelo Método de Simpson
    para ilustrar geometricamente a aproximação.
    """
    a, b = float(a_sym), float(b_sym)

    if n % 2 != 0:
        n += 1

    (var,) = func_sympy.free_symbols
    func_num = sp.lambdify(var, func_sympy, "numpy")

    x_smooth = np.linspace(a, b, 500)
    y_smooth = func_num(x_smooth)

    plt.figure(figsize=(9, 6))
    plt.plot(x_smooth, y_smooth, color="black", linewidth=2, label=f"Função f({var})")

    x_simpson = np.linspace(a, b, n + 1)
    y_simpson = func_num(x_simpson)

    colors = ['skyblue', 'lightgreen', 'salmon', 'plum']

    for i in range(0, n, 2):
        x_points = x_simpson[i:i + 3]
        y_points = y_simpson[i:i + 3]

        poly_coefs = np.polyfit(x_points, y_points, 2)
        poly_func = np.poly1d(poly_coefs)

        x_poly_smooth = np.linspace(x_points[0], x_points[2], 100)
        y_poly_smooth = poly_func(x_poly_smooth)

        color = colors[(i // 2) % len(colors)]

        label = "Área das Parábolas (Simpson)" if i == 0 else ""
        plt.fill_between(x_poly_smooth, y_poly_smooth, alpha=0.6, color=color, label=label)

        plt.plot(x_points, y_points, 'ro')

    plt.title(f"Interpretação Geométrica do Método de Simpson (N={n}) (f(x) = {func_sympy})")
    plt.xlabel(str(var))
    plt.ylabel("f(x)")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT + filename, dpi=300)
    plt.close()