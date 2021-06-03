import pandas as pd
from sklearn.utils import resample
from sklearn.model_selection import train_test_split
from collections import Counter
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.preprocessing import StandardScaler



df = pd.read_csv("ranked-choice-voting/new_final_master.csv")
df = df.replace(np.nan, 0)

# Separate input features and target
y = df.spoiled
X = df.drop('spoiled', axis=1)
print(y.shape)
print(X.shape)
# # # setting up testing and training sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=27)

# model = LogisticRegression(solver='liblinear', random_state=0).fit(X, y)

# print(model.classes_)
# print(model.intercept_)
# print(model.coef_)
# print(model.predict_proba(X))
# print(model.predict_proba(X))

# print(model.score(X,y))

# cm = confusion_matrix(y, model.predict(X))

# fig, ax = plt.subplots(figsize=(8, 8))
# ax.imshow(cm)
# ax.grid(False)
# ax.xaxis.set(ticks=(0, 1), ticklabels=('Predicted 0s', 'Predicted 1s'))
# ax.yaxis.set(ticks=(0, 1), ticklabels=('Actual 0s', 'Actual 1s'))
# ax.set_ylim(1.5, -0.5)
# for i in range(2):
#     for j in range(2):
#         ax.text(j, i, cm[i, j], ha='center', va='center', color='red')
# plt.show()


import pandas as pd
from sklearn import datasets
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix




def evaluate_model(X_train, y_train, model):    
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    scores = cross_val_score(model, X_train, y_train, cv=3, scoring="precision")
    diff = scores.mean() - model.score(X_test, y_test)
    SD = diff / scores.std()
    
    print(f"Training Score:{model.score(X_train, y_train)}")
    print(f"Cross V Score: {scores.mean()} +/- {scores.std()}")
    print(f"Testing Score: {model.score(X_test, y_test)}")
    print(f"Cross & Test Diff: {diff}")
    print(f"Standard Deviations Away: {SD}")
    print(confusion_matrix(y_test, preds))

y = df.spoiled
X = df.drop('spoiled', axis=1)



# setting up testing and training sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=27)


# model = LogisticRegression()
model = KNeighborsClassifier(n_neighbors=3)
# model.fit(X_train_SMOTE, y_train_SMOTE)

#Oversampling on our training sets
from imblearn.over_sampling import SMOTE
smt = SMOTE(random_state=0)
X_train_SMOTE, y_train_SMOTE = smt.fit_sample(X_train, y_train)

#defining and fitting out model on smote training sets:
# model.fit(X_train_SMOTE, y_train_SMOTE)
evaluate_model(X_train_SMOTE, y_train_SMOTE, model)


# print("the model's score on training set is:", model.score(X_train_SMOTE, y_train_SMOTE))
# model.score(X_test, y_test)
# print(model.score(X_train_SMOTE, y_train_SMOTE))


# print(confusion_matrix(X_train_SMOTE, y_train_SMOTE))

# sm = SMOTE(random_state=42)

# X_res, y_res = sm.fit_resample(X_train, y_train)
# print('Resampled dataset shape %s' % Counter(y_res))


# # Modeling:
# from sklearn.linear_model import LogisticRegression
# clf = LogisticRegression(random_state=0).fit(X_train, y_train)
# print(clf.score(X_train, y_test))