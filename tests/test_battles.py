import yaml
from jsonschema import validate
from constants import BASE_URL


class TestBattles:

    def test_get_battles(self, api_session):

        response = api_session.get(
            BASE_URL + "/battle"
        )

        assert response.status_code == 200

        body = response.json()

        with open("schemas/battle_schema.yaml") as file:
            schema = yaml.safe_load(file)

        validate(instance=body, schema=schema)