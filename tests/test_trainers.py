import pytest
import allure

from constants import BASE_URL
from helpers.api_client import send_request


class TestTrainers:

    @allure.title("Получение тренеров по городу")
    @pytest.mark.positive
    def test_get_trainers_by_city(self, api_session):

        city = "Москва"

        with allure.step(f"Получить список тренеров из города {city}"):
            response = send_request(
                "GET",
                BASE_URL + "/trainers",
                headers=api_session.headers,
                params={
                    "city": city
                }
            )

        with allure.step("Проверить код ответа"):
            assert response.status_code == 200

        with allure.step("Проверить, что все тренеры из указанного города"):
            trainers = response.json()["data"]

            for trainer in trainers:
                assert trainer["city"] == city

    @allure.title("Получение тренера по ID")
    @pytest.mark.positive
    def test_get_trainer_by_id(self, api_session):

        trainer_id = 64645

        with allure.step(f"Получить тренера с ID {trainer_id}"):
            response = send_request(
                "GET",
                BASE_URL + "/trainers",
                headers=api_session.headers,
                params={
                    "trainer_id": trainer_id
                }
            )

        with allure.step("Проверить код ответа"):
            assert response.status_code == 200

        with allure.step("Проверить содержимое ответа"):
            body = response.json()

            assert body["status"] == "success"
            assert int(body["data"][0]["id"]) == trainer_id

    @allure.title("Получение тренеров с сортировкой по уровню")
    @pytest.mark.positive
    def test_get_trainers_sorted_by_level_desc(self, api_session):

        city = "Москва"

        with allure.step("Получить список тренеров с сортировкой по уровню"):
            response = send_request(
                "GET",
                BASE_URL + "/trainers",
                headers=api_session.headers,
                params={
                    "city": city,
                    "sort": "desc_level"
                }
            )

        with allure.step("Проверить код ответа"):
            assert response.status_code == 200

        with allure.step("Проверить порядок сортировки"):
            trainers = response.json()["data"]

            levels = [
                int(trainer["level"])
                for trainer in trainers
            ]

            assert levels == sorted(
                levels,
                reverse=True
            )

    @allure.title("Получение несуществующего тренера")
    @pytest.mark.negative
    @pytest.mark.skip(reason="Пример пропуска теста по заданию")
    def test_get_missing_trainer(self, api_session):

        with allure.step("Отправить запрос на несуществующего тренера"):
            response = send_request(
                "GET",
                BASE_URL + "/trainers",
                headers=api_session.headers,
                params={
                    "trainer_id": 1
                }
            )

        with allure.step("Проверить ответ"):
            assert response.status_code == 200

            body = response.json()

            assert body["status"] == "error"
