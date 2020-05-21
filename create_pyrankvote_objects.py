import pyrankvote
import ast
import pandas as pd
from pyrankvote import Candidate, Ballot


def rename_index_col_to_ballot_id(df):
    df.rename(columns={'Unnamed: 0': 'ballot_id'}, inplace=True)
    return df

def get_cand_list(df):
    list_of_unique_vals_in_dataframe = df.iloc[:, 1].value_counts().index
    cand_list = list(filter(lambda x: x != '0', list_of_unique_vals_in_dataframe))
    return cand_list

def initialize_cand_objs(cand_list):
    if isinstance(cand_list, str):
        return [Candidate(c) for c in cand_list.split(', ')]
    else:
        return [Candidate(c) for c in cand_list]

# def initialize_cand_objs_in_df_cols(df):
#     cands_df = df.iloc[:, 1:]  # getting all columns with candidate names in them
#     cands_df = cands_df.applymap(lambda x: create_cand(x))  # making them into pyrankvote candidate objects
#     cands_df['ballot_id'] = df.iloc[:, 0]  # stitching df back with ballot_ids from old dataframe
#     return cands_df

def get_cands_into_single_cell(df):
    df['candidate_list'] = df.iloc[:, 1:].agg(", ".join, axis=1)
    # cands_to_put_in_single_cell = df.iloc[:, 1:].columns.to_list()
    # df['candidate_list'] = str(cands_to_put_in_single_cell)
    # df['candidate_list'] = df['candidate_list'].apply(lambda x: ast.literal_eval(x))
    return df

def initialize_ballot_objs(df):
    ballot_objects = []
    for index, value in enumerate(df['candidate_list']):
        ballot = Ballot(ranked_candidates=value)
        ballot_objects.append(ballot)
    return ballot_objects

def run_election(list_of_cand_objs, election_df):
    return pyrankvote.instant_runoff_voting(list_of_cand_objs, election_df['ballots'], pick_random_if_blank=True)

def rm_invalid_rows(df):
    return df[df['candidate_list'] != '0']

def main():
    df = pd.read_csv('./data/election_05-20-2020_08-09-28_3cands_16noise.csv')
    df = rename_index_col_to_ballot_id(df)
    df = get_cands_into_single_cell(df)

    df['candidate_list'] = df['candidate_list'].apply(lambda x: x.replace('0, ', '').replace(', 0', ''))
    df = rm_invalid_rows(df)
    df['candidate_list'] = df['candidate_list'].apply(lambda x: initialize_cand_objs(x))

    ballots = initialize_ballot_objs(df)
    df['ballots'] = ballots

    cand_list = get_cand_list(df)
    cand_list = initialize_cand_objs(cand_list)

    election = run_election(cand_list, df)
    print(election)


    print('hi')






if __name__ == "__main__":
    main()