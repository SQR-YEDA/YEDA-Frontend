import streamlit as st
from menu import menu

print(st.session_state)
if "auth" not in st.session_state:
    st.session_state.auth = False

st.session_state._auth = st.session_state.auth

def set_auth():
    st.session_state.auth = st.session_state._auth

st.selectbox(
    "Select auth:",
    [False, True],
    key="_auth",
    on_change=set_auth,
)

if "auth_form" not in st.session_state:
    st.session_state.auth_form = "sign in"

st.session_state._auth_form = st.session_state.auth_form

def set_auth_form():
    st.session_state.auth_form = st.session_state._auth_form

st.selectbox(
    "Select auth type:",
    ["sign up", "sign in"],
    key="_auth_form",
    on_change=set_auth_form,
)

if st.session_state.auth_form== "sign up":
    with st.form("Sign Up Form"):
        username_sign_up = st.text_input("Username *", placeholder = 'Enter a unique username')
        password_sign_up = st.text_input("Password *", placeholder = 'Create a strong password', type = 'password')

        st.markdown("###")
        sign_up_submit_button = st.form_submit_button(label = 'Register')

        #if sign_up_submit_button:
            # Тут запрос на бек...

if st.session_state.auth_form == "sign in":
    with st.form("Login Form"):
        username = st.text_input("Username", placeholder = 'Your unique username')
        password = st.text_input("Password", placeholder = 'Your password', type = 'password')

        st.markdown("###")
        login_submit_button = st.form_submit_button(label = 'Login')

        # if login_submit_button:
            
        
menu()
