import streamlit as st
import numpy as np
from templates.s3_stuff import open_s3_connections, download_and_load_pickled_model_from_s3

st.title("How Likely is the Spoiler Effect in Ranked Choice Voting Systems?")

## S3
s3_connection = open_s3_connections()

st.subheader("How many elections do you want to produce?")
num_elections = st.text_input('Number of elections',  value=1)

next = st.button("Press to continue", key='1')
if next:
    if int(num_elections) == 1:
        st.write("Select the number of candidates for your election")
        num_cands = st.select_slider('Candidates must number between 3-8', options=[3, 4, 5, 6, 7, 8], value=3)

        # TODO: figure out why it goes back to step 1 once you select num_cands here
        st.write("Select the amount of noise in your election")
        amt_noise = st.select_slider('Maximum amount of noise is 15%', options=list(np.arange(0, 16, .5)), value=0.0)

    else:
        st.write("Select a range for how many candidates can be randomly applied to elections within your set")
        # TODO: figure out way to prevent same number being the min and max on the slider below
        num_cands = st.slider('Candidates range', 3, 8, (3, 8))
        st.subheader("Number of candidates:")
        st.write(f'Elections within my dataset will have anywhere from {num_cands[0]} candidates to {num_cands[1]} candidates')

        st.write("Select the amount of noise in your election")
        st.subheader("Amount of noise:")
        amt_noise = st.slider('Amount noise', 0.0, 15.0, (0.0, 15.0))
        st.write(f'Elections within my dataset will incorporate a certain amount of noise, ranging from {amt_noise[0]}% to {amt_noise[1]}%')




# with st.spinner('Fetching pretrained model from S3...'):
#     # TODO: figure out how to make loading the model from S3 faster
#     # TODO: how to make this wait until user has input hyperparams
#     rf_model = download_and_load_pickled_model_from_s3(s3_connection, 'models/audrey_test_rf_model')
#     st.success('Model retrieved')



# user_election_data = pd.read_csv('ranked-choice-voting/final_master.csv')
#
# # x, y
# user_election_data_without_outcome = user_election_data.iloc[:, :-1]
# user_election_data_outcome = user_election_data.iloc[:, -1:].values
#
# # preds
# predictions = rf_model.predict(user_election_data_without_outcome)
#
# ## VISUALIZING
# st.title("Results")
# conf_matrix = confusion_matrix(user_election_data_outcome, predictions, normalize='all')
# st.write(conf_matrix)




