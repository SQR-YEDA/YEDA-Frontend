from streamlit.testing.v1 import AppTest
from unittest.mock import patch
import pytest


def mocked_requests_get_product(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    mock_product = [{'name': 'test1', 'id': 1, 'calories': 100}, {'name': 'test2', 'id': 2, 'calories': 100}]
    product_to_add = {'name': 'add_test', 'id': 3, 'calories': 100}
    new_products = mock_product.copy()
    new_products.append(product_to_add)

    return MockResponse({'elements': new_products}, 200)


@pytest.fixture
def at():
    mock_product = [{'name': 'test1', 'id': 1, 'calories': 100}, {'name': 'test2', 'id': 2, 'calories': 100}]
    mock_categories = [{'name': 'c1', 'elements': mock_product}]
    at = AppTest.from_file("pages/tierlist.py")
    at.session_state["authentication_status"] = True
    at.session_state["access_token"] = ""
    at.session_state["tier_list_name"] = "Tierlist name"
    at.session_state["products"] = {product['name']: {'id': product['id'], 'calories': product['calories']}
                                    for product in mock_product}
    at.session_state["categories"] = {category['name']: category['elements']
                                      for category in mock_categories}

    return at


def test_login(at):
    at = AppTest.from_file("app.py").run()

    at.text_input("username_input").input("slry").run()
    at.text_input("password_input").input("12345678").run()

    assert at.title[0].value == "Login"
    assert at.text_input("username_input").value == 'slry'
    assert at.text_input("password_input").value == '12345678'
    assert at.button[0].label == 'Login'

    at.button[0].click()


@patch("streamlit.sidebar.page_link")
@patch("requests.post")
@patch("requests.get", side_effect=mocked_requests_get_product)
def test_add_product(page_link, requests_post, requests_get, at):
    product_to_add = {'name': 'add_test', 'id': 3, 'calories': 100}

    at.run()

    assert at.title[0].value == "Tierlist"
    assert at.markdown[0].value == "# Tierlist name"

    at.button("add_product_button").click().run()

    at.text_input("product_name_input").input(product_to_add["name"]).run()
    at.number_input("product_calories_input").set_value(product_to_add['calories']).run()
    at.button("add_product_in_modal_button").click().run()

    assert at.session_state["products"][product_to_add['name']]['calories'] == product_to_add['calories']


@patch("streamlit.sidebar.page_link")
@patch("requests.post")
@patch("requests.put")
def test_add_category(page_link, r_post, r_put, at):
    at.run()

    assert at.title[0].value == "Tierlist"
    assert at.markdown[0].value == "# Tierlist name"

    at.button("add_category_button").click().run()

    at.text_input("category_name_input").input('c2').run()
    at.button("add_category_in_modal_button").click().run()

    assert 'c2' in at.session_state['categories']
    assert at.session_state["categories"]['c2'] == []


@patch("streamlit.sidebar.page_link")
@patch("requests.post")
@patch("requests.put")
def test_remove_category(page_link, r_post, r_put, at):
    at.run()
    at.button('category_widget_button_delete_c1').click().run()

    assert at.session_state['categories'] == {}
