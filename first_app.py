import streamlit as st
import numpy as np
import pandas as pd
import time
from sklearn.ensemble import RandomForestClassifier as rf
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from templates.s3_stuff import open_s3_connections, download_csv_from_s3_and_load_as_df

st.title("How Likely is the Spoiler Effect in Ranked Choice Voting Systems?")

s3_connection = open_s3_connections()

data = download_csv_from_s3_and_load_as_df(s3_connection, file_name='final_master.csv')
data = data.replace(np.nan, 0)

X = data.iloc[:, :-1].values
y = data['spoiled'].values

train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.20, random_state = 0)

rf_model = rf(n_estimators=1000, random_state=42)

"training model..."  # TODO: get code for generating moving bar for how long this takes
rf_model.fit(train_X, train_y)  # TODO: figure out how to cache this or skip it altogether for same user

predictions = rf_model.predict(test_X)

conf_matrix = confusion_matrix(test_y, predictions, normalize=True)

st.write(conf_matrix)


# 'Starting a long computation...'
#
# # Add a placeholder
# latest_iteration = st.empty()
# bar = st.progress(0)
#
# for i in range(100):
#   # Update the progress bar with each iteration.
#   latest_iteration.text(f'Iteration {i+1}')
#   bar.progress(i + 1)
#   time.sleep(0.1)
#
# '...and now we\'re done!'
#
# progress_bar = st.progress(0)
# status_text = st.empty()
# chart = st.line_chart(np.random.randn(10, 2))
#
# for i in range(100):
#     # Update progress bar.
#     progress_bar.progress(i + 1)
#
#     new_rows = np.random.randn(10, 2)
#
#     # Update status text.
#     status_text.text(
#         'The latest random number is: %s' % new_rows[-1, 1])
#
#     # Append data to the chart.
#     chart.add_rows(new_rows)
#
#     # Pretend we're doing some computation that takes time.
#     time.sleep(0.1)
#
# status_text.text('Done!')
# st.balloons()