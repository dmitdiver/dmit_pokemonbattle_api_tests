import allure
import pytest
import requests

from constants import TOKEN


@pytest.fixture(scope="session")
def api_session():
    with allure.step("Создать API-сессию с токеном тренера"):
        session = requests.Session()
        session.headers.update({
            "trainer_token": TOKEN,
            "Content-Type": "application/json"
        })

    yield session

    with allure.step("Закрыть API-сессию"):
        session.close()