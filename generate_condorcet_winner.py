from generate_pyrankvote_election_results import pyrankvote_main
import pandas as pd
import re

def create_ballot_dict(ballots):
    """
    :goal: create dict of ballots where key is unique ballot & key is frequency of unique ballot in an election
    :param ballots: list of ballot objects from election dataframe
    :return: dict of ballots where key is unique ballot & key is frequency of unique ballot in an election
    """
    ballot_dict={}
    for i in range(len(ballots)):
        ballot_str = str(ballots[i])  # has to be a string or else dict creation does not count correctly
        if ballot_str in ballot_dict:
            ballot_dict[ballot_str][0] = ballot_dict[ballot_str][0] + 1
        else:
            ballot_dict[ballot_str] = [1]
    return ballot_dict

def fill_in_candidate_matrix(ballot_dict,  candidate_matrix):
    for key, value in ballot_dict.items():  # key = ballot, value = # of votes

        ranked_candidates = re.search('\(([^)]+)', key).group(1).split(', ')

        process_cands = list(candidate_matrix.columns)

        for index, candidate in enumerate(ranked_candidates):
            process_cands.remove(candidate)
            candidate_matrix.loc[candidate][process_cands] = candidate_matrix.loc[candidate][process_cands] + candidate

    return candidate_matrix

def condorcet_main(ballots, candidate_matrix):
    fill_in_candidate_matrix(create_ballot_dict(ballots), candidate_matrix)
    print('hi')

if __name__ == "__main__":
    df = pyrankvote_main()

    # Used to make ballot_dict in create_ballot_dict funcs
    ballots = df.ballots.to_list()

    # List of candidates' names (str) for an election
    candidates = [i.name for i in sorted(df['candidate_list'].value_counts().index,
                                         key = lambda x: len(x), reverse=True)[0]]

    # Create candidate x candidate matrix for Condorcet evaluation
    candidate_matrix = pd.DataFrame(0, columns=candidates, index=candidates)

    condorcet_main(ballots, candidate_matrix)
