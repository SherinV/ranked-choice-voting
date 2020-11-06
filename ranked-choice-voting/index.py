import sys
from generate_ballots import ballots_main
from intermediate_master import create_intermediate_master_file
from final_master_feature_extraction import feature_extraction_main
from multiprocessing import Pool
import multiprocessing
import pandas as pd

def create_dataset_for_modeling(num_ballots_to_generate):
    ballots_main(num_ballots_to_generate)
    ballot_level_features_df = create_intermediate_master_file()  # audrey's script
    election_level_features_df = feature_extraction_main()  # anxhela & sherin script

    master_df = pd.merge(election_level_features_df,
                         ballot_level_features_df[['num_candidates', 'noise', 'pyrankvote_winner', 'condorcet_winner', 'spoiled', 'filename']],
                         on='filename',
                         sort=False)

    master_df = master_df.drop_duplicates()
    master_df.to_csv('final_master.csv', index=False)


if __name__ == "__main__":
    num_ballots_to_generate = int(sys.argv[1])
    create_dataset_for_modeling(num_ballots_to_generate)

    # Pooling type #1 (seems to take longer than #2):
    # total_threads = 5
    # pool = Pool(processes=total_threads)
    # res = pool.map_async(create_dataset_for_modeling, [num_ballots_to_generate])
    # pool.close()
    # pool.join()

    # Pooling type #2:
    # with Pool(5) as p:
    #     print(p.map(create_dataset_for_modeling, [3, 4]))
