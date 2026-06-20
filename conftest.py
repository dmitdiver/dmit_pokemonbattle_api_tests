import pytest
import requests

from constants import TOKEN


@pytest.fixture(scope="session")
def api_session():
    session = requests.Session()
    session.headers.update({
        "trainer_token": TOKEN
    })
    return session