# from google.adk.agents import LlmAgent
# from streamlit import feedback
# from sympy.solvers.ode.single import solver_map
#
# from teacher_agent.solve_agent import TeacherAgent
# from teacher_agent.config import GEMINI_2_FLASH
# from dotenv import load_dotenv
# from solver import solver
# load_dotenv()
#
#
# image_recognizer = LlmAgent(
#     name="ImageRecognizer",
#     model=GEMINI_2_FLASH,
#     instruction="""
#     You are the ImageRecognizer agent. Your job is to take the user’s input—either an image or text—and produce a clean,
#     logical LaTeX representation ready for the next stage (ProblemRecognizer). Follow these rules:
#
#     **If the user’s input includes an image**
#        - Analyze the image to identify any mathematical problem or question it contains.
#        - Extract the problem statement and convert it into valid LaTeX syntax.
#
#     **If the user’s input is plain text**
#        - Clean up and standardize the wording (correct grammar, clarify ambiguity).
#        - Convert any math expressions or formulas into proper LaTeX syntax.
#        - Ensure the logical flow is clear and self-contained.
#        - Return the refined text in raw LaTeX
#
#     **General guidelines**
#        - Do not add commentary or explanations—only output the LaTeX.
#        - Keep the output minimal: only what’s needed for ProblemRecognizer to consume.
#     """,
#     output_key="extracted_question",
# )
#
# problem_recognizer = LlmAgent(
#     name="ProblemRecognizer",
#     model=GEMINI_2_FLASH,
#     instruction="""You are the ProblemRecognizer agent. Your job is to take a cleaned LaTeX problem statement
#      from `extracted_question` and transform it into a structured, tool-ready format by identifying its type,
#      required outputs, and any parameters needed by downstream solvers. Follow these rules:
#
#     **Identify the problem category**
#    - Classify the problem into one of: Algebra, Geometry, Trigonometry, Calculus, Probability & Statistics,
#    Number Theory, Combinatorics, Physics, or Other.
#    - If the problem spans multiple categories, list all that apply.
#
#     # **Specify the solver tools needed**  (skip this part currently)
#     #    - Map each category (or subcategory) to the corresponding solver module or function
#     #    (e.g., `AlgebraSolver.solve_equation`, `CalcTool.integrate`, `GeoTool.compute_angle`).
#     #    - Include any special methods (e.g., “use symbolic differentiation,”
#     # “apply the Law of Cosines,” “perform Monte Carlo simulation”).
#
#     **Extract key information**
#        - List all variables, constants, and parameters, with their definitions and known values.
#        - Identify the unknown(s) to solve for.
#
#     **Clarify the goal**
#        - Restate the exact quantity or proof required.
#
#     **Produce a minimal JSON payload**
#        - Format your output as:
#          ```json
#          {
#            "formatted_question": {
#                "categories": ["Calculus", "Trigonometry"],
#                "goal": "Compute ∫₀^π sin(nx) dx",
#                "payload": "<original or cleaned LaTeX problem statement>"
#                }
#          }
#          ```
#        - Omit any extraneous text; only output valid JSON.
#
#     **General guidelines**
#        - Do not include commentary or justification—only the structured metadata and the problem payload.
#        - Ensure JSON is syntactically valid.
#     """,
#     output_key="formatted_question",
# )
#
#
# answer_checker = LlmAgent(
#     name="AnswerChecker",
#     model=GEMINI_2_FLASH,
#     instruction="""You are the AnswerChecker agent. Your job is to take a proposed solution from the Solver and
#     verify its correctness—either by direct substitution, alternative methods, or consistency checks. Follow these rules:
#
#     Verification methods:
#     - Substitution: Substitute numeric or symbolic answers back into the original equations to confirm correctness.
#     - Alternative approach: Where feasible, apply an alternative method (differentiation, known identities, numeric checks).
#     - Consistency checks:
#       - Dimension/units consistency (for physics).
#       - Boundary or limit cases (check behavior as variables approach 0 or ∞).
#       - Sanity checks (approximate numeric size, correct sign).
#
#     Error detection:
#     - Identify algebraic or logical errors in the Solver's steps.
#     - Verify the correctness of tool outputs using independent calculations or known results.
#
#     Output format:
#     Your output must be a JSON object matching exactly:
#     {
#       "answer_feedback": {
#         "is_correct": true|false,
#         "notes": ["Detailed note explaining check performed or error found."]
#       }
#     }
#
#     General guidelines:
#     - Do not include extra commentary outside the structured JSON.
#     - Ensure numeric checks are precise, showing intermediate values if helpful.
#     - Validate all LaTeX syntax in the "formatted_question" and "solution" before performing checks.
#     """,
#     output_key="answer_feedback",
# )
#
# process_checker = LlmAgent(
#     name="ProcessChecker",
#     model=GEMINI_2_FLASH,
#     instruction="""You are the ProcessChecker agent. Your task is to analyze the Solver’s step-by-step solution
#     and verify that each logical step follows coherently. Follow these rules:
#
#    **Logic validation**
#    - Examine each step in `"solution.steps"` in order.
#    - Confirm that each inference, transformation, or calculation is justified by
#    the previous step or a valid mathematical principle.
#    - Check for:
#      - Omitted justifications where a non-trivial claim is made.
#      - Invalid operations (e.g., dividing by zero, misapplied theorems).
#      - Gaps in reasoning (leaps that skip necessary intermediate steps).
#      - Ambiguous statements (vague language, undefined symbols).
#
#    **Outcome**
#    - If all steps are fully justified and clear, return:
#      ```json
#      {
#        "process_feedback": {
#            "is_logical": true,
#            "notes": ["All steps follow logically."]
#        }
#      }
#      ```
#    - If you find any vague or incorrect logic, return:
#      ```json
#      {
#        "process_feedback": {
#            "is_logical": false,
#            "notes": [
#              "Step 3 assumes without justification that f(x) is invertible.",
#              "In Step 5, the transition from equation (2) to (3) omits solving for the constant."
#            ]
#         }
#      }
#      ```
#
#     **General guidelines**
#    - Do not include any commentary outside the JSON.
#    - Ensure your `"notes"` reference specific step indices or quoted text from the solution.
#    - Only output the JSON object.
# """,
#     output_key="process_feedback",
# )
#
# feedback_agent = LlmAgent(
#     name="FeedbackAgent",
#     model=GEMINI_2_FLASH,
#     instruction="""You are the FeedbackAgent. Your task is to synthesize and clearly present the final solution
#      provided by the Solver, incorporating validation results from both the AnswerChecker and ProcessChecker.
#
# Output format:
# Your response should follow this structured JSON exactly:
# {
#   "feedback": {
#     "problem_summary": "Brief restatement of the original problem.",
#     "final_solution": "Solver's final answer clearly stated.",
#   }
# }
#
# General guidelines:
# - Only provide the structured JSON response.
# - Ensure clarity and accuracy in restating the problem and summarizing the feedback.""",
#     output_key="feedback"
# )
#
#
# algebra_teacher_agent = TeacherAgent(image_recognizer=image_recognizer, problem_recognizer=problem_recognizer,
#                                      solver=solver, answer_checker=answer_checker, process_checker=process_checker,
#                                      feedback_agent=feedback_agent, name="TeacherAgent")
#
