import pytest
import allure

from constants import BASE_URL, TRAINER_ID
from helpers.api_client import send_request
from helpers.pokemon_helpers import (
    knockout_all_trainers_pokemons,
    create_pokemon,
)


class TestPokemons:

    @allure.title("Изменение имени покемона")
    @pytest.mark.positive
    def test_change_pokemons_name(self, api_session):

        with allure.step("Нокаутировать всех покемонов тренера"):
            knockout_all_trainers_pokemons(api_session)

        with allure.step("Создать нового покемона"):
            pokemon_id = create_pokemon(api_session)

        new_name = "Bobik"

        with allure.step("Изменить имя покемона через PATCH /pokemons"):
            response = send_request(
                "PATCH",
                BASE_URL + "/pokemons",
                headers=api_session.headers,
                json={
                    "pokemon_id": pokemon_id,
                    "name": new_name,
                    "photo_id": 1
                }
            )

            assert response.status_code == 200

        with allure.step("Получить список покемонов тренера"):
            response = send_request(
                "GET",
                BASE_URL + "/pokemons",
                headers=api_session.headers,
                params={
                    "trainer_id": TRAINER_ID
                }
            )

            assert response.status_code == 200

        with allure.step("Проверить, что имя покемона изменилось"):
            pokemons = response.json()["data"]

            updated_pokemon = None

            for pokemon in pokemons:
                if pokemon["id"] == pokemon_id:
                    updated_pokemon = pokemon

            assert updated_pokemon is not None
            assert updated_pokemon["name"] == new_name
