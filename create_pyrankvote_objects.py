import pyrankvote
import pandas as pd
from pyrankvote import Candidate, Ballot


def rename_index_col_to_ballot_id(df):
    df.columns.values[0] = "ballot_id"
    return df

def get_cand_list(df):
    list_of_unique_vals_in_dataframe = df.iloc[:, 1].value_counts().index
    cand_list = list(filter(lambda x: x != '0', list_of_unique_vals_in_dataframe))
    return cand_list

def create_cand(x):
    return Candidate(x)

def initialize_cand_objs(cand_list):
    cand_objs = [create_cand(cand) for cand in cand_list]
    return cand_objs

def initialize_cand_objs_in_df_cols(df):
    cands_df = df.iloc[:, 1:]  # getting all columns with candidate names in them
    cands_df = cands_df.applymap(lambda x: create_cand(x))  # making them into pyrankvote candidate objects
    cands_df['ballot_id'] = df.iloc[:, 0]  # stitching df back with ballot_ids from old dataframe
    return cands_df


def main():
    df = pd.read_csv('election_04-25-2020_20-24-11_3cands_11noise.csv')
    df = rename_index_col_to_ballot_id(df)

    cand_list = get_cand_list(df)
    cand_objs = initialize_cand_objs(cand_list)

    df = initialize_cand_objs_in_df_cols(df)


    return 'hi'



if __name__ == "__main__":
    main()