import asyncio
from google.adk.evaluation.agent_evaluator import AgentEvaluator
from dotenv import load_dotenv

# Load environment variables (e.g., API keys)
load_dotenv()

from pathlib import Path


def test_solver_integral_of_sin_x():
    """
    Evaluate the Solver agent on the integral ∫₀^{2π} sin(x) dx and assert the result is 0.
    """
    # # Path to the eval dataset file containing our test case(s)
    # dataset_path = "tests/agent_test/solver.test.json"
    # Resolve the .test.json relative to this test file's directory
    dataset_path = str(Path(__file__).parent / "solver.test.json")

    # Run the evaluation synchronously
    results = asyncio.run(
        AgentEvaluator.evaluate(
            agent_module="teacher_agent.sub_agents.solve_agent.solver",
            eval_dataset_file_path_or_dir=dataset_path,
            num_runs=1,
        )
    )

    # We expect exactly one result entry
    assert len(results) == 1, "Evaluator should return one result per dataset entry"

    result = results[0]
    # Assert the agent succeeded
    assert result.success, f"Test failed: {result.feedback}"

    # Ensure a response was returned
    response = getattr(result, 'response', None)
    assert response is not None, "No response returned from the agent"

    # Check that the integral evaluates to 0
    assert "0" in response, f"Expected '0' in response, got: {response}"
