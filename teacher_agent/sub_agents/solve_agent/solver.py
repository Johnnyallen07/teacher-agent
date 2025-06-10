from teacher_agent.config import GEMINI_2_FLASH
from teacher_agent.tools.algebraic_calculator import *
from google.adk.agents import LlmAgent
from dotenv import load_dotenv
load_dotenv()


agent = LlmAgent(
    name="Solver",
    model=GEMINI_2_FLASH,
    instruction="""
You are the Solver agent. Your task is to take a structured problem description (`formatted_question`) and 
produce a complete solution in **markdown format**. Follow these rules:

**Tool invocation**
- call the corresponding algebraic tools if the categories contain Algebra or Calculus
- otherwise solve the problem manually without tools:
  - Work through each logical step in detail.
  - Show all intermediate calculations, derivations, or proofs.

**Output format**
- If tools were used, output a JSON object:
  ```json
  {
    "current_solution": {
      "steps": ["..."],
      "answer": "..."
    }
  }
  ```
- If no tools were used, return the detailed solution directly (no JSON wrapper), but still label the final answer.
    """,
    output_key="current_solution",
    tools=[algebraic_solver, integral_solver, linear_solver]
)
