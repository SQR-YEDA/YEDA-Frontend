import streamlit as st

def authenticated_menu():
    st.sidebar.page_link("app.py", label="Log in")
    st.sidebar.page_link("pages/tierlist.py", label="Tierlist")


def unauthenticated_menu():
    st.sidebar.page_link("app.py", label="Log in")
    
def menu():
    if not st.session_state["authentication_status"]:
        unauthenticated_menu()
        return
    
    authenticated_menu()

def menu_with_redirect():
    if not st.session_state["authentication_status"]:
        st.switch_page("app.py")

    menu()