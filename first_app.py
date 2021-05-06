import streamlit as st
import numpy as np
from sklearn.ensemble import RandomForestClassifier as rf
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from templates.s3_stuff import open_s3_connections, download_csv_from_s3_and_load_as_df

st.title("How Likely is the Spoiler Effect in Ranked Choice Voting Systems?")

## S3
s3_connection = open_s3_connections()
data = download_csv_from_s3_and_load_as_df(s3_connection, file_name='final_master.csv')

## CLEANUP
data = data.replace(np.nan, 0)

## MODELING
X = data.iloc[:, :-1].values
y = data['spoiled'].values

train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.20, random_state = 0)

rf_model = rf(n_estimators=1000, random_state=42)

with st.spinner('Training Random Forest classifier...'):
    rf_model.fit(train_X, train_y)
    st.success('Training complete')

predictions = rf_model.predict(test_X)

## VISUALIZING
st.title("Results")
conf_matrix = confusion_matrix(test_y, predictions, normalize='all')
st.write(conf_matrix)



