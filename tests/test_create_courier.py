import allure
import requests
import data
import helpers
import scooter_api
import urls


class TestCreateCourier:
    @allure.title("Проверка успешного создания курьера")
    @allure.description("Создание шаблонного курьера проверка статуса ответа и тело ответа")
    def test_create_successfully_courier(self):
        courier_data = {
            "login": "test_user_123",
            "password": "password123",
            "firstName": "Testtt"
        }
        with allure.step("Отправляем POST- запрос на создание курьера"):
            create_response = requests.post(urls.BASE_URL + urls.CREATE_COURIER_ENDPOINT, json=courier_data)

        with allure.step("Проверяем, что статус ответа - 201 Created"):
            assert create_response.status_code == 201, f"Ожидался статус 201, получен {create_response.status_code}"
        with allure.step("Проверяем, что в теле ответа есть ключ 'ok' со значением true"):
            response_json = create_response.json()
            assert create_response.json().get("ok") is True, f"Ответ сервера: {response_json}"

    @allure.title("Проверка на получение ошибки при попытке создать двух одинаковых курьеров")
    @allure.description("Создание двух одинаковых курьеров, проверка статус ответа и тело ответа")
    def test_create_duplicate_courier(self):
        body = helpers.new_courier_login_password()
        with allure.step("Создаем первого курьера"):
            create_response = requests.post(urls.BASE_URL + urls.CREATE_COURIER_ENDPOINT, json=body)
            assert create_response.status_code == 201, "Первый курьер не был создан"

        with allure.step("Пытаемся создать дублирующего курьера"):
            duplicate_response = requests.post(urls.BASE_URL + urls.CREATE_COURIER_ENDPOINT, json=body)
            assert duplicate_response.status_code == 409 and duplicate_response.json()["message"] == data.ErrorMessages.FAIL_NAME_ERROR

    @allure.title("Проверка на появление ошибки при создании курьера с пустым полем 'login'")
    @allure.description("Создание курьера с пустым полем 'login', проверка статуса ответа и тела ответа")
    def test_empty_login_create_courier(self):
        body_login = helpers.ChangeTestDataHelper.modify_create_courier_body("login", "")
        with allure.step("Отправляем запрос на создание курьера с пустым login"):
            empty_login_courier_request = scooter_api.create_courier(body_login)
        with allure.step("Проверяем, что ответ имеет статус 400 и сообщение об ошибке" ):
            assert empty_login_courier_request.status_code == 400 and empty_login_courier_request.json()["message"] == data.ErrorMessages.NOT_ENOUGH_DATA_ERROR

    @allure.title(" Проверка появления ошибки при создании курьера с пустым полем 'password'")
    @allure.description("Создание курьера с пустым полем 'password', проверка статуса ответа и тела ответа")
    def test_empty_password_create_courier(self):
        body_password = helpers.ChangeTestDataHelper.modify_create_courier_body("password", "")
        with allure.step("Отправляем запрос на создание курьера с пустым password"):
            empty_password_courier_request = scooter_api.create_courier(body_password)
        with allure.step("Проверяем, что ответ имеет статус 400 и сообщение об ошибке" ):
            assert empty_password_courier_request.status_code == 400 and empty_password_courier_request.json()["message"] == data.ErrorMessages.NOT_ENOUGH_DATA_ERROR

    @allure.title("Проверка появления ошибки при создании курьера с пустым полем 'firstname'")
    @allure.description("Создание курьера с пустым полем 'firstname', проверка статуса ответа и тела ответа")
    def test_empty_first_name_create_courier(self):
        body_first_name = helpers.ChangeTestDataHelper.modify_create_courier_body("firstname", "")
        with allure.step("Отправляем запрос на создание курьера с пустым firstname"):
            empty_first_name_courier_request = scooter_api.create_courier(body_first_name)
        with allure.step("Проверяем, что ответ имеет статус 400 и сообщение об ошибке" ):
            assert  empty_first_name_courier_request.status_code == 400 and empty_first_name_courier_request.json()["message"] == data.ErrorMessages.NOT_ENOUGH_DATA_ERROR





