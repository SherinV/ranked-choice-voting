import pandas as pd
import matplotlib as plt
from sklearn.preprocessing import MinMaxScaler
import numpy as np
  

df=pd.read_csv("ranked-choice-voting/new_final_master.csv")

# for i in range(3,9):
#     print( "for {} number of candidates".format(i), 
#     df[(df["num_candidates"]==i)].sample(n=200)["spoiled"].value_counts())

print(df['num_candidates'].plot(kind = 'bar'))

# # copy the data
# df_sklearn = df.copy()
  
# # apply normalization techniques
# column = 'Column 1'
# df_sklearn[column] = MinMaxScaler().fit_transform(np.array(df_sklearn[column]).reshape(-1,1))
  
# # view normalized data  
# display(df_sklearn)

# df['num_candidates'].plot(kind = 'bar')