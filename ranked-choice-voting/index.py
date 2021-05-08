import sys
from generate_ballots import ballots_main
from intermediate_master import create_intermediate_master_file
from final_master_feature_extraction import feature_extraction_main
from multiprocessing import Pool
import multiprocessing
import pandas as pd
import numpy as np

def create_dataset_for_modeling(num_ballots_to_generate):
    ballots_main(num_ballots_to_generate)
    ballot_level_features_df = create_intermediate_master_file()  # audrey's script
    election_level_features_df = feature_extraction_main()  # anxhela & sherin script

    master_df = pd.merge(election_level_features_df,
                         ballot_level_features_df[['num_candidates', 'noise', 'pyrankvote_winner', 'condorcet_winner', 'spoiled', 'filename']],
                         on='filename',
                         sort=False)

    master_df = master_df.drop_duplicates()

    # Drop all cols with "Rounds" info:
    to_filter_out = [col for col in master_df if not col.startswith('Round')]
    master_df  = master_df[to_filter_out]

    # Drop other cols we don't :
    master_df = master_df.drop(columns=['Election', 'filename',
                                        'pyrankvote_winner_x',
                                        'condorcet_winner',
                                        'pyrankvote_winner_y'])

    # Vectorizing dependent var:
    master_df['spoiled'] = np.where(master_df['spoiled'] == 'Y', 0, 1)  # 0 = yes, 1 = no

    master_df.to_csv('master.csv', index=False)


if __name__ == "__main__":
    num_ballots_to_generate = int(sys.argv[1])
    create_dataset_for_modeling(num_ballots_to_generate)

    # TODO: automatically make data directory

    # Pooling type #1 (seems to take longer than #2):
    # total_threads = 5
    # pool = Pool(processes=total_threads)
    # res = pool.map_async(create_dataset_for_modeling, [num_ballots_to_generate])
    # pool.close()
    # pool.join()

    # Pooling type #2:
    # with Pool(5) as p:
    #     print(p.map(create_dataset_for_modeling, [3, 4]))
