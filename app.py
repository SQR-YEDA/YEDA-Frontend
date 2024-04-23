import streamlit as st
from menu import menu
import requests
from constants import API
from streamlit_jwt_authenticator import Authenticator

def handler(data, res):
    print(data)
    print(res)
    return

authenticator = Authenticator(f"{API}/login", response_handler=handler, headers={"Content-Type": "application/json"})

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

        if sign_up_submit_button:
            data = requests.post(f"{API}/register", json={ 'login': username_sign_up, 'password': password_sign_up })

            if data.status_code == 200:
                st.session_state.auth_form="sign in"
            else:
                st.markdown('ERROR');

if st.session_state.auth_form == "sign in":
    authenticator.login()
   
    if st.session_state["authentication_status"]:
        st.markdown("Content")
    
    # with st.form("Login Form"):
    #     username = st.text_input("Username", placeholder = 'Your unique username')
    #     password = st.text_input("Password", placeholder = 'Your password', type = 'password')

    #     st.markdown("###")
    #     login_submit_button = st.form_submit_button(label = 'Login')

    #     if login_submit_button:
    #         data = requests.post(f"{API}/login", json={ 'login': username, 'password': password })

    #         if data.status_code == 200:
    #             token = data.json()['tokens']['access_token']
    #         else:
    #             st.markdown('ERROR');
            
        
menu()
