import sys
import os
from ranked_choice_voting.generate_ballots import ballots_main
from ranked_choice_voting.intermediate_master import create_intermediate_master_file
from ranked_choice_voting.final_master_feature_extraction import feature_extraction_main
import pandas as pd
import numpy as np


def create_dataset_for_modeling(num_ballots_to_generate, user_input=None):
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

    master_df.to_csv('master.csv', index=False)



if __name__ == "__main__":
    if not os.path.isdir('../data/'):
        os.mkdir('../data/')
        num_ballots_to_generate = int(sys.argv[1])
        create_dataset_for_modeling(num_ballots_to_generate, user_input=[3, 2])
    else:
        num_ballots_to_generate = int(sys.argv[1])
        create_dataset_for_modeling(num_ballots_to_generate, user_input=[3, 2])
