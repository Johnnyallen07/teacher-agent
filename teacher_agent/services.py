import asyncio

from google.adk.sessions import InMemorySessionService

from teacher_agent.config import APP_NAME, USER_ID, SESSION_ID

session_service = InMemorySessionService()
initial_state = {}
session = asyncio.run(session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state
))