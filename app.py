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

# database
from firebase_admin import db
import firebase_admin
import csv
import google.cloud
from firebase_admin import credentials, firestore

# etc
from PIL import Image
import requests
import pickle
from pathlib import Path
from sklearn.preprocessing import LabelEncoder
from github import Github
from sklearn.tree import DecisionTreeClassifier
import os
from dotenv import load_dotenv

# ===== SET PAGE =====
pageicon = Image.open("CardioCheck.png")
st.set_page_config(page_title="CardioCheck Web App", page_icon=pageicon, layout="wide")

# ===== INITIALIZE DATABASE =====
def get_firebase_app():
    # Periksa apakah aplikasi Firebase sudah ada
    if not firebase_admin._apps:
        # Jika belum ada, inisialisasi Firebase Admin SDK
        cred = credentials.Certificate("test-db-19c39-firebase-adminsdk-3noie-95deabbed0.json")
        firebase_admin.initialize_app(cred)
    # Kembalikan referensi ke aplikasi Firebase
    return firebase_admin.get_app()

def load_data_from_firebase():
    app = get_firebase_app()
    db = firestore.client(app)
    collection_name = "dataset_ML"
    # Dapatkan semua dokumen dari koleksi "feedback"
    ML_docs = db.collection(collection_name).stream()
    ML_data = []
    for doc in ML_docs:
        ML_data.append(doc.to_dict())
    # Konversi data menjadi DataFrame
    df = pd.DataFrame(ML_data)
    df['Gender'] = df['Gender'].replace("Laki-Laki", "1")
    df['Gender'] = df['Gender'].replace("Perempuan", "0")
    df = df[["Age", "Gender", "Heart rate", "Systolic blood pressure", "Diastolic blood pressure",
            "Blood sugar", "CK-MB", "Troponin", "Result"]]
    cols_num = ["Age", "Gender", "Heart rate", "Systolic blood pressure", "Diastolic blood pressure",
                "Blood sugar", "CK-MB", "Troponin"]
    for col in cols_num:
        df[col] = df[col].astype(float)
    return df

def load_data_from_firebase_feedback():
    app = get_firebase_app()
    db = firestore.client(app)
    collection_name = "feedback"
    # Dapatkan semua dokumen dari koleksi "feedback"
    feedback_docs = db.collection(collection_name).stream()
    feedback_data = []
    for doc in feedback_docs:
        feedback_data.append(doc.to_dict())
    # Konversi data menjadi DataFrame
    df = pd.DataFrame(feedback_data)
    df = df[["Stars", "Tingkat Kepuasan", "Ulasan"]]
    return df

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
    
    # ===== LOAD DATABASE =====
#     @st.cache_resource
#     def load_data():
#     dataset_ML = load_data_from_firebase()
#     feedback_df = load_data_from_firebase_feedback()
#         return dataset_ML, feedback_df

