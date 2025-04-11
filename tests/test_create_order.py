import allure
import pytest
import requests

import scooter_api
import urls


class TestCreateOrder:
    @allure.title("Успешное создание заказа с разным цветом самоката")
    @allure.description("Проверка успешного заказа с цветами Black, Grey, Black and Grey, цвет не указан. Проверка кода ответа и наличия в ответе номера заказа")
    @pytest.mark.parametrize("color", [
        pytest.param(["BLACK"]),
        pytest.param(["GREY"]),
        pytest.param(["BLACK", "GREY"]),
        pytest.param([])
    ])
    def test_choose_the_color_in_success_order(self, color):
        color_body = {"color": color}
        create_order_with_color = scooter_api.create_order(color_body)
        assert create_order_with_color.status_code == 201
        assert create_order_with_color.json()["track"] != None


class TestOrderList:
    @allure.title("Проверка получения списка заказов в тело ответа")
    @allure.description("Проверка получения списка заказов в тело ответа. Проверка кода ответа и наличия непустого массива с заказами")
    def test_return_list_order(self):
        order_list = requests.get(urls.BASE_URL + urls.ORDER_LIST_ENDPOINT)
        assert order_list.status_code == 200
        assert order_list.json()["orders"] != None
