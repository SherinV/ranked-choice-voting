import pyrankvote
import pandas as pd
from pyrankvote import Candidate, Ballot


def rename_index_col_to_ballot_id(df):
    """
    :goal: turn unnamed index column from csv dataframe as ballot id
    :param df:
    :return:
    """
    df.rename(columns={'Unnamed: 0': 'ballot_id'}, inplace=True)
    return df

def get_cand_list(df):
    """
    :goal: Get a list of the candidates for an election, excluding 0s
    :param df:
    :return:
    """
    list_of_unique_vals_in_dataframe = df.iloc[:, 1].value_counts().index
    cand_list = list(filter(lambda x: x != '0', list_of_unique_vals_in_dataframe))
    return cand_list

def initialize_cand_objs(cand_list):
    """
    :goal: Initialize Candidate() objects from PyRankVote library
    :param cand_list:
    :return:
    """
    if isinstance(cand_list, str):
        return [Candidate(c) for c in cand_list.split(', ')]
    else:
        return [Candidate(c) for c in cand_list]

def get_cands_into_single_cell(df):
    """
    :goal: Get all candidates into a list & then into a single cell within the election dataframe
    :param df:
    :return:
    """
    df['candidate_list'] = df.iloc[:, 1:].agg(", ".join, axis=1)
    return df

def initialize_ballot_objs(df):
    """
    :goal: initialize Ballot() objects from PyRankVote library
    :param df:
    :return:
    """
    ballot_objects = []
    for index, value in enumerate(df['candidate_list']):
        ballot = Ballot(ranked_candidates=value)
        ballot_objects.append(ballot)
    return ballot_objects

def run_election(list_of_cand_objs, election_df):
    """
    :goal: simulate Instant Runoff Voting election via PyRankVote
    :param list_of_cand_objs:
    :param election_df:
    :return:
    """
    return pyrankvote.instant_runoff_voting(list_of_cand_objs, election_df['ballots'], pick_random_if_blank=True)

def rm_invalid_rows(df):
    """
    :goal: Get rid of rows/ballots with only 0s
    :param df:
    :return:
    """
    return df[df['candidate_list'] != '0']

def pyrankvote_main():
    # Read in election
    df = pd.read_csv('./data/election_05-20-2020_08-09-28_3cands_16noise.csv')

    # Data cleaning & initializing necessary class Objects
    df = rename_index_col_to_ballot_id(df)
    df = get_cands_into_single_cell(df)
    df['candidate_list'] = df['candidate_list'].apply(lambda x: x.replace('0, ', '').replace(', 0', ''))
    df = rm_invalid_rows(df)
    df['candidate_list'] = df['candidate_list'].apply(lambda x: initialize_cand_objs(x))
    ballots = initialize_ballot_objs(df)
    df['ballots'] = ballots
    cand_list = get_cand_list(df)
    cand_list = initialize_cand_objs(cand_list)

    # Simulate election
    election = run_election(cand_list, df)

    # Add election winners to dataframe
    pyrankvote_winner = election.get_winners()[0].name  # Extracting single string rep'ing election winner
    df['pyrankvote_winner'] = pyrankvote_winner

    return df


if __name__ == "__main__":
    df = pyrankvote_main()
