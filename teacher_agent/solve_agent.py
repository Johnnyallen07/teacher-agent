from asyncio import Event
from typing import AsyncGenerator
import logging
from google.adk.agents import BaseAgent, LlmAgent, SequentialAgent, LoopAgent
from google.adk.agents.invocation_context import InvocationContext
from streamlit import feedback
from typing_extensions import override


# --- Configure Logging ---


class TeacherAgent(BaseAgent):

    image_recognizer: LlmAgent
    problem_recognizer: LlmAgent
    recognizer: SequentialAgent

    solver: LlmAgent

    answer_checker: LlmAgent
    process_checker: LlmAgent
    checker: LoopAgent
    feedback_agent: LlmAgent



    def __init__(
            self,
            image_recognizer: LlmAgent,
            problem_recognizer: LlmAgent,

            solver: LlmAgent,
            answer_checker: LlmAgent,
            process_checker: LlmAgent,

            feedback_agent: LlmAgent,
            name: str = "TeacherAgent",

    ):
        """
        Initializes the StoryFlowAgent.

        Args:
            image_recognizer: image recognition agent; TODO: try OCR tools for efficiency
            problem_recognizer: detect the type of the problem
            solver: solve problem agent; TODO: add Math-specific tools
            answer_checker: check answer agent use different methods or substitute the answer
            process_checker: check the correctness and logic of the solution problem
            feedback_agent: give student feedback
        """

        recognizer = SequentialAgent(
            name="ProblemProcessing",
            sub_agents=[image_recognizer, problem_recognizer],
        )

        checker = LoopAgent(
            name="ProblemSolver",
            sub_agents=[answer_checker, process_checker],
            max_iterations=1
        )

        sub_agents_list = [
            recognizer, solver, checker, feedback_agent
        ]

        super().__init__(
            name=name,
            image_recognizer=image_recognizer,
            problem_recognizer=problem_recognizer,
            recognizer=recognizer,

            solver=solver,

            answer_checker=answer_checker,
            process_checker=process_checker,
            checker=checker,

            feedback_agent=feedback_agent,

            sub_agents=sub_agents_list,
        )

    @override
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        async for event in self.recognizer.run_async(ctx):
            print(f"[{self.name}] Recognized event: {event.model_dump_json(indent=2, exclude_none=True)}")
            yield event

        if "formatted_question" not in ctx.session.state or not ctx.session.state["formatted_question"]:
            print(f"[{self.name}] Failed to recognize the problem. Aborting workflow.")
            return


        async for event in self.solver.run_async(ctx):
            yield event

        if "current_solution" not in ctx.session.state or not ctx.session.state["current_solution"]:
            return

        async for event in self.checker.run_async(ctx):
            yield event

        # Feedback Step
        async for event in self.feedback_agent.run_async(ctx):
            yield event

        print(f"[{self.name}] Workflow finished.")
