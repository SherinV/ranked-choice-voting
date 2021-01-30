from itertools import permutations
import pandas as pd
import numpy as np
from datetime import datetime
import sys



def generate_all_possible_rank_combos(num_cands):
    """
    :param num_cands: number of candidates for an election
    :return: list of tuples, each tuple contains unique combination of ranks
    """
    while True:


        yield list(permutations(list(range(1,num_cands+1))))

