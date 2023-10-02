from .taylor import TaylorSeries
from .base_action import BaseAction
from sympy import diff, symbols, lambdify
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')


def newton_method(f, x0, tol=1e-6, max_iter=100):
    x = x0
    df = difference(f)
    for i in range(max_iter):
        fx = float(f(x))
        if abs(fx) < tol:
            return x
        dfx = df(x)
        if dfx == 0:
            break
        x = x - fx / dfx


def difference(f):
    x, y = symbols('x y')
    return lambdify(x, diff(f(x)))


def build_graph(f, x):
    fig, ax = plt.subplots()

    ax.plot(
        x,
        [f(x_) for x_ in x]
    )
    plt.grid()
    plt.show()


def build_graph_params(x, y, point_mode=False):
    fig, ax = plt.subplots()
    if point_mode:
        ax.plot(x, y, '.r')
    else:
        ax.plot(x, y)
    plt.grid()
    plt.show()
