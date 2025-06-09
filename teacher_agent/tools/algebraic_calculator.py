import os
from wolframalpha import Client


app_id = os.getenv("WOLFRAMALPHA_APPID")
client = Client(app_id)


def algebraic_solver(equation: str) -> str:
    """
    Solve an algebraic equation, e.g. "x^2 - 5x + 6 = 0".
    Returns the roots or factorization.
    """
    return client.query(f"solve {equation}")

def integral_solver(integral: str) -> str:
    """
    Compute an integral, e.g. "∫_0^1 x^2 dx" or solids of revolution.
    """
    return client.query(f"integrate {integral}")

def linear_solver(system: str) -> str:
    """
    Solve a system of linear equations, e.g. "2x + 3y = 6;  x - y = 1".
    """
    return client.query(f"solve {system}")