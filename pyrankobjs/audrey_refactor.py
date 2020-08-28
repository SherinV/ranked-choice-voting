import os
import glob
from typing import List
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
    master_df.to_csv('./master_elections.csv', index=False)
    return master_df


def get_cands_into_single_cell(df: pd.DataFrame()) -> List[str]:
    """
    Per election within master dataframe, take
    all candidates and put them in one cell, separating
    them with commas

    :param df: master dataset

    :return: list of concatenated candidates
        per election within master dataset
        that you can then use to set a new
        column in master dataset called
        "candidate_list"
    """
    concat_cands = []
    for name, group in df.groupby('filename'):
        group = group.dropna(axis=1, how='all')
        cand_cols = [col for col in group if col.startswith('candidate_')]
        group[cand_cols] = group[cand_cols].astype('str')
        group['cands'] = group[cand_cols].agg(", ".join, axis=1)
        concat_cands.extend(group['cands'].values)
    return concat_cands


if __name__ == "__main__":
    master_df = create_master_file_from_csvs()
    # master_df = pd.read_csv('./master_elections.csv')  # tmp
    master_df['candidate_list'] = get_cands_into_single_cell(master_df)
