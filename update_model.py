import pickle
from pathlib import Path
import github
from github import Github
import os
from dotenv import load_dotenv
import streamlit as st
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris

iris = load_iris()
X = iris.data
y = iris.target

# Retrain the model with new data
new_model = DecisionTreeClassifier(random_state=42)
new_model.fit(X, y)

# Update the existing model object with the new model
model = new_model


# Convert the model to binary content
updated_model_content = pickle.dumps(model)


def update(updated_model):
  # Replace 'YOUR_ACCESS_TOKEN' with your actual access token
  access_token = os.environ.get('PAT')
  # Create a PyGithub instance with your access token
  g = Github(access_token)

  repo_owner = 'adamzzio'
  repo_name = 'FINAL_EXAM_ML'
  file_path = 'model/decision_tree_model_test1.sav'

  # Get the repository object
  repo = g.get_user(repo_owner).get_repo(repo_name)

  # Get the contents of the model file as bytes
  file_content = repo.get_contents(file_path)
  existing_sha = file_content.sha
  # file_content = file_content.decoded_content
#   st.write(file_content)
#   st.write(file_path)
#   st.write(existing_sha)
#   st.write(access_token)
  repo.update_file(file_path, "Updated model file", updated_model, existing_sha, branch="main")
#   st.write(github.enable_console_debug_logging())
  # repo.create_file("test.txt", "test", "test")

update(updated_model_content)
