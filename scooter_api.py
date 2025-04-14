import allure
import requests

import urls


# Создание курьера в сервисе "Самокат"
def create_courier(body):
    return requests.post(urls.BASE_URL + urls.CREATE_COURIER_ENDPOINT, json=body)

@allure.step("Создание заказа в сервисе 'Самокат'")
def create_order(order_body):
    return requests.post(urls.BASE_URL + urls.CREATE_ORDER_ENDPOINT, json=order_body)