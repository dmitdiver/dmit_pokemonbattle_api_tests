import allure
import yaml

from jsonschema import validate

from constants import BASE_URL
from helpers.api_client import send_request


class TestBattles:

    @allure.title("Получение списка битв")
    def test_get_battles(self, api_session):

        with allure.step("Отправить GET запрос на /battle"):
            response = send_request(
                "GET",
                BASE_URL + "/battle",
                headers=api_session.headers
            )

        with allure.step("Проверить код ответа"):
            assert response.status_code == 200

        with allure.step("Получить тело ответа"):
            body = response.json()

        with allure.step("Проверить соответствие JSON Schema"):
            with open("schemas/battle_schema.yaml") as file:
                schema = yaml.safe_load(file)

            validate(
                instance=body,
                schema=schema
            )
