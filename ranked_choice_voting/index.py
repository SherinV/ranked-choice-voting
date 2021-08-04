import sys
import os
import shutil
from ranked_choice_voting.generate_ballots import ballots_main
from ranked_choice_voting.intermediate_master import create_intermediate_master_file
from ranked_choice_voting.final_master_feature_extraction import feature_extraction_main
import pandas as pd
import numpy as np


def create_dataset_for_modeling(num_ballots_to_generate, user_input=None):
    if not os.path.isdir('data/'):
        os.mkdir('data/')
    else:
        directory = 'data/'
        for files in os.listdir(directory):
            path = os.path.join(directory, files)
            try:
                shutil.rmtree(path)
            except OSError:
                os.remove(path)

    ballots_main(num_ballots_to_generate, user_input)
    ballot_level_features_df = create_intermediate_master_file()  # audrey's script
    election_level_features_df = feature_extraction_main()  # anxhela & sherin script

    master_df = pd.merge(election_level_features_df,
                         ballot_level_features_df[['num_candidates', 'noise', 'pyrankvote_winner', 'condorcet_winner', 'spoiled', 'filename']],
                         on='filename',
                         sort=False)

    master_df = master_df.drop_duplicates()

    # Drop all cols with "Rounds" info:
    to_filter_out = [col for col in master_df if not col.startswith('Round')]
    master_df = master_df[to_filter_out]

    # Drop other cols we don't :
    master_df = master_df.drop(columns=['Election', 'filename',
                                        'pyrankvote_winner_x',
                                        'condorcet_winner',
                                        'pyrankvote_winner_y'])

    # Vectorizing dependent var:
    master_df['spoiled'] = np.where(master_df['spoiled'] == 'Y', 0, 1)  # 0 = yes, 1 = no

    master_df.to_csv('./master.csv', index=False)
    return master_df


if __name__ == "__main__":
    # if num elections generated = 1
    if not os.path.isdir('data/'):
        os.mkdir('data/')
        num_ballots = int(sys.argv[1])
        # create_dataset_for_modeling(num_ballots, user_input=[3, 2])  # user_input=[(3, 8), (0, 3)]
        create_dataset_for_modeling(num_ballots)
    else:
        num_ballots = int(sys.argv[1])
        # create_dataset_for_modeling(num_ballots, user_input=[3, 2])
        create_dataset_for_modeling(num_ballots)

