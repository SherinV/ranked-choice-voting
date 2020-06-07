from generate_pyrankvote_election_results import pyrankvote_main
import pandas as pd

def create_ballot_dict(ballots):
    """
    :goal: create dict of ballots where key is unique ballot & key is frequency of unique ballot in an election
    :param ballots: list of ballot objects from election dataframe
    :return: dict of ballots where key is unique ballot & key is frequency of unique ballot in an election
    """
    ballot_dict={}
    for i in range(len(ballots)):
        ballot_str = str(ballots[i])
        if ballot_str in ballot_dict:
            ballot_dict[ballot_str][0] = ballot_dict[ballot_str][0] + 1
        else:
            ballot_dict[ballot_str] = [1]
    return ballot_dict


def condorcet_main(ballots):
    ballot_dict = create_ballot_dict(ballots)


if __name__ == "__main__":
    df = pyrankvote_main()

    # Used to make ballot_dict in create_ballot_dict funcs
    ballots = df.ballots.to_list()

    # Get list of candidates per election
    # Used for create_candidate_matrix func
    candidates = [i.name for i in sorted(df['candidate_list'].value_counts().index,
                                         key = lambda x: len(x), reverse=True)[0]]

    # Create candidate x candidate matrix for Condorecet evaluation
    candidate_matrix = pd.DataFrame(0, columns=candidates, index=candidates)

    condorcet_main(ballots)
