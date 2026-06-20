from requests import Session

from constants import BASE_URL, TRAINER_ID


def knockout_all_trainers_pokemons(api_session: Session) -> None:
    response = api_session.get(
        BASE_URL + "/pokemons",
        params={"trainer_id": TRAINER_ID}
    )

    assert response.status_code == 200

    body = response.json()

    if "data" not in body:
        return

    for pokemon in body["data"]:
        if pokemon["status"] == 1:
            response = api_session.post(
                BASE_URL + "/pokemons/knockout",
                json={"pokemon_id": pokemon["id"]}
            )

            assert response.status_code == 200


def create_pokemon(api_session: Session) -> str:
    response = api_session.post(
        BASE_URL + "/pokemons",
        json={
            "name": "Ohlatop",
            "photo_id": 1
        }
    )

    assert response.status_code == 201

    body = response.json()

    return body["id"]