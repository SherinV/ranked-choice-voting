import os
import glob
from typing import List
from typing import Dict
import pandas as pd
from final_master_feature_extraction import feature_extraction_main
from generate_condorcet_winner import *
import pyrankvote
from pyrankvote import Candidate, Ballot


def create_master_file_from_csvs(glob_pattern=r'C:\Users\anxhe\Documents\github\ranked-choice-voting\data\*.csv') -> pd.DataFrame():
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
            print(df.shape)
            df['filename'] = os.path.basename(file)

            # takes care of edge case where elections
            # have unexplainable numbers instead of cands
            filter_col = [col for col in df if col.startswith('candidate_')]
            # if any of the rows have numbers other than 0 (partial votes are represented as 0's), remove those rows
            for col in filter_col:
                idx = df[col].str.isnumeric() & (df[:][col] != '0')
                df = df[~idx]
            # if any rows contain all '0's, drop that row
            df = df[(df[filter_col]!='0').any(axis=1)].reset_index(drop=True)

            yield df

    master_df = pd.concat(list(yielder(glob_pattern)))
    # master_df.to_csv('master_elections.csv', index=False)
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
        group.loc[:,'candidate_list'] = group[cand_cols].agg(", ".join, axis=1)
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
        rounds.append((f'Round: {round+1}', cand_votes, ))

    return dict(rounds)

def run_all_elections(df):
    """
    :return:
        List of election results. Each
        result has the metadata of the election,
        the pyrankvote election object, the
        election winner (pyrankvote Candidate obj),
        and the file name of the election
    """
    elect_results = []
    for name, group in df.groupby('filename'):
        cands = group['candidate_list'].to_list()
        cands = max(cands, key=len)
        ballots = group['ballots'].to_list()
        elect_result = run_single_election(cands, ballots)
        pyrankvote_winner = elect_result.get_winners()
        elect_results.append((elect_result.__str__(),
                              elect_result,
                              pyrankvote_winner,
                              name))
    return elect_results

def make_election_dicts(elect_results) -> List[Dict[str,List[Dict[str,str]]]]:
    elect_dicts = []
    for result in elect_results:
        elect_dict = transform_single_election_metadata_to_dict(result[0])
        elect_dict['Election'] = result[-1]
        elect_dicts.append(elect_dict)
    return elect_dicts

def make_winners_df(tuple_of_pyrankvote_election_obj_and_filename):
    winner_filename_tuple = [(i[2], i[3]) for i in tuple_of_pyrankvote_election_obj_and_filename]
    df = pd.DataFrame(winner_filename_tuple, columns=['pyrankvote_winner', 'filename'])
    return df

def get_condorcet_results(df):
    groups = []
    for name, group in df.groupby('filename'):
        cand_list = group['candidate_list'].to_list()
        cand_list = max(cand_list, key=len)
        ballots = group['ballots'].to_list()
        condorcet_election = condorcet_compile(cand_list, ballots)
        parsed_condorcet = parse_condorcet_results(condorcet_election)
        condorcet_winner = return_condorcet_winner(parsed_condorcet)
        group.loc[:,'condorcet_winner'] = condorcet_winner
        groups.append(group)
    return groups

def indicate_spoiled(df):
    if df['pyrankvote_winner'].all() != df['condorcet_winner'].all():
        df['spoiled'] = 'Y'
    else:
        df['spoiled'] = 'N'
    return df

def transform_name_of_pyrankvote_winner(pyrankvote_winner_obj):
    """
    Extract candidate name from pyrankvote winner object
    """
    return pyrankvote_winner_obj[0].name

def filter_out_cand_zeros(df):
    indices_to_delete = []
    for i,v in enumerate(df['candidate_list']):
        if "0" in str(v[0]) and len(v) ==1:
            indices_to_delete.append(i)
    df = df.drop(index=indices_to_delete)
    return indices_to_delete


def create_intermediate_master_file():
    master_df = create_master_file_from_csvs()  # writes a file
    dfs_with_cands_list = get_cands_into_single_cell(master_df)
    master_df = pd.concat([df for df in dfs_with_cands_list])  # len = 105775

    # remove rows w/only 0s
    # master_df = master_df[master_df['candidate_list'] != '0']
    # master_df = filter_out_cand_zeros(master_df)

    # replacing 0s with blank space to work with pyrankvote
    master_df['candidate_list'] = master_df['candidate_list'].apply(
        lambda x: x.replace('0, ', '').replace(', 0', ''))

    # initializing pyrankvote candidate objs
    master_df['candidate_list'] = master_df['candidate_list'].apply(lambda x: initialize_cand_objs(x))

    # initializing ballot objs
    master_df['ballots'] = initialize_ballot_objs(master_df)

    all_election_metadata = run_all_elections(master_df)
    # example of one item from all_election_metadata:
    # 'ROUND 1\nCandidate      Votes  Status\n-----------  -------  --------\ncandidate_3    18581  Hopeful\ncandidate_2    13659  Hopeful\ncandidate_1     9433  Rejected\n\nFINAL RESULT\nCandidate      Votes  Status\n-----------  -------  --------\ncandidate_2    21423  Elected\ncandidate_3    20250  Rejected\ncandidate_1        0  Rejected\n', <ElectionResults(2 rounds)>, [<Candidate('candidate_2')>], 'election_07-21-2020_10-40-22_3cands_0.006666666666666667noise.csv')


    # creating and converting election dictionary to dataframe and merging winners df with it on filename:
    election_dicts = make_election_dicts(all_election_metadata)
    elect_dict = pd.DataFrame(election_dicts)
    winners_df = make_winners_df(all_election_metadata)


    final_elect_df = pd.merge(elect_dict, winners_df, left_on='Election', right_on='filename')
    final_elect_df.to_csv(r"C:\Users\anxhe\Documents\github\ranked-choice-voting\data\election_dict.csv")  # writes a file


    # with pyrankvote winners:
    master_df = pd.merge(master_df, winners_df, on='filename')  # ballot-level dataframe

    condorcet_winners_df = get_condorcet_results(master_df)


    # with condorcet winners
    master_df = pd.concat([df for df in condorcet_winners_df])
    

    # Got to pull name out of pyrankvote obj to work
    # with spoiled/not-spoiled function below
    master_df['pyrankvote_winner'] = master_df['pyrankvote_winner'].apply(transform_name_of_pyrankvote_winner)

    master_df = indicate_spoiled(master_df)

    # master_df.to_csv('master_dataset.csv', index=False)

    return master_df


if __name__ == "__main__":
    create_intermediate_master_file()
