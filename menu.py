import streamlit as st

def authenticated_menu():
    st.sidebar.page_link("app.py", label="Log in")
    st.sidebar.page_link("pages/tierlist.py", label="Tierlist")


def unauthenticated_menu():
    st.sidebar.page_link("app.py", label="Log in")
    
def menu():
    if "auth" not in st.session_state or st.session_state.auth is False:
        unauthenticated_menu()
        return
    
    authenticated_menu()

def menu_with_redirect():
    if "auth" not in st.session_state or st.session_state.auth is False:
        st.switch_page("app.py")

    menu()