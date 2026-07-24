import allure

from requests import Session

from constants import BASE_URL, TRAINER_ID
from helpers.api_client import send_request


def knockout_all_trainers_pokemons(api_session: Session) -> None:

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

    body = response.json()

    if "data" not in body:
        return

    for pokemon in body["data"]:
        if pokemon["status"] == 1:
            with allure.step(f"Нокаутировать покемона с ID {pokemon['id']}"):
                response = send_request(
                    "POST",
                    BASE_URL + "/pokemons/knockout",
                    headers=api_session.headers,
                    json={
                        "pokemon_id": pokemon["id"]
                    }
                )

                assert response.status_code == 200


def create_pokemon(api_session: Session) -> str:

    with allure.step("Создать нового покемона"):
        response = send_request(
            "POST",
            BASE_URL + "/pokemons",
            headers=api_session.headers,
            json={
                "name": "Ohlatop",
                "photo_id": 1
            }
        )

        assert response.status_code == 201

    body = response.json()

    return body["id"]

def add_pokemon_to_pokeball(api_session: Session, pokemon_id: str) -> None:

    with allure.step(f"Добавить покемона с ID {pokemon_id} в покебол"):
        response = send_request(
            "POST",
            BASE_URL + "/trainers/add_pokeball",
            headers=api_session.headers,
            json={
                "pokemon_id": pokemon_id
            }
        )

        assert response.status_code == 200