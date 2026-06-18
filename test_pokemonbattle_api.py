import requests
from requests import Session


BASE_URL = "https://api.pokemonbattle.ru/v2"
TRAINER_ID = 64605
TOKEN = "95adee986cb298a0b6c69a78706c0fbe"


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

    response = api_session.get(
        BASE_URL + "/pokemons",
        params={"trainer_id": TRAINER_ID}
    )

    assert response.status_code == 200

    body = response.json()

    for pokemon in body["data"]:
        assert pokemon["status"] == 0


def create_pokemon(api_session: Session) -> str:
    response = api_session.post(
        BASE_URL + "/pokemons",
        json={
            "name": "Ohlatop",
            "photo_id": 1
        }
    )

    assert response.status_code == 201 or response.status_code == 200

    body = response.json()

    return body["id"]


class TestPokemonBattleApi:

    @classmethod
    def setup_class(cls):
        cls.session = requests.Session()
        cls.session.headers.update({
            "trainer_token": TOKEN
        })

    def test_change_pokemons_name(self):
        knockout_all_trainers_pokemons(self.session)

        pokemon_id = create_pokemon(self.session)

        new_name = "Pikachu"

        response = self.session.patch(
            BASE_URL + "/pokemons",
            json={
                "pokemon_id": pokemon_id,
                "name": new_name
            }
        )

        assert response.status_code == 200

        response = self.session.get(
            BASE_URL + "/pokemons",
            params={"trainer_id": TRAINER_ID}
        )

        assert response.status_code == 200

        pokemons = response.json()["data"]

        updated_pokemon = None

        for pokemon in pokemons:
            if pokemon["id"] == pokemon_id:
                updated_pokemon = pokemon

        assert updated_pokemon is not None
        assert updated_pokemon["name"] == new_name
