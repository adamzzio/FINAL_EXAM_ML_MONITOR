import pickle
from pathlib import Path
from github import Github
import os
from dotenv import load_dotenv
import streamlit as st

def update(updated_model):
  # Replace 'YOUR_ACCESS_TOKEN' with your actual access token
  access_token = os.environ.get('PAT')
  # Create a PyGithub instance with your access token
  g = Github(access_token)

  repo_owner = 'adamzzio'
  repo_name = 'FINAL_EXAM_ML'
  file_path = '/model/decision_tree_model_test1.sav'

  # Get the repository object
  repo = g.get_user(repo_owner).get_repo(repo_name)

  # Get the contents of the model file as bytes
  file_content = repo.get_contents(file_path)
  existing_sha = file_content.sha
  file_content = file_content.decoded_content
  st.write(file_content)
  st.write(file_path)
  st.write(existing_sha)
  st.write(access_token)
  # repo.update_file(file_path, "Updated model file", updated_model, existing_sha)

