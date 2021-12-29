import streamlit as st
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from templates.s3_stuff import open_s3_connections, download_and_load_pickled_model_from_s3
from ranked_choice_voting.index import create_dataset_for_modeling


st.title("How Likely is the Spoiler Effect in Ranked Choice Voting Systems?")
s3_connection = open_s3_connections()
st.markdown(body='## Choose Your Hyperparameters:')
number = st.number_input(label='Insert the number of elections you want to generate', min_value=0, value=1)

if number == 1:
    num_cands = st.number_input(label='Select the number of candidates for your election', min_value=3,
                                max_value=8, value=3)
    amt_noise = st.select_slider('Select the amount of noise in your election. (Integers you choose get turned'
                                 ' into percentages with orders of magnitude proportional to their '
                                 'original values.)', options=list(np.arange(0, 16, .5)), value=0.0)
    cont = st.checkbox("Check to create your election", key='1')
    if cont:
        with st.spinner('Calculating... *beep bop boop*...'):
            df = create_dataset_for_modeling(1, user_input=[num_cands, amt_noise])
            st.success('ta da!')
            st.markdown(body='## Your Election:')
            st.dataframe(df)
            # Legend:
            st.markdown(body='## Legend')
            st.markdown(body='`round[x]winnervotes`: # votes [x] round winner received')
            st.markdown(body='`total_votes_allrounds`: Total # of votes across all rounds')
            st.markdown(body='`num_dropped_cands_Round: [x]`: Total # of canddiates droppped each round')
            st.markdown(body='`num_candidates`: # candidates in election as a whole')
            st.markdown(body='`noise`: amount of partial ballots cast in election')
            st.markdown(body='`spoiled`: whether or not the election is predicted to be spoiled '
                             '(`0` = not spoiled, `1` = spoiled)')
else:
    # TODO: account for edge case: when min/max on slider(s) is the same for 1 of 2 hyperparams
    # TODO: fix amt_noise not being able to be 0
    num_cands = st.slider('Select a range of candidates for your elections. Range is inclusive.',
                          min_value=3, max_value=8, value=(3, 8))
    amt_noise = st.slider('Select a range noise for your elections Range is inclusive.',
                          min_value=0, max_value=15, value=(0, 15))
    cont = st.checkbox("Check to create your elections", key='2')
    if cont:
        with st.spinner('Calculating... *beep bop boop*...'):
            df = create_dataset_for_modeling(int(number), user_input=[num_cands, amt_noise])
            st.success('ta da!')
            st.markdown(body='## Your Elections:')
            st.dataframe(df)
            st.markdown(body='## Legend')
            st.markdown(body='`round[x]winnervotes`: # votes [x] round winner received')
            st.markdown(body='`total_votes_allrounds`: Total # of votes across all rounds')
            st.markdown(body='`num_dropped_cands_Round: [x]`: Total # of canddiates droppped each round')
            st.markdown(body='`num_candidates`: # candidates in election as a whole')
            st.markdown(body='`noise`: amount of partial ballots cast in election')
            st.markdown(body='`spoiled`: whether or not the election is predicted to be spoiled '
                                 '(`0` = not spoiled, `1` = spoiled)')

            st.markdown(body='## Model Time:')
            cont_model = st.checkbox('Click to fetch pretrained model')
            if cont_model:
                rf_model = download_and_load_pickled_model_from_s3(s3_connection, 'models/anxela_model.pkl')
                st.success('Model retrieved')
                cont_train = st.checkbox('Check to train model with your data')
                if cont_train:
                    user_election_data = pd.read_csv('master.csv')
                    user_election_data.fillna(0, inplace=True)

                    X = df.iloc[:, :-1]
                    Y = df.iloc[:, -1]

                    # preds
                    predictions = rf_model.predict(X)
                    st.write(Y)  # just for debugging

                    ## VISUALIZING
                    st.title("Results")
                    conf_matrix = confusion_matrix(Y, predictions, labels=[0, 1])
                    st.write(conf_matrix)


# TODO: include something re: # of ballots in each election that are auto-generated
# TODO: include legend for reading election(s) dataframe
# TODO: include styling for election(s) dataframe (not necessary, but pretty)
# TODO: figure out way to avoid truncation of dataframe cells
# TODO: make steps into diff side bars?
# TOOD: figure out how to make check boxes maintain previous state
# TODO: dockerize shit
# TODO: change labels on confusion matrix to words








