import os
import glob
from typing import List
from typing import Dict
from typing import Tuple
import pandas as pd
import pyrankvote
from pyrankvote import Candidate, Ballot


def create_master_file_from_csvs(glob_pattern='../data/*.csv') -> pd.DataFrame():
    """
    Combine election-level csvs in data dir into
    single master dataset using a generator

    :param glob_pattern: pattern for recursive glob
        search files

    :return: master dataset as dataframe
    """

    def yielder(glob_pattern):
        for file in glob.glob(glob_pattern):
            df = pd.read_csv(file, index_col=0)
            df['filename'] = os.path.basename(file)

            # takes care of edge case where elections
            # have unexplainable numbers instead of cands
            filter_col = [col for col in df if col.startswith('candidate_')]
            for col in filter_col:
                idx = df[col].str.isnumeric() & (df[:][col] != '0')
                df = df[~idx]

            yield df

    master_df = pd.concat(list(yielder(glob_pattern)))
    master_df.to_csv('./master_elections.csv', index=False)
    return master_df


def get_cands_into_single_cell(df: pd.DataFrame()) -> List:
    """
    Per election within master dataframe, take
    all candidates and put them in one cell, separating
    them with commas

    :param df: master dataset

    :return: tk
    """
    group_dfs = []
    for name, group in df.groupby('filename'):
        group = group.dropna(axis=1, how='all')
        cand_cols = [col for col in group if col.startswith('candidate_')]
        group['candidate_list'] = group[cand_cols].agg(", ".join, axis=1)
        group_dfs.append(group)
    return group_dfs

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

def run_single_election(list_of_cand_objs: List, list_of_ballot_objs: List) -> pyrankvote.instant_runoff_voting:
    return pyrankvote.instant_runoff_voting(list_of_cand_objs,
                                            list_of_ballot_objs,
                                            pick_random_if_blank=True)

def transform_single_election_metadata_to_dict(str) -> Dict:
    """
    :param str:
    :return:
    """

    list_of_rounds = [i for i in str.split('\n') if i.startswith('R') or i.startswith('F')]
    split_into_rounds = str.split('\n\n')
    rounds = []

    # for each round (2):
    for round in range(0, len(split_into_rounds)):
        # isolate the candidate names (3):
        cands = split_into_rounds[round].split('\n')[3:]
        cands = [i.split('  ') for i in cands]
        cand_votes = []
        # for each candidate name, isolate the # of votes
        # and save the name,# tuple to cand_votes
        for cand in cands:
            if len(cand)>1:
                cand_name = cand[0]
                num_votes = cand[-2]
                cand_with_votes = {cand_name: num_votes}
                cand_votes.append(cand_with_votes)
        rounds.append((f'Round: {round+1}', cand_votes))

    return dict(rounds)

def run_all_elections(df):
    elect_results = []
    for name, group in df.groupby('filename'):
        cands = group['candidate_list'].to_list()[0]
        ballots = group['ballots'].to_list()
        elect_result = run_single_election(cands, ballots)
        elect_results.append((elect_result.__str__(), elect_result))
    return elect_results

def make_election_dicts(elect_results) -> List[Dict[str,List[Dict[str,str]]]]:
    elect_dicts = []
    for result in elect_results:
        elect_dicts.append(transform_single_election_metadata_to_dict(result[0]))
    return elect_dicts


if __name__ == "__main__":
    # master_df = create_master_file_from_csvs()
    master_df = pd.read_csv('./master_elections.csv')  # tmp
    dfs_with_cands_list = get_cands_into_single_cell(master_df)
    master_df = pd.concat([df for df in dfs_with_cands_list])  # len = 105775

    # remove rows w/only 0s
    master_df = master_df[master_df['candidate_list'] != '0']

    # replacing 0s with blank space to work with pyrankvote
    master_df['candidate_list'] = master_df['candidate_list'].apply(
        lambda x: x.replace('0, ', '').replace(', 0', ''))

    # initializing pyrankvote candidate objs
    master_df['candidate_list'] = master_df['candidate_list'].apply(lambda x: initialize_cand_objs(x))

    # initializing ballot objs
    master_df['ballots'] = initialize_ballot_objs(master_df)

    all_election_metadata = run_all_elections(master_df)  # metadata + election result

    election_dicts = make_election_dicts(all_election_metadata)


    print('hi')