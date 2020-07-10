import pandas as pd
import numpy as np

df = pd.read_csv('./master_elections.csv')
pd.set_option('display.expand_frame_repr', False)
#df.groupby('filename').size().reset_index(name='num_of_ballots')
cols = df.columns.difference(['Unnamed: 0','num_of_ballots', 'num_of_candidates','filename'])
df['num_of_ballots'] = df.groupby(['filename'])['candidate_1'].transform('count')
df['num_of_candidates'] = df[list(['candidate_1','candidate_2','candidate_3','candidate_4','candidate_5','candidate_6'])].count(axis=1)
df = df.replace(np.nan, 'yan', regex=True)
df = df.loc[1:].astype(str).replace('0',np.nan)
df['zeros'] = df.isnull().sum(axis = 1)
df['total_num_of_zeros'] = df.groupby(['filename'])['zeros'].transform(sum)
df['num_of_ballots'] = df['num_of_ballots'].astype(str).astype(int)
df['percentage_of_noise'] =df['total_num_of_zeros']/df['num_of_ballots']
df.drop(['zeros','total_num_of_zeros'],axis =1,inplace = True)
df.to_csv('feature_engineering_Moeid.csv')
