import os
import pytest
from wolframalpha import Client
from dotenv import load_dotenv
load_dotenv()


@pytest.fixture(scope="session")
def client():
    app_id = os.getenv("WOLFRAMALPHA_APPID")
    if not app_id:
        pytest.skip("WOLFRAMALPHA_APPID environment variable not set")
    # Instantiate the Wolfram|Alpha client with your App ID
    return Client(app_id)  # :contentReference[oaicite:0]{index=0}
