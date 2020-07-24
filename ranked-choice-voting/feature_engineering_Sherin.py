import pyrankvote
import ast
import pandas as pd
from pyrankvote import Candidate, Ballot
import glob
import os

def create_master_file(file_name_pattern, master_file_path):
    file_names = [name for name in glob.glob(file_name_pattern)]
    # combine all files in the list
    data = []
    for csv in file_names:
        print('csv:', csv)
        frame = pd.read_csv(csv)
        print("before:", len(frame))

        frame['filename'] = os.path.basename(csv)
        filter_col = [col for col in frame if col.startswith('candidate_')]
        for col in filter_col:
            idx = frame[col].str.isnumeric() & (frame[:][col] != '0')
            frame = frame[~idx]
            print("after:", len(frame))
        data.append(frame)

    # concat all dfs
    combined_csv_df = pd.concat(data)
    # export to csv
    combined_csv_df.to_csv(master_file_path, index=False)


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

def get_cands_into_single_cell(df):
    df['candidate_list'] = df.iloc[:, 1:].agg(", ".join, axis=1)
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


def run_all_steps(df):
    election_dict = {}
    df = df.dropna(axis=1, how='all')
    df = df.drop(['ballot_id', 'filename', 'num_candidates', 'noise'], axis=1)
    print('df.shape', df.shape)
    df = get_cands_into_single_cell(df)

    df['candidate_list'] = df['candidate_list'].apply(lambda x: x.replace('0, ', '').replace(', 0', ''))
    df = rm_invalid_rows(df)
    df['candidate_list'] = df['candidate_list'].apply(lambda x: initialize_cand_objs(x))

    ballots = initialize_ballot_objs(df)
    df['ballots'] = ballots

    cand_list = get_cand_list(df)
    cand_list = initialize_cand_objs(cand_list)
    print("cand_list: ", cand_list)
    election = run_election(cand_list, df)
    winner = election.get_winners()
    print("get_winners", winner)
    election_dict['winner'] = winner
    print("rounds", len(election.rounds))
    election_dict['rounds'] = len(election.rounds)

    #     open file and write results. read winners votes from file and write to df
    print("election:", election)
    election_dict['election'] = election

    #     print("election type:", type(election))
    election_dict['register'] = election.register_round_results(election.rounds[-1])

    # print('hi')
    return df, election_dict


def read_votes(file, election_dict,winner):
    with open(file, 'r') as file1:
        count = 0
        while True:
            count += 1

            # Get next line from file
            line = file1.readline()
            if not line:
                break
            strip_line = line.strip()
            #         print('*',strip_line,'*')
            if 'ROUND' in strip_line or 'FINAL' in strip_line:
                start_round = True
                if 'ROUND 1' in strip_line or 'FINAL' in strip_line:
                    monitor_round = True
                    print('*', strip_line, '*')
                else:
                    monitor_round = False
            if 'ROUND' not in strip_line and 'FINAL' not in strip_line:
                start_round = False
                if winner in line and monitor_round:
                    print('*', strip_line, '*')
                    if 'firstRoundVotes' not in election_dict:
                        election_dict['firstRoundVotes'] = [int(s) for s in strip_line.split() if s.isdigit()].pop()
                    else:
                        election_dict['finalRoundVotes'] = [int(s) for s in strip_line.split() if s.isdigit()].pop()

    file1.close()

def gen_features_sv():
    file_name_pattern = "../data/election_07-24-2020_09-47-*.csv"
    master_file_path = "../data/combined_csv.csv"
    create_master_file(file_name_pattern, master_file_path)
    #load master file
    df = pd.read_csv(master_file_path)
    rename_index_col_to_ballot_id(df)
    election_ids = df['filename'].unique()
    all_elections_dict = {}

    #Store each election file and number in a dict
    election_num_dict = {}
    for election_num, election in enumerate(election_ids):
        election_num_dict[election_num] = election

    #Run each election and generate results
    for election_num, election in enumerate(election_ids):
        print("***********Election: ",election_num, election)
        df_election = df.loc[df['filename'] == election]
        temp_df, election_dict = run_all_steps(df_election)
        print(election_dict)
        if len(election_dict['winner']) == 1:
            winner = election_dict['winner'][0].name
            election_dict['winner'] = winner
        else:
            print(election, "has more than one winner")
        result_file = '../data/out.txt'
        with open(result_file, 'w') as file1:
            print(election_dict['election'], file=file1)
        read_votes(result_file, election_dict,winner)
        all_elections_dict[election_num] = election_dict

    #Store results
    election_results_df = pd.DataFrame()
    election_results_list = []


    for key, val in all_elections_dict.items():
        val['election_id'] = election_num_dict[key]
        del val['register']
        del val['election']
        print(val)

        election_results_list.append(val)
    election_results_df = pd.DataFrame(election_results_list)
    election_results_df.to_csv('sher_features.csv', index=False)

if __name__ == "__main__":
    gen_features_sv()