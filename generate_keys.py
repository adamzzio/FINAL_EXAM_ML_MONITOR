import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ['Admin']
usernames = ['XXX']
passwords = ['XXX']

hashed_paswords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_paswords, file)