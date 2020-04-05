from itertools import permutations
import pandas as pd
import numpy as np
import math

# unit test for this would just be len(returned_list) = permutations of num_cands:
def generate_all_possible_rank_combos(num_cands):
    """
    :param num_cands: number of candidates for an election
    :return: list of tuples, each tuple contains unique combination of ranks
    """
    return list(permutations(list(range(1,num_cands+1))))


def generate_election_df(cand_ranks, names_of_cands):
    """
    :param names_of_cands: list of strings; each string == candidate name
    :return: dataframe with columns named per candidate; each row is a ranked ballot
    """
    df = pd.DataFrame(data=cand_ranks, columns=names_of_cands)
    return df


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
    :param weights: weights per unique combo of ranks (i.e. unique ballots) generated for an election
    :return: list of ints, where each int == num rows (i.e. ballots) to be generated per unique rank combo
        for an election
    """
    total_rows = num_ballots_in_election
    distribution_of_ballots = []
    for weight in weights:
        distribution_of_ballots.append(int(round(total_rows*weight)))
    return distribution_of_ballots






if __name__ == "__main__":
    # hyperparams:
    num_cands = 3
    names_of_cands = ['audrey', 'moeid', 'sherin']

    # funcs:
    candidate_ranks = generate_all_possible_rank_combos(num_cands) # unit test that len(cand ranks) == len(cand names)
    num_ballots_in_election = pick_rand_num_of_ballots_for_an_election()
    weights = generate_weights_to_apply_to_each_unique_set_of_ranks(candidate_ranks)
    election_row_distribution = generate_distribution_of_ballots(num_ballots_in_election, weights)

    df = generate_election_df(candidate_ranks, names_of_cands)




    print(df)