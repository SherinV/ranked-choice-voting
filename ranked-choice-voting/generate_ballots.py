from itertools import permutations
import pandas as pd
import numpy as np
from datetime import datetime
import sys


# unit test for this would just be len(returned_list) = permutations of num_cands:
def generate_all_possible_rank_combos(num_cands):
    """
    :param num_cands: number of candidates for an election
    :return: list of tuples, each tuple contains unique combination of ranks
    """
    return list(permutations(list(range(1,num_cands+1))))


# unit test = that the number is btwn 500 and 50k:
def pick_rand_num_of_ballots_for_an_election():
    """
    :return: a random number between 500-50k to tell us how many ballots we should generate for an election
    """
    return(np.random.randint(500, 50001))


# unit test = weights have to sum to 1.0 always
def generate_weights_to_apply_to_each_unique_set_of_ranks(cand_ranks):
    """
    :param cand_ranks: list of tuples, each tuple contains unique combination of ranks
    :return: list of weights that sum to 1.0 that will be used to determine the percentage of the total ballots
        in an election that look like one of the unique rank combinations
    """
    num_unique_rank_combos = len(cand_ranks)
    weights = np.random.randint(1, 101, num_unique_rank_combos)
    weights = [weight/sum(weights) for weight in weights]
    return weights


def generate_distribution_of_ballots(num_ballots_in_election, weights):
    """
    :param num_ballots_in_election: total rows (i.e. ballots) to be generated for an election
    :param weights: weights to apply to unique combo of ranks (i.e. unique ballots) generated for an election
    :return: list of ints, where each int == num rows (i.e. ballots) to be generated per unique rank combo
        for an election
    """
    total_rows = num_ballots_in_election
    distribution_of_ballots = []
    for weight in weights:
        distribution_of_ballots.append(int(round(total_rows*weight)))
    return distribution_of_ballots


def generate_ballots(distribution_of_ballots, cand_ranks):
    ballots = []
    for unique_rank_combo in range(len(cand_ranks)):
        ballots.append([cand_ranks[unique_rank_combo]]*distribution_of_ballots[unique_rank_combo])
    return ballots


def turn_ballots_into_dfs(list_of_ballots, cand_names):
    return [pd.DataFrame(ballot_combo, columns=cand_names) for ballot_combo in list_of_ballots]


def reconcile_num_ballots_with_len_df(num_total_ballots, df):
    if len(df) == num_total_ballots:
        print(f'length of df ({len(df)}) matches total num of ballots ({num_total_ballots})')
        return df

    if len(df) < num_total_ballots:
        print(f'length of df ({len(df)}) is less than total num of ballots ({num_total_ballots})')
        diff = num_total_ballots - len(df)
        df = pd.concat([df, df[-1:]*diff])
        df.reset_index(inplace=True, drop=True)
        return df

    if len(df) > num_total_ballots:
        print(f'length of df ({len(df)}) is longer than total num of ballots ({num_total_ballots})')
        diff = len(df) - num_total_ballots
        df = df[:-diff]
        return df

def add_noise(percent_noise, matrix_shape):
    """
    :param percent_noise:
    :param matrix_shape:
    :return:
    """
    p = [percent_noise/1, 1-percent_noise/1]
    n = matrix_shape[0]
    m = matrix_shape[1]
    return np.random.choice([0, 1], size=(n, m), p=p)

def generate_ballots_main_function(num_cands, names_of_cands):
    candidate_ranks = generate_all_possible_rank_combos(num_cands)  # unit test that len(cand ranks) == len(cand names)
    num_ballots_in_election = pick_rand_num_of_ballots_for_an_election()
    weights = generate_weights_to_apply_to_each_unique_set_of_ranks(candidate_ranks)
    election_row_distribution = generate_distribution_of_ballots(num_ballots_in_election, weights)
    ballots = generate_ballots(election_row_distribution, candidate_ranks)
    dfs = turn_ballots_into_dfs(ballots, names_of_cands)
    df = pd.concat(dfs)
    df = reconcile_num_ballots_with_len_df(num_ballots_in_election, df)
    return df

def ballots_main(num_cands: int, amount_of_noise: int) -> None:
    """
    Writes dataframe to csv.
    Dataframe has cols "candidate_1, candidate_2, candidate_3"
    """

    # hyperparams
    names_of_cands = [f'candidate_{i}' for i in range(1, num_cands+1)]
    amount_of_noise = (amount_of_noise/100)/num_cands
    date = datetime.now()
    file_date = date.strftime("%m-%d-%Y_%H-%M-%S")

    # funcs:
    df = generate_ballots_main_function(num_cands, names_of_cands)
    matrix_shape = df.to_numpy().shape
    noise_matrix = add_noise(percent_noise=amount_of_noise, matrix_shape=matrix_shape)
    df = df * noise_matrix

    col_replacements = list(range(1, len(df.columns) + 1))
    for i in col_replacements:
        df = df.replace({i: df.columns[i - 1]})

    df['num_candidates'] = num_cands
    df['noise'] = amount_of_noise
    df.to_csv(f'../data/election_{file_date}_{num_cands}cands_{amount_of_noise}noise.csv')


if __name__ == "__main__":
    for i in range(20):   # change to 25k when ready

        # rand # cands btwn 3-8, with 3 being the most likely randomly-generated number:
        cands = np.random.choice([3, 4, 5, 6, 7, 8], 1, p=[.6, .25, .1, .03, .015, 0.005])[0]
        noise = np.random.randint(0, 15)
        ballots_main(cands, noise)
