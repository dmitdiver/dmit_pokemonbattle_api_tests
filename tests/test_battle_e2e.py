import allure
import pytest

from constants import BASE_URL, TRAINER_ID
from helpers.pokemon_helpers import (
    knockout_all_trainers_pokemons,
    create_pokemon,
    add_pokemon_to_pokeball,
)


class TestBattleE2E:

    @allure.title("E2E: битва покемонов и проверка состояния после боя")
    @pytest.mark.positive
    def test_pokemon_battle_result_state(self, api_session):
        with allure.step("Подготовить покемонов тренера: отправить всех в нокаут"):
            knockout_all_trainers_pokemons(api_session)

        with allure.step("Создать своего покемона и добавить его в покебол"):
            my_pokemon_id = create_pokemon(api_session)
            add_pokemon_to_pokeball(api_session, my_pokemon_id)

        with allure.step("Найти чужого покемона в покеболе"):
            response = api_session.get(
                BASE_URL + "/pokemons",
                params={"in_pokeball": 1}
            )

            assert response.status_code == 200

            pokemons = response.json()["data"]

            enemy_pokemons = [
                pokemon for pokemon in pokemons
                if str(pokemon["trainer_id"]) != str(TRAINER_ID)
            ]

            assert len(enemy_pokemons) > 0

            enemy_pokemon_id = enemy_pokemons[0]["id"]

        with allure.step("Провести битву"):
            response = api_session.post(
                BASE_URL + "/battle",
                json={
                    "attacking_pokemon": my_pokemon_id,
                    "defending_pokemon": enemy_pokemon_id
                }
            )

            assert response.status_code == 200

            battle_body = response.json()
            assert battle_body["message"] == "Битва проведена"
            result = battle_body["result"]

        with allure.step("Получить своего покемона после битвы"):
            response = api_session.get(
                BASE_URL + "/pokemons",
                params={"pokemon_id": my_pokemon_id}
            )

            assert response.status_code == 200

            my_pokemon = response.json()["data"][0]

        with allure.step("Проверить состояние своего покемона после битвы"):
            if result == "Твой покемон проиграл":
                assert int(my_pokemon["status"]) == 0
                assert int(my_pokemon["in_pokeball"]) == 0

            elif result == "Твой покемон победил":
                assert int(my_pokemon["status"]) == 1
                assert int(my_pokemon["in_pokeball"]) == 1

            else:
                raise AssertionError(f"Неизвестный результат битвы: {result}")