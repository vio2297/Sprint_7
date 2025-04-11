class TestDataCreateOrder:
    CREATE_ORDER_BODY = {
    "firstName": "Naruto",
    "lastName": "Uchiha",
    "address": "Konoha, 142 apt.",
    "metroStation": 4,
    "phone": "+7 800 355 35 35",
    "rentTime": 5,
    "deliveryDate": "2020-06-06",
    "comment": "Saske, come back to Konoha",
    "color": [
        "BLACK"
    ]
}

class ErrorMessages:
    FAIL_NAME_ERROR = "Этот логин уже используется"
    NOT_ENOUGH_DATA_ERROR = "Недостаточно данных для создания учетной записи"
    NOT_ENOUGH_LOGIN_DATA_ERROR = "Недостаточно данных для входа"
    ACCOUNT_NOT_FOUND_ERROR = "Учетная запись не найдена"