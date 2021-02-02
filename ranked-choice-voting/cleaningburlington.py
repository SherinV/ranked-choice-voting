import pandas as pd
import numpy as np
import pyrankvote
from pyrankvote import Candidate, Ballot

df = pd.read_csv("us_vt_btv_2009_03_mayor_normalized.csv")

kiss = Candidate('Bob Kiss')
montroll = Candidate('Andy Montroll')
wright = Candidate('Kurt Wright')
smith = Candidate('Dan Smith')
simpson = Candidate('James Simpson')

candidates = [kiss, montroll, wright, smith, simpson]

df['ballot_id_rank'] = df['ballot_id'].astype(str) + '_' + df['rank'].astype(str)

df[df.duplicated(subset='ballot_id_rank') == True]
df = df.drop_duplicates(subset='ballot_id_rank')
df1 = df.pivot(index='ballot_id', columns='rank', values='choice').rename_axis(None, axis=1).reset_index()
df1 = df1.replace(np.nan, '0')
list_of_ballot_choices = df1[[1, 2, 3, 4, 5]].values.tolist()
for x in list_of_ballot_choices:
    while '0' in x:
        x.remove('0')

df1['ballot_choices_list'] = list_of_ballot_choices
def remove_anomalies_from_ballots(ballots, value_to_remove):
    """
    ballots: series from dataframe. Each row contains a list of ranked candidates representing 1 ballot.
    value_to_remove: string that a ballot contains as a condition for its deletion
    """
    indices_to_drop = []
    
    for index, value in enumerate(ballots):
        if value_to_remove in value:
            indices_to_drop.append(index)
                   
    return indices_to_drop



write_in_indices_to_drop = remove_anomalies_from_ballots(df1['ballot_choices_list'], 'Write-in')
undervote_indices_to_drop = remove_anomalies_from_ballots(df1['ballot_choices_list'], '$UNDERVOTE')
overvote_indices_to_drop = remove_anomalies_from_ballots(df1['ballot_choices_list'], '$OVERVOTE')

indices_to_drop = write_in_indices_to_drop +  undervote_indices_to_drop + overvote_indices_to_drop


df1 = df1.drop(index=indices_to_drop)



candidates_array = []

for candidate_list in df1['ballot_choices_list']:
    ballot = []
    for candidate in candidate_list:
        candidate = candidate.strip(' ')
        ballot.append(Candidate(candidate))
    candidates_array.append(ballot)
candidates_array


df1['ballot_choices_list_with_candidate_objects'] = candidates_array

ballot_objects = []

for index,value in enumerate(df1['ballot_choices_list_with_candidate_objects']):
    ballot = Ballot(ranked_candidates=value)
    ballot_objects.append(ballot)
    
ballot_objects

df1['ballot_objects'] = ballot_objects

df1.drop(columns=["ballot_choices_list","ballot_choices_list_with_candidate_objects","ballot_objects"], inplace=True)

df1.replace('Bob Kiss', 'candidate_Bob Kiss', inplace=True)
df1.replace('Andy Montroll', 'candidate_Andy Montroll',inplace=True)
df1.replace('Kurt Wright', 'candidate_Kurt Wright',inplace=True)
df1.replace('Dan Smith', 'candidate_Dan Smith',inplace=True)
df1.replace('James Simpson', 'candidate_James Simpson',inplace=True)

df1["candidate_1"] = df1[1]
df1["candidate_2"] = df1[2]
df1["candidate_3"] = df1[3]
df1["candidate_4"] = df1[4]
df1["candidate_5"] = df1[5]

df1.drop(columns=[1,2,3,4,5, "ballot_id"], inplace=True)



df1.to_csv("../data/burlington_data.csv", index=True)
df1.to_csv("../data/burlington_data1.csv", index=True)