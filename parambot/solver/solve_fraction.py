from sympy import symbols, solve, simplify

x, a = symbols('x a')


def solve_numerator(numerator_expr):
    solutions = solve(numerator_expr, a)
    return solutions

def check_denominator(numerator_expr, a):
    simplified_expr = simplify(numerator_expr)
    if simplified_expr.is_Number and simplified_expr == 0:
        return False
    return True
