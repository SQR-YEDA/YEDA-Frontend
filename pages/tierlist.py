import streamlit as st
from menu import menu_with_redirect
from streamlit_modal import Modal
import requests
from constants import API

menu_with_redirect()

if(st.button("Logout")):
    st.session_state.auth = False
    st.switch_page("app.py")

st.title("Tierlist")

def category_widget(name, elements):
    category = st.empty()

    def remove_category():
        category.empty()
        del st.session_state["categories"][name]

    with category:
        category_name, multiselect = st.columns([15, 40])
        with category_name:
            col1, col2 = st.columns([10, 5])
            col1.write(name)
            col2.button("x", key=f"category_widget_button_delete_{name}", on_click=remove_category)

        with multiselect:
            st.multiselect(default=elements,
                           options=list(map(lambda x: x["name"], st.session_state["products"])),
                           label="Products", label_visibility="collapsed",
                           key=f"category_widget_multiselect_{name}")
    return category


if "products" not in st.session_state:
    st.session_state["products"] = [
            {
                "name": "product1",
                "calories": 10
            }]

if "categories" not in st.session_state:
    st.session_state["categories"] = {f"Category {i}": {"multiselect": []} for i in range(5)}

# Запрашиваем тир лист
head = {'Authorization': 'Bearer {}'.format(st.session_state["init"]["access_token"])}
tierlist = requests.get(f"{API}/tier-list", headers=head).json()

print("DATA", tierlist)

# Header layout
head1, head2, head3 = st.columns([10, 3, 3])

head1.markdown(f"# {tierlist['tier_list']['name']}")

with head2:
    st.write("")  # genius way to center the button
    st.write("")
    add_product_modal_open = st.button("Add product")


with head3:
    st.write("")
    st.write("")
    add_category_modal_open = st.button("Add category")

# Categories
category_widgets = [category_widget(name, props) for name, props in st.session_state["categories"].items()]

# Add Product Modal
add_product_modal = Modal("Add product", key="add_product_modal")


def add_product(product):
    st.session_state["products"].append(product)
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
    st.session_state["categories"][name] = {"multiselect": []}
    add_category_modal.close()


if add_category_modal_open:
    add_category_modal.open()

if add_category_modal.is_open():
    with add_category_modal.container():
        category_name = st.text_input(label="Name", placeholder="Enter your category name")
        _, col2 = st.columns([10, 1])
        with col2:
            st.button("Add", on_click=lambda: add_category(category_name))