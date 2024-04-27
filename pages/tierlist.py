import streamlit as st
from menu import menu_with_redirect
from streamlit_modal import Modal
import requests
from constants import API

menu_with_redirect()

if (st.button("Logout")):
    st.session_state.auth = False
    st.switch_page("app.py")

st.title("Tierlist")


def category_widget(name, elements):
    category = st.empty()

    def remove_category():
        category.empty()
        del st.session_state["categories"][name]

        head = {'Authorization': 'Bearer {}'.format(st.session_state["access_token"])}
        categories = list(map(
            lambda x: {"name": x[0], "element_ids": list(map(lambda y: y['id'], x[1]))},
            st.session_state["categories"].items()))
        requests.put(f"{API}/tier-list",
                     json={
                         "update_tier_list": {
                            "name": st.session_state["tier_list_name"],
                            "categories": categories
                         }}, headers=head)

    def on_change(name):
        selected_product_names = st.session_state[f"category_widget_multiselect_{name}"]
        selected_products = []

        for prod_name in selected_product_names:
            prod = st.session_state["products"][prod_name]
            selected_products.append({"name": prod_name, "id": prod['id'], "calories": prod['calories']})

        st.session_state['categories'][name] = selected_products

        head = {'Authorization': 'Bearer {}'.format(st.session_state["access_token"])}
        categories = list(map(
            lambda x: {"name": x[0], "element_ids": list(map(lambda y: y['id'], x[1]))},
            st.session_state["categories"].items()))
        res = requests.put(f"{API}/tier-list", json={
                         "update_tier_list": {
                            "name": st.session_state["tier_list_name"],
                            "categories": categories
                         }}, headers=head)
        print(res.json())

    with category:
        category_name, multiselect = st.columns([15, 40])
        with category_name:
            col1, col2 = st.columns([10, 5])
            col1.write(name)
            col2.button("x",
                        key=f"category_widget_button_delete_{name}",
                        on_click=remove_category)

        with multiselect:
            st.multiselect(default=list(map(lambda x: x["name"], elements)), on_change=lambda: on_change(name),
                           options=st.session_state["products"].keys(),
                           label="Products", label_visibility="collapsed",
                           key=f"category_widget_multiselect_{name}")
    return category


# Запрашиваем тир лист
if 'init' in st.session_state:
    st.session_state['access_token'] = st.session_state["init"]["access_token"]
    head = {'Authorization': 'Bearer {}'.format(st.session_state["access_token"])}
    tierlist = requests.get(f"{API}/tier-list", headers=head).json()

    elements = requests.get(f"{API}/elements", headers=head).json()

    st.session_state["tier_list_name"] = tierlist['tier_list']['name']
    st.session_state["products"] = {product['name']: {'id': product['id'], 'calories': product['calories']}
                                    for product in elements['elements']}

    st.session_state["categories"] = {category['name']: category['elements']
                                      for category in tierlist['tier_list']['categories']}


# Header layout
head1, head2, head3 = st.columns([10, 3, 3])

head1.markdown(f"# {st.session_state['tier_list_name']}")

with head2:
    st.write("")  # genius way to center the button
    st.write("")
    add_product_modal_open = st.button("Add product")


with head3:
    st.write("")
    st.write("")
    add_category_modal_open = st.button("Add category")

# Categories
category_widgets = [category_widget(name, elements) for name, elements in st.session_state['categories'].items()]

# Add Product Modal
add_product_modal = Modal("Add product", key="add_product_modal")


def add_product(product):
    # Post new product
    head = {'Authorization': 'Bearer {}'.format(st.session_state["access_token"])}
    requests.post(f"{API}/elements", json=product, headers=head)
    new_products = requests.get(f"{API}/elements", headers=head)
    new_products = new_products.json()

    # Update products to get id for new product
    st.session_state["products"] = {product['name']: {'id': product['id'], 'calories': product['calories']}
                                    for product in new_products['elements']}

    add_product_modal.close()


if add_product_modal_open:
    add_product_modal.open()

if add_product_modal.is_open():
    with add_product_modal.container():
        product_name = st.text_input(label="Name", placeholder="Enter your product name")
        product_calories = st.number_input(label="Calories", step=1)
        _, col2 = st.columns([10, 1])
        with col2:
            st.button("Add", on_click=lambda: add_product({"name": product_name, "calories": product_calories}))

# Add Category Modal
add_category_modal = Modal("Add product", key="add_category_modal")


def add_category(name):
    head = {'Authorization': 'Bearer {}'.format(st.session_state["access_token"])}
    st.session_state["categories"][name] = []
    categories = list(map(lambda x: {"name": x[0], "element_ids": x[1]}, st.session_state["categories"].items()))
    res = requests.put(f"{API}/tier-list", json={
                     "update_tier_list": {
                        "name": st.session_state["tier_list_name"],
                        "categories": categories
                     }}, headers=head)
    print(res.json())
    add_category_modal.close()


if add_category_modal_open:
    add_category_modal.open()

if add_category_modal.is_open():
    with add_category_modal.container():
        category_name = st.text_input(label="Name", placeholder="Enter your category name")
        _, col2 = st.columns([10, 1])
        with col2:
            st.button("Add", on_click=lambda: add_category(category_name))
