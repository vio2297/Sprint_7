import allure
import pytest
import requests

import data
import helpers
import urls


class TestLoginCourier:
    @allure.title("Проверка успешной авторизации курьера")
    @allure.description("Создание курьера и его авторизация, проверка статуса ответа и наличия id курьера в ответе")
    def test_success_login_courier(self, default_courier):
        body = default_courier["body"]

        with allure.step("Формируем данные для авторизации"):
            login_data = {
                "login": body["login"],
                "password": body["password"]
            }

        with allure.step("Отправляем запрос на авторизацию"):
            courier_login = requests.post(urls.BASE_URL + urls.LOGIN_COURIER_ENDPOINT, json=login_data)

        with allure.step("Проверяем, что статус ответа 200"):
            assert courier_login.status_code == 200, f"Ожидаемый результат 200, вернулся {courier_login.status_code}"

        with allure.step("Проверяем, что в ответе есть id курьера"):
            assert courier_login.json().get("id") is not None, "В ответе нет id курьера"


@pytest.mark.parametrize(
    "title, modify, expected_status, expected_error",
    [
        ("Неверный логин",
         lambda b: {**b, "login": "Courier"},
         404,
         data.ErrorMessages.ACCOUNT_NOT_FOUND_ERROR
         ),
        ("Неверный пароль",
         lambda b: {**b, "password": "Password"},
         404,
         data.ErrorMessages.ACCOUNT_NOT_FOUND_ERROR
         ),
        ("Пустой логин",
         lambda b: {**b, "login": ""},
         400,
         data.ErrorMessages.NOT_ENOUGH_LOGIN_DATA_ERROR
         ),
        ("Пустой пароль",
         lambda b: {**b, "password": ""},
         400,
         data.ErrorMessages.NOT_ENOUGH_LOGIN_DATA_ERROR
         ),
    ],
    ids=["wrong_login", "wrong_password", "empty_login", "empty_password"]
)
@allure.title("Проверка появления ошибки при авторизации курьера с неверным полем login, password")
@allure.description("Создание курьера и его авторизация с неверным полем логин,пароль и проверка статуса ответа с ошибкой и текста ошибки в ответе")
def test_negative_login_scenario(title, modify, expected_status, expected_error, default_courier):
    with allure.step(f"Подготовка данных: {title}"):
        base_body = default_courier["body"]
        test_body = modify(base_body)

    with allure.step("Отправка запроса на авторизацию"):
        response = requests.post(urls.BASE_URL + urls.LOGIN_COURIER_ENDPOINT, json=test_body)

    with allure.step(f"Проверка, что статус ответа равен {expected_status}"):
        assert response.status_code == expected_status, f"Ожидался статус {expected_status}, получен {response.status_code}"

    with allure.step(f"Проверка текста ошибки: {expected_error}"):
        assert response.json()["message"] == expected_error, f"Ожидалась ошибка '{expected_error}', получена '{response.json().get('message')}'"


@allure.title("Проверка, что нельзя авторизоваться с несуществующим курьером")
@allure.description("Авторизация несуществующего курьера. Проверка статуса ответа и текста ошибки.")
def test_fail_fake_courier_login():
    with allure.step("Генерация случайных логина и пароля для несуществующего курьера"):
        body = helpers.new_courier_login_password()

    with allure.step("Отправка запроса на авторизацию"):
        response = requests.post(urls.BASE_URL + urls.LOGIN_COURIER_ENDPOINT, json=body)

    with allure.step("Проверка, что статус ответа 404"):
        assert response.status_code == 404, f"Ожидался статус 404, получен {response.status_code}"

    with allure.step("Проверка текста ошибки: аккаунт не найден"):
        assert response.json()["message"] == data.ErrorMessages.ACCOUNT_NOT_FOUND_ERROR, (
            f"Ожидалась ошибка '{data.ErrorMessages.ACCOUNT_NOT_FOUND_ERROR}', "
            f"получена '{response.json().get('message')}'"
        )
