import random
import string
import requests


def new_courier_login_password():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    login_pass = []

    # генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    return payload


class ChangeTestDataHelper:
    @staticmethod
    def modify_create_courier_body(key, value):
        body = new_courier_login_password().copy()
        body[key] = value
        return body