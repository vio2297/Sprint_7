import allure
import requests
import data
import helpers
import scooter_api
import urls


class TestCreateCourier:
    @allure.title("Проверка успешного создания курьера")
    @allure.description("Создание шаблонного курьера проверка статуса ответа и тело ответа")
    def test_create_successfully_courier(self, default_courier):
        create_response = default_courier["response"]
        assert create_response.status_code == 201
        assert create_response.json().get("ok") is True

    @allure.title("Проверка на получение ошибки при попытке создать двух одинаковых курьеров")
    @allure.description("Создание двух одинаковых курьеров, проверка статус ответа и тело ответа")
    def test_create_duplicate_courier(self):
        body = helpers.new_courier_login_password()
        create_response = requests.post(urls.BASE_URL + urls.CREATE_COURIER_ENDPOINT, json=body)
        assert create_response.status_code == 201, "Первый курьер не был создан"

        duplicate_response = requests.post(urls.BASE_URL + urls.CREATE_COURIER_ENDPOINT, json=body)
        assert duplicate_response.status_code == 409 and duplicate_response.json()["message"] == data.ErrorMessages.FAIL_NAME_ERROR

    @allure.title("Проверка на появление ошибки при создании курьера с пустым полем 'login'")
    @allure.description("Создание курьера с пустым полем 'login', проверка статуса ответа и тела ответа")
    def test_empty_login_create_courier(self):
        body_login = helpers.ChangeTestDataHelper.modify_create_courier_body("login", "")
        empty_login_courier_request = scooter_api.create_courier((body_login))
        assert empty_login_courier_request.status_code == 400 and empty_login_courier_request.json()["message"] == data.ErrorMessages.NOT_ENOUGH_DATA_ERROR

    @allure.title(" Проверка появления ошибки при создании курьера с пустым полем 'password'")
    @allure.description("Создание курьера с пустым полем 'password', проверка статуса ответа и тела ответа")
    def test_empty_password_create_courier(self):
        body_password = helpers.ChangeTestDataHelper.modify_create_courier_body("password", "")
        empty_password_courier_request = scooter_api.create_courier((body_password))
        assert  empty_password_courier_request.status_code == 400 and empty_password_courier_request.json()["message"] == data.ErrorMessages.NOT_ENOUGH_DATA_ERROR

    @allure.title("Проверка появления ошибки при создании курьера с пустым полем 'firstname'")
    @allure.description("Создание курьера с пустым полем 'firstname', проверка статуса ответа и тела ответа")
    def test_empty_first_name_create_courier(self):
        body_first_name = helpers.ChangeTestDataHelper.modify_create_courier_body("firstname", "")
        empty_first_name_courier_request = scooter_api.create_courier((body_first_name))
        assert  empty_first_name_courier_request.status_code == 400 and empty_first_name_courier_request.json()["message"] == data.ErrorMessages.NOT_ENOUGH_DATA_ERROR





