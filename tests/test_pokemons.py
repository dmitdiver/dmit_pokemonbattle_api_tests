import time

import pytest

from constants import BASE_URL, TRAINER_ID
from helpers.pokemon_helpers import (
    knockout_all_trainers_pokemons,
    create_pokemon,
)


class TestPokemons:

    @pytest.mark.positive
    def test_change_pokemons_name(self, api_session):
        knockout_all_trainers_pokemons(api_session)

        pokemon_id = create_pokemon(api_session)

        new_name = "Bobik"

        response = api_session.patch(
            BASE_URL + "/pokemons",
            json={
                "pokemon_id": pokemon_id,
                "name": new_name,
                "photo_id": 1
            }
        )

        assert response.status_code == 200

        response = api_session.get(
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
