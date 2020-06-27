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

    cand_matrix = pd.DataFrame(0, columns=candidate_names, index=candidate_names)
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
    return cand_matrix


def countX(lst, x):
    return lst.count(x)


def return_winners(cand_matrix):
    results = []
    result_dict = {}
    for i in cand_matrix.index:
        key = ''.join([str(countX(list(cand_matrix.loc[i]), '--') + 1), ". ", i])
        result_dict[key] = [countX(list(cand_matrix.loc[i]), '--') + 1,
                            (countX(list(cand_matrix.loc[i]), '++'), countX(list(cand_matrix.loc[i]), '--'))]
    for key, item in sorted(result_dict.items(), key=lambda x: x[1]):
        results.append("Rank %s: [Rank, (Wins, losses] %s" % (key, item))

    return results


def condorcet_compile(candidates, ballots):
    ballot_dict = create_ballot_dict(ballots)

    candidate_names = []
    for cand in candidates:
        candidate_names.append(cand.name)

    cand_matrix = pd.DataFrame(0, columns=candidate_names, index=candidate_names)

    for votes, ballot in ballot_dict.values():
        ranked_candidates = [cand.name for cand in list(ballot.ranked_candidates)]
        process_cands = list(cand_matrix.columns)
        for i, current_cand in enumerate(ranked_candidates):
            process_cands.remove(current_cand)
            cand_matrix.loc[current_cand][process_cands] = cand_matrix.loc[current_cand][process_cands] + votes

    symbolize_cand_matrix(cand_matrix)
    return return_winners(cand_matrix)


def parse_condorcet_results(condorcet_results):  # list
    parsed_results = []

    for i in condorcet_results:
        cand = i.split(':')[0].split('. ')[1]
        wins = int(i.split(':')[1].split(', ')[-2:][0].split('(')[1])
        parsed_results.append((cand, wins))

    return parsed_results


def return_condorcet_winner(parsed_results):
    return sorted(parsed_results, key=lambda x: x[1], reverse=True)[0][0]

def main():
    # candidates = list of Candidate() objects
    # ballots = list of Ballot() objects
    df, cand_list, ballots = pyrankvote_main()
    condorcet_results = condorcet_compile(cand_list, ballots)
    parsed_condorcet_results = parse_condorcet_results(condorcet_results)
    winner = return_condorcet_winner(parsed_condorcet_results)

    df['condorcet_winner'] = winner

    if df['pyrankvote_winner'].all() != df['condorcet_winner'].all():
        df['spoiled'] = 'Y'
    else:
        df['spoiled'] = 'N'
    return df

if __name__ == "__main__":
    df = main()


