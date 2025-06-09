from google.adk import Runner

from teacher_agent.config import APP_NAME
from teacher_agent.sub_agents.solve_agent.model import algebra_teacher_agent
from teacher_agent.services import session_service

runner = Runner(
    agent=algebra_teacher_agent, # Pass the custom orchestrator agent
    app_name=APP_NAME,
    session_service=session_service
)