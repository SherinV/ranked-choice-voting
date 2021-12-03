import streamlit as st
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from templates.s3_stuff import open_s3_connections, download_and_load_pickled_model_from_s3
from ranked_choice_voting.index import create_dataset_for_modeling

st.title("How Likely is the Spoiler Effect in Ranked Choice Voting Systems?")

## S3
s3_connection = open_s3_connections()

st.subheader("How many elections do you want to produce?")
num_elections = st.text_input('Number of elections',  value=1)

cont = st.checkbox("Check to continue", key='1')

if cont:
    if int(num_elections) == 1:
        num_cands = st.select_slider('Select the number of candidates for your election', options=[3, 4, 5, 6, 7, 8], value=3)
        cont = st.checkbox("Check to continue", key='2')
        if cont:
            amt_noise = st.select_slider('Select the amount of noise in your election. (Integers you choose get turned'
                                         ' into percentages with orders of magnitude proportional to their '
                                         'original values.)', options=list(np.arange(0, 16, .5)), value=0.0)

            cont = st.checkbox("Check to create your election", key='3')  # TODO: make progress bar
            if cont:
                df = create_dataset_for_modeling(1, user_input=[num_cands, amt_noise])
                st.dataframe(df)

                # Legend:
                st.markdown(body='## Columns')
                st.markdown(body='`round[x]winnervotes`: # votes [x] round winner received')
                st.markdown(body='`total_votes_allrounds`: Total # of votes across all rounds')
                st.markdown(body='`num_candidates`: # candidates in election as a whole')
                st.markdown(body='`noise`: amount of partial ballots cast in election')
                st.markdown(body='`spoiled`: whether or not the election is predicted to be spoiled '
                                 '(`0` = not spoiled, `1` = spoiled)')

    else:
        st.subheader("Range of candidates:")
        # TODO: account for edge case: when min/max on slider(s) is the same for 1 of 2 hyperparams
        num_cands = st.slider('Select a range representing the number of candidates each election in your dataset'
                              ' can have. Range is inclusive.',
                              3, 8, (3, 8))
        cont = st.checkbox("Check to continue", key='4')
        if cont:
            st.subheader("Range of noise:")
            amt_noise = st.slider('Select a range representing the amount of noise each election in your dataset '
                                  'can have. Range is inclusive. (Integers you choose get turned into percentages with'
                                  ' orders of magnitude proportional to their original values.)',
                                  0, 15, (0, 15))
            cont = st.checkbox("Check to create your election(s)", key='5')
            if cont:
                with st.spinner('Calculating... *beep bop boop*...'):

                    df = create_dataset_for_modeling(int(num_elections), user_input=[num_cands, amt_noise])
                    st.success('ta da!')
                    st.dataframe(df)

                    # Legend: # TODO: update legend w/new cols
                    st.markdown(body='## Columns')
                    st.markdown(body='`round[x]winnervotes`: # votes [x] round winner received')
                    st.markdown(body='`total_votes_allrounds`: Total # of votes across all rounds')
                    st.markdown(body='`num_candidates`: # candidates in election as a whole')
                    st.markdown(body='`noise`: amount of partial ballots cast in election')
                    st.markdown(body='`spoiled`: whether or not the election is predicted to be spoiled '
                                         '(`0` = not spoiled, `1` = spoiled)')

        cont = st.checkbox('Check to retrieve model')
        if cont:
            rf_model = download_and_load_pickled_model_from_s3(s3_connection, 'models/anxela_model.pkl')
            st.success('Model retrieved')

        cont = st.checkbox('Check to train model with your data')
        if cont:
            user_election_data = pd.read_csv('final_master.csv')

            user_election_data.fillna(0, inplace=True)

            # x, y
            X = df.iloc[:, :-1]
            Y = df.iloc[:, -1]


            # preds
            predictions = rf_model.predict(X)

            ## VISUALIZING
            st.title("Results")
            conf_matrix = confusion_matrix(Y, predictions, normalize='all')
            st.write(conf_matrix)






# TODO: include something re: # of ballots in each election that are auto-generated
# TODO: include legend for reading election(s) dataframe
# TODO: include styling for election(s) dataframe (not necessary, but pretty)
# TODO: figure out way to avoid truncation of dataframe cells









