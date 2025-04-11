
import pytest
import requests
import helpers
import scooter_api
import urls


# Создание шаблонного курьера
@pytest.fixture(scope='function')
def default_courier():
    body = helpers.new_courier_login_password()

# создаём курьера
    create_response = scooter_api.create_courier(body)

# логинимся, чтобы получить id
    login_data = {
        "login": body["login"],
        "password": body["password"]
    }
    login_response = requests.post(urls.BASE_URL + urls.LOGIN_COURIER_ENDPOINT, json=login_data)
    courier_id = login_response.json().get("id")

# возвращаем тело курьера и id
    yield {
        "response": create_response,
        "body": body,
        "id": courier_id
    }
# удаление
    if courier_id:
        requests.delete(urls.BASE_URL + urls.DELETE_COURIER_ENDPOINT + str(courier_id))