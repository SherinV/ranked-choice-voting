import pandas as pd

df = pd.read_csv(r"C:\Users\anxhe\Documents\github\ranked-choice-voting\data\election_02-02-2021_13-26-40_3cands_0.03666666666666667noise.csv")

df.drop(columns=["num_candidates","noise"], inplace=True)

df.to_csv(r"C:\Users\anxhe\Documents\github\ranked-choice-voting\data\df.csv", index=False)