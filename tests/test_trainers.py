import pytest

from constants import BASE_URL


class TestTrainers:

    @pytest.mark.positive
    def test_get_trainers_by_city(self, api_session):
        city = "Москва"

        response = api_session.get(
            BASE_URL + "/trainers",
            params={"city": city}
        )

        assert response.status_code == 200

        trainers = response.json()["data"]

        for trainer in trainers:
            assert trainer["city"] == city

    @pytest.mark.positive
    def test_get_trainer_by_id(self, api_session):
        trainer_id = 64645

        response = api_session.get(
            BASE_URL + "/trainers",
            params={"trainer_id": trainer_id}
        )

        assert response.status_code == 200

        body = response.json()

        assert body["status"] == "success"
        assert int(body["data"][0]["id"]) == trainer_id

    @pytest.mark.positive
    def test_get_trainers_sorted_by_level_desc(self, api_session):
        city = "Москва"

        response = api_session.get(
            BASE_URL + "/trainers",
            params={
                "city": city,
                "sort": "desc_level"
            }
        )

        assert response.status_code == 200

        trainers = response.json()["data"]

        levels = [int(trainer["level"]) for trainer in trainers]

        assert levels == sorted(levels, reverse=True)

    @pytest.mark.negative
    @pytest.mark.skip(reason="Пример пропуска теста по заданию")
    def test_get_missing_trainer(self, api_session):
        response = api_session.get(
            BASE_URL + "/trainers",
            params={"trainer_id": 1}
        )

        assert response.status_code == 200

        body = response.json()

        assert body["status"] == "error"