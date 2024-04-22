import streamlit as st
from menu import menu_with_redirect

menu_with_redirect()

if(st.button("Logout")):
    st.session_state.auth = False
    st.switch_page("app.py")

st.title("Tierlist")