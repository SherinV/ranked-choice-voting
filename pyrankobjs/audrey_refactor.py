import os
import glob
import pandas as pd


def create_master_file_from_csvs(glob_pattern='../data/*.csv') -> pd.DataFrame():
    """
    Combine election-level csvs in data dir into
    single master dataset using a generator

    :param glob_pattern: pattern for recursive glob
    search files

    :return: master dataset as dataframe
    """

    def yielder(glob_pattern):
        for file in glob.glob(glob_pattern):
            df = pd.read_csv(file, index_col=0)
            df['filename'] = os.path.basename(file)
            yield df

    master_df = pd.concat(list(yielder(glob_pattern)))
    master_df.to_csv('master_elections.csv')
    return master_df



if __name__ == "__main__":
    master_df = create_master_file_from_csvs()
    print('hi')
