from http import HTTPStatus

import allure
import pytest

from constants import LAVKA_URL


def cancel_premium(api_session):
    response = api_session.post(LAVKA_URL + "/cancel_premium")

    assert response.status_code in [HTTPStatus.OK, HTTPStatus.BAD_REQUEST]

    body = response.json()

    assert body["message"] in [
        "Пользователь потерял премиум",
        "Подписка уже отменена",
    ]


class TestPremiumE2E:

    @allure.title("E2E: успешная покупка Premium")
    @pytest.mark.api
    @pytest.mark.positive
    def test_buy_premium_successfully(self, api_session):
        with allure.step(
                "Подготовить состояние: отменить Premium, если он уже активен"
        ):
            cancel_premium(api_session)

        with allure.step("Купить Pokemon Premium"):
            response = api_session.post(
                LAVKA_URL + "/payments",
                json={
                    "order_type": "premium",
                    "details": {
                        "card_number": "5555555544444442",
                        "secure_code": "56456",
                        "card_name": "IVAN IVANOV",
                        "card_cvv": "125",
                        "card_actual": "12/34",
                        "avatar_id": 1,
                        "days": 30
                    }
                }
            )

            assert response.status_code == HTTPStatus.OK

            body = response.json()

            assert body["message"] == "Транзакция успешна"
            assert body["days"] == 30

        with allure.step("Вернуть систему в исходное состояние: отменить Premium"):
            cancel_premium(api_session)

    @allure.title("E2E: покупка Premium не проходит при некорректных платёжных данных")
    @pytest.mark.api
    @pytest.mark.negative
    @pytest.mark.parametrize(
        "field,value",
        [
            ("card_number", "4242424242424242"),
            ("secure_code", ""),
            ("card_name", ""),
            ("card_cvv", "000"),
            ("card_actual", "01/20"),
            ("days", 0),
        ]
    )
    def test_buy_premium_payment_failed(self, api_session, field, value):
        payload = {
            "order_type": "premium",
            "details": {
                "card_number": "2202202000000000",
                "secure_code": "123456",
                "card_name": "IVAN IVANOV",
                "card_cvv": "125",
                "card_actual": "12/34",
                "avatar_id": 1,
                "days": 30
            }
        }

        payload["details"][field] = value

        with allure.step(f"Попытаться купить Premium с некорректным полем {field}"):
            response = api_session.post(
                LAVKA_URL + "/payments",
                json=payload
            )

            assert response.status_code != HTTPStatus.OK

            body = response.json()

            assert body["status"] == "error"
