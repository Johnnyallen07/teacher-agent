import os
from wolfram_alpha_service import WolframAlphaService

# 1. Initialize the WolframAlpha client
app_id = os.getenv("API_KEY")
wolfram = WolframAlphaService(app_id=app_id)

# 2. Adapter functions
def algebraic_solver(equation: str) -> str:
    """
    Solve an algebraic equation, e.g. "x^2 - 5x + 6 = 0".
    Returns the roots or factorization.
    """
    # prefix your query so WA knows you want roots
    return wolfram.query(f"solve {equation}")

def integral_solver(integral: str) -> str:
    """
    Compute an integral, e.g. "∫_0^1 x^2 dx" or solids of revolution.
    """
    return wolfram.query(f"integrate {integral}")

def linear_solver(system: str) -> str:
    """
    Solve a system of linear equations, e.g. "2x + 3y = 6;  x - y = 1".
    """
    return wolfram.query(f"solve {system}")