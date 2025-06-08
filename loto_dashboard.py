
import streamlit as st
import pandas as pd
import yaml
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader

st.set_page_config(page_title="Lebanese Loto Dashboard", layout="wide")

# Load config
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    credentials=config['credentials'],
    cookie_name=config['cookie']['name'],
    key=config['cookie']['key'],
    expiry_days=config['cookie']['expiry_days'],
    preauthorized=config.get('preauthorized', {})
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    st.sidebar.success(f"Welcome {name}")
    st.title("Lebanese Loto Prediction Dashboard")

    uploaded_file = st.file_uploader("Upload historical Loto data (Excel)", type=["xlsx"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.dataframe(df.head())

    if st.button("Generate Prediction"):
        st.write("Predicted numbers (example):")
        st.success("4 - 11 - 18 - 23 - 32 - 37")

    if st.button("Export Predictions"):
        st.info("Export to Excel feature coming soon.")

    authenticator.logout("Logout", "sidebar")

elif authentication_status is False:
    st.error("Username/password is incorrect")

elif authentication_status is None:
    st.warning("Please enter your username and password")
