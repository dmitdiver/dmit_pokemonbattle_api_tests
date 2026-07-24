import allure
import yaml
import pytest_check as check

from deepdiff import DeepDiff
from jsonschema import validate

from constants import BASE_URL
from helpers.api_client import send_request


class TestAchievements:

    @allure.title("Негативная проверка GET /achievements с некорректным is_reached")
    def test_invalid_is_reached(self, api_session):
        with allure.step("Отправить GET /achievements с некорректным query-параметром is_reached"):
            response = send_request(
                "GET",
                BASE_URL + "/achievements",
                headers=api_session.headers,
                params={
                    "is_reached": "abracadabra"
                }
            )

        with allure.step("Проверить код ответа и поля ошибки"):
            body = response.json()

            check.equal(response.status_code, 422)
            check.equal(body["status"], "error")
            check.is_in("message", body)

    @allure.title("Получение списка достижений GET /achievements")
    def test_get_achievements(self, api_session):
        with allure.step("Отправить GET /achievements без параметров"):
            response = send_request(
                "GET",
                BASE_URL + "/achievements",
                headers=api_session.headers
            )

        with allure.step("Проверить код ответа"):
            assert response.status_code == 200

        with allure.step("Проверить тело ответа по JSON Schema"):
            body = response.json()

            with open("schemas/achievements_schema.yaml") as file:
                schema = yaml.safe_load(file)

            validate(instance=body, schema=schema)

        with allure.step("Проверить тело ответа через DeepDiff без поля is_reached"):
            diff = DeepDiff(
                body,
                body,
                exclude_regex_paths=r".*is_reached.*"
            )

            assert diff == {}
