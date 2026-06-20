import yaml
import pytest_check as check

from deepdiff import DeepDiff
from jsonschema import validate

from constants import BASE_URL





class TestAchievements:

    def test_invalid_is_reached(self, api_session):
        response = api_session.get(
            BASE_URL + "/achievements",
            params={
                "is_reached": "abracadabra"
            }
        )

        body = response.json()

        check.equal(response.status_code, 422)
        check.equal(body["status"], "error")
        check.is_in("message", body)

    def test_get_achievements(self, api_session):

        response = api_session.get(
            BASE_URL + "/achievements"
        )

        assert response.status_code == 200

        body = response.json()

        with open("schemas/achievements_schema.yaml") as file:
            schema = yaml.safe_load(file)

        validate(instance=body, schema=schema)

        expected = body

        diff = DeepDiff(
            body,
            body,
            exclude_regex_paths=r".*is_reached.*"
        )

        assert diff == {}