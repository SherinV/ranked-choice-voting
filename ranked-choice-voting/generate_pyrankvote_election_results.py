import pyrankvote
import pandas as pd
import numpy as np
from pyrankvote import Candidate, Ballot
from pyrankvote.models import DuplicateCandidatesError


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

    indices_to_drop = []

    for index, value in enumerate(df['candidate_list']):
        try:
            ballot = Ballot(ranked_candidates=value)
            ballot_objects.append(ballot)
        except DuplicateCandidatesError:
            print(f'duplicated candidate on ballot {index}')
            indices_to_drop.append(index)


    return ballot_objects, indices_to_drop


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

def pyrankvote_main(file_path_of_election):

    df = pd.read_csv('us_vt_btv_2009.csv')

    df1 = df.pivot(index='ballot_id', columns='rank', values='choice').rename_axis(None, axis=1).reset_index()

    # Getting rid of under/over votes
    mask = np.column_stack([df1[col].str.contains(r"\$", na=False) for col in df1])
    indices_to_drop = df1.loc[mask.any(axis=1)].index
    df1 = df1.drop(index=indices_to_drop)

    # Getting rid of write-ins
    mask = np.column_stack([df1[col].str.contains(r"Write-in", na=False) for col in df1])
    indices_to_drop = df1.loc[mask.any(axis=1)].index
    df1 = df1.drop(index=indices_to_drop)

    # Making Candidates
    df1 = df1.replace(np.nan, '0')
    df1 = get_cands_into_single_cell(df1)
    df1['candidate_list'] = df1['candidate_list'].apply(lambda x: x.replace('0, ', '').replace(', 0', ''))
    df1 = rm_invalid_rows(df1)
    df1['candidate_list'] = df1['candidate_list'].apply(lambda x: initialize_cand_objs(x))

    # Making Ballots
    ballots, indices_to_drop = initialize_ballot_objs(df1)  # found dupes

    df1 = df1.drop(index=indices_to_drop)

    df1['ballots'] = ballots
    cand_list = get_cand_list(df1)
    cand_list = initialize_cand_objs(cand_list)

    # Simulate election
    election = run_election(cand_list, df1)

    # Add election winners to dataframe
    pyrankvote_winner = election.get_winners()[0].name  # Extracting single string rep'ing election winner
    df['pyrankvote_winner'] = pyrankvote_winner

    return df, cand_list, ballots


if __name__ == "__main__":  # would read in concatenated csvs here
    bob_kiss_wins = pyrankvote_main('us_vt_btv_2009.csv')
    print('hi')
