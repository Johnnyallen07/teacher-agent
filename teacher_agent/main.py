import asyncio
from google.genai import types

from teacher_agent.config import APP_NAME, USER_ID, SESSION_ID
from teacher_agent.services import session_service
from teacher_agent.runner import runner

def call_agent(user_input: str):
    current_session = asyncio.run(session_service.get_session(app_name=APP_NAME,
                                                              user_id=USER_ID,
                                                              session_id=SESSION_ID))
    if not current_session:
        print("Session not found!")
        return

    current_session.state["question"] = user_input


    content = types.Content(role='user', parts=[types.Part(text=f"Solve the question about: {user_input}")])
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    final_response = "No final response captured."
    for event in events:
        if event.is_final_response() and event.content and event.content.parts:
            final_response = event.content.parts[0].text

    print("\n--- Agent Interaction Result ---")
    print("Agent Final Response: ", final_response)

    final_session = asyncio.run(session_service.get_session(app_name=APP_NAME,
                                                            user_id=USER_ID,
                                                            session_id=SESSION_ID))
    print("Final Session State:")
    import json
    print(json.dumps(final_session.state, indent=2))
    print("-------------------------------\n")

if __name__ == '__main__':
    call_agent("Solve the integral of x^2 from 0 to 1")