#     dataset_ML, feedback_df = load_data()
    
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
        'menu',
        ('Pilih Menu', 'Dataset', 'Dashboard', 'Re-train Model'), label_visibility="hidden")
    
    if option == 'Dataset':
        dataset_ML = load_data_from_firebase()
        feedback_df = load_data_from_firebase_feedback()
        st.write("### Dataset ML")
        st.dataframe(dataset_ML, use_container_width = True)
        st.write("### Dataset Feedback")
        st.dataframe(feedback_df, use_container_width = True)
        
    elif option == 'Dashboard':
        # load data
        dataset_ML = load_data_from_firebase()
        feedback_df = load_data_from_firebase_feedback()
        feedback_df['Stars'] = feedback_df['Stars'].astype(int)
        
        # create KPI dashboard
        st.markdown('<hr>', unsafe_allow_html=True)
        left_column_kpi, right_column_kpi = st.columns(2)
        with left_column_kpi:
            st.subheader("Rata-rata Rating Bintang")
            star_rating = ":star:" * int(round(feedback_df['Stars'].mean(), 0))
            st.write(star_rating, "(", np.round(feedback_df['Stars'].mean(), 2), ")")
        with right_column_kpi:
            st.subheader("Proporsi Kepuasan")
            proporsi_puas = feedback_df[feedback_df['Tingkat Kepuasan'] == 'Puas'].shape[0] / feedback_df.shape[0]
            proporsi_puas = np.round(proporsi_puas, 2)
            proporsi_puas = proporsi_puas*100
            st.write(proporsi_puas, "%")
        st.markdown('<hr>', unsafe_allow_html=True)
        
        # create bar rating star
        count_star = feedback_df['Stars'].value_counts()
        count_star = pd.DataFrame(count_star).sort_values(by='Stars',
                                                          ascending=False)

        fig_count_star = px.bar(count_star,
                                x=count_star.index,
                                y="count",
                                title="<b>Jumlah Rating Star</b>",
                                labels={"index": "Tingkat Bintang",
                                        "count":"Stars"},
                                color_discrete_sequence=["#0083B8"] * len(count_star),
                                template="plotly_white",
        )
        fig_count_star.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )
        st.plotly_chart(fig_count_star, use_container_width=True)
        
        # create bar tingkat kepuasan
        count_puas = feedback_df['Tingkat Kepuasan'].value_counts()
        count_puas = pd.DataFrame(count_puas).sort_values(by='Tingkat Kepuasan',
                                                          ascending=False)

        fig_count_puas = px.bar(count_puas,
                                x=count_puas.index,
                                y="count",
                                title="<b>Jumlah Tingkat Kepuasan</b>",
                                labels={"index": "Tingkat Kepuasan",
                                        "count":"Jumlah"},
                                color_discrete_sequence=["#0083B8"] * len(count_puas),
                                template="plotly_white",
        )
        fig_count_puas.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )
        st.plotly_chart(fig_count_puas, use_container_width=True)
        
        # create bar avg star by tingkat kepuasan
        avg_star_puas = feedback_df.groupby('Tingkat Kepuasan')['Stars'].mean()
        avg_star_puas = pd.DataFrame(avg_star_puas).sort_values(by='Stars',
                                                                ascending=False)

        fig_avg_star_puas = px.bar(avg_star_puas,
                                   x=avg_star_puas.index,
                                   y="Stars",
                                   title="<b>Rata-rata Rating Bintang berdasarkan Tingkat Kepuasan</b>",
                                   labels={"Tingkat Kepuasan": "Tingkat Kepuasan",
                                           "Stars":"Rata-rata Rating Bintang"},
                                   color_discrete_sequence=["#0083B8"] * len(avg_star_puas),
                                   template="plotly_white",
        )
        fig_avg_star_puas.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )
        st.plotly_chart(fig_avg_star_puas, use_container_width=True)
        
    elif option == 'Re-train Model':
        st.error('PERINGATAN : ANDA AKAN MEMPERBARUI MODEL! PASTIKAN UNTUK MENDAPATKAN PERSETUJUAN DARI STAKEHOLDER TERKAIT')
        retrain = st.button("Re-train Model", use_container_width=True)
        if retrain:
            dataset_ML = load_data_from_firebase()
            le = LabelEncoder()
            dataset_ML['Result'] = le.fit_transform(dataset_ML['Result'])
#             st.dataframe(dataset_ML, use_container_width=True)
            # Load environment variables from .env file
#             load_dotenv()
            # Replace 'YOUR_ACCESS_TOKEN' with your actual access token
            access_token = os.environ.get('ACCESS_TOKEN')

            # Create a PyGithub instance with your access token
            g = Github(access_token)

            repo_owner = 'adamzzio'
            repo_name = 'FINAL_EXAM_ML'
            file_path = 'model/finalized_model_dt_tuning_v1.sav'

            # Get the repository object
            repo = g.get_user(repo_owner).get_repo(repo_name)

            # Get the contents of the model file as bytes
            file_content = repo.get_contents(file_path)
            existing_sha = file_content.sha
            # file_content = file_content.decoded_content
            # st.write(file_content)

            # Load the model from the binary content
            # model = pickle.loads(file_content)
            
            # Re-train model 
            X = dataset_ML.drop(columns = ['Result']).values
            y = dataset_ML['Result'].values
            
            # Retrain the model with new data
            new_model = DecisionTreeClassifier(random_state=42)
            new_model.fit(X, y)

            # Update the existing model object with the new model
            # model = new_model
            st.dataframe(new_model.predict(X))

            # Convert the model to binary content
            # Save the updated model to a file
            filename = 'finalized_model_dt_tuning_v1.sav'
            pickle.dump(new_model, open(filename, 'wb'))

            # Read the updated model file as bytes
            with open(filename, 'rb') as file:
                updated_model_content = file.read()

            # Update the file on GitHub
            # repo.update_file(file_path, "Updated model file", updated_model_content, existing_sha)
            st.write(file_content)
            st.success("Model has been succesfully retrained and updated")
            
    authenticator.logout("Logout", "main")
