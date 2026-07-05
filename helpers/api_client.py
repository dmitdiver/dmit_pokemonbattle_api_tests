import json
import time
import allure
import requests


def attach_request_response(response):
    request = response.request

    allure.attach(
        request.url,
        name="Request URL",
        attachment_type=allure.attachment_type.TEXT
    )

    allure.attach(
        json.dumps(dict(request.headers), indent=4, ensure_ascii=False),
        name="Request headers",
        attachment_type=allure.attachment_type.JSON
    )

    if request.body:
        allure.attach(
            request.body.decode()
            if isinstance(request.body, bytes)
            else str(request.body),
            name="Request body",
            attachment_type=allure.attachment_type.TEXT
        )

    allure.attach(
        str(response.status_code),
        name="Response status code",
        attachment_type=allure.attachment_type.TEXT
    )

    allure.attach(
        json.dumps(dict(response.headers), indent=4, ensure_ascii=False),
        name="Response headers",
        attachment_type=allure.attachment_type.JSON
    )

    try:
        response_body = json.dumps(response.json(), indent=4, ensure_ascii=False)
    except Exception:
        response_body = response.text

    allure.attach(
        response_body,
        name="Response body",
        attachment_type=allure.attachment_type.JSON
    )


def send_request(method, url, retries=3, **kwargs):
    for attempt in range(retries):
        response = requests.request(method, url, **kwargs)
        attach_request_response(response)

        if response.status_code != 429:
            return response

        time.sleep(1)

    return response
