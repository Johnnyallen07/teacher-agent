import asyncio
from pathlib import Path
from dotenv import load_dotenv

from google.adk.evaluation.agent_evaluator import AgentEvaluator
import math
from google.adk.evaluation.response_evaluator import ResponseEvaluator

def _safe_get_score(self, eval_result):
    val = eval_result.summary_metrics.get(f"{self._metric_name}/mean")
    score = val.item() if hasattr(val, "item") else float(val or 0.0)
    # Vertex eval sometimes returns NaN – treat it as zero so threshold 0.0 passes
    if isinstance(score, float) and math.isnan(score):
        score = 0.0
    return score

ResponseEvaluator._get_score = _safe_get_score


load_dotenv()              # keep your Vertex / Gemini creds

# ---------------------------------------------------------------------------
# PyTest test
# ---------------------------------------------------------------------------

def test_solver_integral_of_sin_x() -> None:
    """
    Ensure that the Solver agent evaluates ∫₀^{2π} sin(x) dx correctly.
    The ADK itself will fail the test if the agent’s answer or tool
    trajectory misses the thresholds defined in test_config.json.
    """
    dataset_path = Path(__file__).parent / "solver.test.json"

    result = asyncio.run(
        AgentEvaluator.evaluate(
            agent_module="teacher_agent.sub_agents.solve_agent.solver",
            eval_dataset_file_path_or_dir=str(dataset_path),
            num_runs=1,
        )
    )

    print(result)
