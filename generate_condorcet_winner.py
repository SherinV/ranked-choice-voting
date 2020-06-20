from generate_pyrankvote_election_results import pyrankvote_main
import pandas as pd
import re

def create_ballot_dict(ballots):
    """
    """
    all_ballots = ballots
    ballot_dict = {}
    for i in range(len(all_ballots)):
        ballot_str = str(all_ballots[i])
        curr_ballot = all_ballots[i]
        if ballot_str in ballot_dict:
            ballot_dict[ballot_str][0] = ballot_dict[ballot_str][0] + 1
        else:
            ballot_dict[ballot_str] = [1, all_ballots[i]]
    return ballot_dict


def create_candidate_matrix(candidates):
    candidate_names = []
    for cand in candidates:
        candidate_names.append(cand.name)

    print("candidate_names: ", candidate_names)
    cand_matrix = pd.DataFrame(0, columns=candidate_names, index=candidate_names)
    # display(cand_matrix)
    return cand_matrix


def symbolize_cand_matrix(cand_matrix):
    for i in cand_matrix.index:
        for j in cand_matrix.columns:
            if i == j:
                cand_matrix.loc[i, j] = '`'
            else:
                if cand_matrix.loc[i, j] != '++' and cand_matrix.loc[i, j] != '--':
                    if cand_matrix.loc[i, j] > cand_matrix.loc[j, i]:
                        cand_matrix.loc[i, j] = '++'
                        cand_matrix.loc[j, i] = '--'
                    else:
                        cand_matrix.loc[i, j] = '--'
                        cand_matrix.loc[j, i] = '++'
    # display(cand_matrix)
    return cand_matrix

def countX(lst, x):
    return lst.count(x)

def return_winners(cand_matrix):
    # This func returns Condorcet winner
    result_dict = {}
    for i in cand_matrix.index:
        key = ''.join([str(countX(list(cand_matrix.loc[i]), '--') + 1), ". ", i])
        result_dict[key] = [countX(list(cand_matrix.loc[i]), '--') + 1,
                            (countX(list(cand_matrix.loc[i]), '++'), countX(list(cand_matrix.loc[i]), '--'))]

    keys = []
    items = []
    for key, item in sorted(result_dict.items(), key=lambda x: x[1]):
        keys.append(key.split('. ')[1])  # this will append candidate name
        items.append(item[1][0])  # this will append # pairwise faceoffs won by candidate

    pairwise_df = pd.DataFrame(data=[items], columns=keys)
    condorcet_winner = pairwise_df.max().reset_index().max().values[0]  # gets name of cand who won all faceoffs

    return condorcet_winner


def condorcet_compile(candidates, ballots):
    # all_ballots = list(df['ballot_objects'].values)

    print("Creating the ballot dictionary...")
    ballot_dict = create_ballot_dict(ballots)

    print("Creating the candidate matrix to store pairwise results...")
    candidate_names = []
    for cand in candidates:
        candidate_names.append(cand.name)

    print("\ncandidate_names: ", candidate_names)
    cand_matrix = pd.DataFrame(0, columns=candidate_names, index=candidate_names)

    print("\nUpdating the candidate matrix with pairwise results...")

    for votes, ballot in ballot_dict.values():
        ranked_candidates = [cand.name for cand in list(ballot.ranked_candidates)]
        process_cands = list(cand_matrix.columns)
        for i, current_cand in enumerate(ranked_candidates):
            process_cands.remove(current_cand)
            cand_matrix.loc[current_cand][process_cands] = cand_matrix.loc[current_cand][process_cands] + votes

    print("\n")
    print(cand_matrix)
    print("\nSymbolizing the candidate matrix with pairwise results...\n")

    symbolize_cand_matrix(cand_matrix)
    print("\n\nCondorcet results: ")
    return return_winners(cand_matrix)

def main():
    # candidates = list of Candidate() objects
    # ballots = list of Ballot() objects
    df, cand_list, ballots = pyrankvote_main()
    condorcet_winner = condorcet_compile(cand_list, ballots)
    df['condorcet_winner'] = condorcet_winner
    return df

if __name__ == "__main__":
    df = main()
    print('hi')


