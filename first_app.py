import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier as rf
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from templates.s3_stuff import open_s3_connections, download_and_load_pickled_model_from_s3

st.title("How Likely is the Spoiler Effect in Ranked Choice Voting Systems?")

## S3
s3_connection = open_s3_connections()

with st.spinner('Fetching pretrained model from S3...'):
    rf_model = download_and_load_pickled_model_from_s3(s3_connection, 'models/audrey_test_rf_model')
    st.success('Model retrieved')

# TODO: make script that takes user-input hyperparams & makes the 'final_master' file
user_election_data = pd.read_csv('ranked-choice-voting/final_master.csv')

# x, y
user_election_data_without_outcome = user_election_data.iloc[:, :-1]
user_election_data_outcome = user_election_data.iloc[:, -1:].values

# preds
predictions = rf_model.predict(user_election_data_without_outcome)

## VISUALIZING
st.title("Results")
conf_matrix = confusion_matrix(user_election_data_outcome, predictions, normalize='all')
st.write(conf_matrix)




