# ===== IMPORT LIBRARY =====
# for data manipulation
import pandas as pd
import numpy as np

# for web app
import streamlit as st
import streamlit_authenticator as stauth
import streamlit_lottie as st_lottie

# for dataviz
import plotly.express as px
import matplotlib.pyplot as plt

# etc
from PIL import Image
import requests
import pickle
from pathlib import Path

# ===== SET PAGE =====
pageicon = Image.open("CardioCheck.png")
st.set_page_config(page_title="CardioCheck Web App", page_icon=pageicon, layout="wide")

# ===== SET USERNAME =====
names = ['Admin']
usernames = ['admin123']

# ===== LOAD HASHED PASSWORD =====
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

# ===== SET AUTHENTICATE =====
authenticator = stauth.Authenticate(names,
                                    usernames,
                                    hashed_passwords,
                                    'test',
                                    'abc',
                                    cookie_expiry_days=30)

# ===== SET LOGIN PAGE =====
name, authentication_status, username = authenticator.login("Login", "main")

# ===== CONDITIONAL STATEMENT LOGIN PAGE =====
if authentication_status == False:
    st.error("Username / Password is incorrect")
if authentication_status == None:
    st.warning("Please Enter Your Username & Password")
if authentication_status:
    st.header(f'Welcome {st.session_state["name"]} !')
    st.markdown('<hr>', unsafe_allow_html=True)
    # ===== DEVELOP FRONT-END =====
    # SET HEADER PAGE
    st.header('CardioCheck: Monitoring & Retraining Model')
    # def load_lottieurl(url):
    #     r = requests.get(url)
    #     if r.status_code != 200:
    #         return None
    #     return r.json()

    # lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_CdU3jV.json")

    # intro_column_left, intro_column_right = st.columns(2)
    # with st.container():
    #     with intro_column_left:
    #         # st.title(":bar_chart: Dashboard")
    #         st.markdown(
    #             '<div style="text-align: justify; font-size:300%; line-height: 150%; margin-top: -55px;"> <b><br>CardioCheck: Monitoring & Retraining Model </b> </div>', unsafe_allow_html=True)
    #     # with intro_column_right:
    #     #     st_lottie(lottie_coding, height=250, key="dashboard")

    st.markdown('<hr>', unsafe_allow_html=True)
    option = st.selectbox(
        'Pilih Menu?',
        ('Dataset', 'Dashboard', 'Re-train'))

    st.button("Re-train Model", use_container_width=True)
    authenticator.logout("Logout", "main")
