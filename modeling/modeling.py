from operator import index
import sklearn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score

np.random.seed(53)

hat_data = pd.read_csv("data_sheet.csv", header=0)

hat_names = hat_data["name"]
hat_data = hat_data.drop(columns=["id", "name"])

#hat_data.sort_values(by="price", inplace=True, ascending=True)

#encoding
one_hot_effect = pd.get_dummies(hat_data["effect"])
hat_data = hat_data.drop("effect", axis = 1)
hat_data = hat_data.join(one_hot_effect)

one_hot_quality = pd.get_dummies(hat_data["quality"])
hat_data = hat_data.drop("quality", axis = 1)
hat_data = hat_data.join(one_hot_quality)

hat_data = hat_data.rename(columns={6 : "unique", 0 : "normal", 3 : "vintage", 1 : "genuine", 5 : "unusual", 11 : "strange", 13 : "haunted", 14 : "collector's"})

def split_train_test(data, test_ratio):
    shuffled_indices = np.random.permutation(len(data))
    test_set_size = int(len(data) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    return data.iloc[train_indices], data.iloc[test_indices]

train_set, test_set = split_train_test(hat_data, 0.2)

#pipeline
num_pipeline = Pipeline([
    ('std_scaler', StandardScaler())
])

full_pipeline = ColumnTransformer([
    ("num", num_pipeline, ["exist"])],
    remainder="passthrough"
)

train_set_labels = train_set["price"]
train_set = train_set.drop("price", axis=1)

#print(train_set_labels)
#print(train_set)

train_set_tr = full_pipeline.fit_transform(train_set)
#print(train_set_tr[0])

forest_reg = RandomForestRegressor()
forest_reg.fit(train_set_tr, train_set_labels)



test_set_labels = test_set["price"]
test_set = test_set.drop("price", axis=1)

#print(len(train_set))
#print(len(test_set))

some_test = test_set.iloc[0:25]
some_labels = test_set_labels.iloc[0:25]

some_test_tr = full_pipeline.fit_transform(some_test)


predictions = forest_reg.predict(some_test_tr)
labels = list(some_labels)

#names

print(some_test)

print("#, Prediction, Label")
for i in range(len(predictions)):
    print(i, round(predictions[i], 2), ", ", round(labels[i], 2))



def display_scores(scores):
    print("Scores:", scores)
    print("Mean:", scores.mean())
    print("St Dev:", scores.std())

#scores = cross_val_score(forest_reg, train_set_tr, train_set_labels, scoring="neg_mean_squared_error", cv=10)
#rmse_scores = np.sqrt(-scores)

#display_scores(rmse_scores)

#print(train_set_tr)

#print(train_set)
#print(test_set)



#print(hat_data)
#plt.show()