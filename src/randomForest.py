# %% imports
# import pandas as pd
import modin.pandas as pd
import numpy as np
import sklearn as sk
from sklearn.linear_model import Perceptron
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
import timeit

# %% crate label dataframe, NAMES and NUMBER
labelstxt = pd.read_csv(
    filepath_or_buffer="./HAPT Data Set/activity_labels.txt", names=['label'])

labels = pd.DataFrame(columns=['labels', 'numbers'])
labels['labels'] = labelstxt['label'].apply(
    lambda x: [str(x).strip(' 123456789')])
labels['numbers'] = labelstxt['label'].apply(
    lambda x: [str(x).strip('ABCDEFGHIJKLMNOPQRSTUVWXYZ_ ')])
print(labels)

# %% create data frames
df_features_info = pd.read_csv(
    filepath_or_buffer='./HAPT Data Set/features.txt', names=['features'])
listfeatures = df_features_info['features']

df_train = pd.read_csv(
    filepath_or_buffer='./HAPT Data Set/Train/X_train.txt', sep=' ', names=listfeatures)
df_train_labels = pd.read_csv(
    filepath_or_buffer='./HAPT Data Set/Train/y_train.txt', names=['label'])
df_test = pd.read_csv(
    filepath_or_buffer='./HAPT Data Set/Test/X_test.txt', sep=' ', names=listfeatures)
df_test_labels = pd.read_csv(
    filepath_or_buffer='./HAPT Data Set/Test/y_test.txt', names=['label'])

print("df_train shape: " + str(df_train.shape))
print("df_test shape: " + str(df_test.shape))

# %% Preprocess the X data by scaling
sc = StandardScaler()
sc.fit(df_train)
x_train_std = sc.transform(df_train)
x_test_std = sc.transform(df_test)


# %% 
rand_f = RandomForestClassifier(n_estimators=50)
rand_f.fit(x_train_std, df_train_labels['label'])
rand_f_predict = rand_f.predict(x_test_std)

print("accuracy: %.4f" % accuracy_score(
    df_test_labels['label'], rand_f_predict))

# %% predict with random forest

accuracyList = []

for i in range(1,50,1):
    rand_f = RandomForestClassifier(n_estimators=i)
    rand_f.fit(x_train_std, df_train_labels['label'])
    rand_f_predict = rand_f.predict(x_test_std)
    accuracyList.append(rand_f_predict)

print(accuracyList)

# print("accuracy: %.4f" % accuracy_score(df_test_labels['label'], rand_f_predict))

#%%
