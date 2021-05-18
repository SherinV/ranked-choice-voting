import pandas as pd
from sklearn.utils import resample
from sklearn.model_selection import train_test_split
import numpy 
from collections import Counter
from sklearn.datasets import make_classification
from imblearn.over_sampling import SMOTE

df = pd.read_csv("ranked-choice-voting/new_final_master.csv")


# Separate input features and target
y = df.spoiled
X = df.drop('spoiled', axis=1)

# setting up testing and training sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=27)


sm = SMOTE(random_state=42)


X_res, y_res = sm.fit_resample(X, y)
print('Resampled dataset shape %s' % Counter(y_res))


#Modeling:
from sklearn.linear_model import LogisticRegression
clf = LogisticRegression(random_state=0).fit(X_res, y_res)
print(clf.score(X_res, y_res))