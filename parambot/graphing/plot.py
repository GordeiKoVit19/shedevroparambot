import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, solve, lambdify

x, a = symbols('x a')

def plot_graph(numerator_expr=None, denominator_expr=None, limit=10, y_limit=10):
    x_vals = np.linspace(-limit, limit, 2000)
    plt.figure(figsize=(8, 8))

    if numerator_expr is not None:
        num_solutions = solve(numerator_expr, a)
        for expr in num_solutions:
            func = lambdify(x, expr, modules=['numpy'])
            y_vals = func(x_vals)
            y_vals[np.iscomplex(y_vals)] = np.nan
            plt.plot(x_vals, y_vals, color='blue')

    if denominator_expr is not None:
        denom_solutions = solve(denominator_expr, a)
        for expr in denom_solutions:
            func = lambdify(x, expr, modules=['numpy'])
            y_vals = func(x_vals)
            y_vals[np.iscomplex(y_vals)] = np.nan
            plt.plot(x_vals, y_vals, linestyle='--', color='orange')

    plt.axhline(0, color='black')
    plt.axvline(0, color='black')
    plt.xlim(-limit, limit)
    plt.ylim(-y_limit, y_limit)
    plt.xticks(np.arange(-limit, limit+1, 1))
    plt.yticks(np.arange(-y_limit, y_limit+1, 1))
    plt.grid(True, linestyle=':', linewidth=0.5)
    plt.xlabel('x')
    plt.ylabel('a')
    plt.title('График a(x)')
    plt.tight_layout()

    filename = 'graph.png'
    plt.savefig(filename)
    plt.close()
    return filename
