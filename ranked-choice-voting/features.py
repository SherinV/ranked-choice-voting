import ast
import json
import operator
import numpy as np
import pandas as pd


def load_data():
    df = pd.read_csv("../data/election_dict.csv")
    return df


def clean_df(df):
    cols = [col for col in df if col.startswith('Round:')] #MAIN
    for col in cols:
        df[col] =  df[col].apply(lambda x: x if pd.isnull(x) else x.strip('[]'))
        df[col]  = df[col].apply(lambda x: x if pd.isnull(x) else ast.literal_eval(x)) # convert string into tuple of string dicts
        df[col] = df[col].apply(lambda x: x if pd.isnull(x) else {k:v for t in x for k,v in t.items()}) # convert tuple of string dicts to actual dicts
    return df


def get_number_rounds(df): #Function to get number of max rounds for master_df dynamically:
    '''
    INPUT: df - dataframe
    OUTPUT: max round in data (if there is one election with 5 rounds than number_rounds=5)
    '''
    number_rounds = len([col for col in df if col.startswith("Round: ")])
    return number_rounds


# GETTING ROUND num WINNER VOTES:
def func(df, num):
    '''
    INPUT: df
           num - will be associated with following function (generate_roundwinnervotes) which will call 
           this function iteratively and generate dataframe with votes per each round and total votes for all rounds per pyrankvote winner
    OUTPUT: Number of votes pyrankwinner recieved for each round
    '''
    
    df=df[df["Round: {}".format(num)].notna()]
    
    r = [rounds for rounds in df['Round: {}'.format(num)]]
    r_clean =  [x for x in r if str(x) != 'nan']
    cands = [x for x in df['pyrankvote_winner']]
    return [r_clean [i][cands[i]] for i in range(0, len(df))]


def generate_roundwinnervotes(df, num_rounds):
    '''
    INPUT: df
           num_rounds - from get_number_rounds(df) function max round in data.
    '''
    
    for i in range(1, num_rounds + 1):
        
        df_new=df[df["Round: {}".format(i)].notna()]
        df_new['round{}winnervotes'.format(i)]=func(df, i)
        
        df["Round: {}".format(i)]=df["Round: {}".format(i)].astype(str)
        df_new["Round: {}".format(i)]=df_new["Round: {}".format(i)].astype(str)

        df_new=df_new.reindex(df.index, fill_value=0)
        df=pd.concat([df, df_new.reindex(df.index)], axis=1)
        df = df.loc[:,~df.columns.duplicated()]     
    return df


def main():
    df=load_data()
    df=clean_df(df)
    df['pyrankvote_winner'] = df['pyrankvote_winner'].apply(lambda x: x[13:-4])
    num_rounds=get_number_rounds(df)
    df=generate_roundwinnervotes(df,num_rounds)
    num_rounds = "-"+"{}".format(num_rounds) #MAIN
    df['total_votes_allrounds']= df.iloc[:, int(num_rounds):].astype(int).sum(axis=1) #MAIN
    df.to_csv("master_data_with_features.csv")
    
    
if __name__ == "__main__":
    main()
    print('hi')