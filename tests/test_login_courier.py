import allure
import requests

import data
import helpers
import urls


class TestLoginCourier:
    @allure.title("Проверка успешной авторизации курьера")
    @allure.description("Создание курьера и его авторизация, проверка статуса ответа и наличия id курьера в ответе")
    def test_success_login_courier(self, default_courier):
        body = default_courier["body"]

        login_data = {
            "login":body["login"],
            "password":body["password"]
        }
        courier_login = requests.post(urls.BASE_URL + urls.LOGIN_COURIER_ENDPOINT, json=login_data)
        assert courier_login.status_code == 200, f"Ожидаемый результат 200, вернулся {courier_login.status_code}"
        assert courier_login.json().get("id") is not None, "В ответе нет id курьера"

    @allure.title("Проверка появления ошибки при авторизации курьера с неверным полем login")
    @allure.description("Создание курьера и его авторизация с неверным полем логин и проверка статуса ответа с ошибкой и теста ошибки в ответе")
    def test_fail_with_wrong_login(self, default_courier):
        correct_body = default_courier["body"]
        wrong_login_body = correct_body.copy()
        wrong_login_body["login"] = "Courier"

        courier_login = requests.post(urls.BASE_URL + urls.LOGIN_COURIER_ENDPOINT, json=wrong_login_body)
        assert courier_login.status_code == 404
        assert courier_login.json()["message"] == data.ErrorMessages.ACCOUNT_NOT_FOUND_ERROR


    @allure.title("Проверка появления ошибки при авторизации курьера с неверным полем password")
    @allure.description("Создание курьера и его авторизация с неверным полем пароль и проверка статуса ответа с ошибкой и теста ошибки в ответе")
    def test_fail_with_wrong_password(self, default_courier):
        correct_body = default_courier["body"]
        wrong_password_body = correct_body.copy()
        wrong_password_body["password"] = "Password"

        courier_login = requests.post(urls.BASE_URL + urls.LOGIN_COURIER_ENDPOINT, json=wrong_password_body)
        assert courier_login.status_code ==404
        assert courier_login.json()["message"] == data.ErrorMessages.ACCOUNT_NOT_FOUND_ERROR

    @allure.title("Проверка появления ошибки при авторизации курьера с пустым полем login")
    @allure.description("Создание курьера и его авторизация с пустым полем логин и проверка статуса ответа с ошибкой и теста ошибки в ответе")
    def test_fail_with_empty_login(self,default_courier):
        correct_body = default_courier["body"]
        empty_login = correct_body.copy()
        empty_login["login"] = ""

        courier_login = requests.post(urls.BASE_URL + urls.LOGIN_COURIER_ENDPOINT, json=empty_login)
        assert courier_login.status_code == 400
        assert courier_login.json()["message"] == data.ErrorMessages.NOT_ENOUGH_LOGIN_DATA_ERROR

    @allure.title("Проверка появления ошибки при авторизации курьера с пустым полем password")
    @allure.description("Создание курьера и его авторизация с пустым полем пароля и проверка статуса ответа с ошибкой и теста ошибки в ответе")
    def test_fail_with_empty_password(self,default_courier):
        correct_body = default_courier["body"]
        empty_login = correct_body.copy()
        empty_login["password"] = ""

        courier_login = requests.post(urls.BASE_URL + urls.LOGIN_COURIER_ENDPOINT, json=empty_login)
        assert courier_login.status_code == 400
        assert courier_login.json()["message"] == data.ErrorMessages.NOT_ENOUGH_LOGIN_DATA_ERROR

    @allure.title("Проверка, что нельзя авторизоваться с несуществующим курьером")
    @allure.description("Авторизация несуществующего курьера проверка статуса ответа и текст ошибки")
    def test_fail_fake_courier_login(self):
        body = helpers.new_courier_login_password()
        courier_login = requests.post(urls.BASE_URL + urls.LOGIN_COURIER_ENDPOINT, json=body)
        assert courier_login.status_code == 404
        assert courier_login.json()["message"] == data.ErrorMessages.ACCOUNT_NOT_FOUND_ERROR