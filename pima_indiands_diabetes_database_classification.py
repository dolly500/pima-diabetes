# -*- coding: utf-8 -*-
"""Pima Indiands Diabetes Database Classification

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/#fileId=https%3A//storage.googleapis.com/kaggle-colab-exported-notebooks/pima-indiands-diabetes-database-classification-ae9f41c3-bf4e-4910-b4cc-210d5060383b.ipynb%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com/20240302/auto/storage/goog4_request%26X-Goog-Date%3D20240302T053210Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D0e3336aba28c0b5c2f56419f36a1457122f4404acfcb69c1b43ed68a7670e1ff2e1d23f14119de170425aad7e4b677a92ff5016e9cc9788934a1b4ec54bc217182891db3aee7a9cbdc76b5b5361f1f7836e7ae3e8d56c2396a4f3de46ce4a3390924947cd9c046fd7110841c3ecdfbe8bba0e480272c481f645aade8e62fe153e67dfc5b256f2138afda3eecc83182736997b650584852376ece93fe71f047d2cdd619b51abdf801b7a5bd44ba23c1f2cb2abbb5b730aa315a43900ad4787a3fbdf9d997b3a1a456e204f6730659a8c3674dcbe2e548a85f115beb47422064614ef06d5206bb15ec4e964183b4c9ff21e44f85909d44956eda04fdaa2a797909
"""

# IMPORTANT: RUN THIS CELL IN ORDER TO IMPORT YOUR KAGGLE DATA SOURCES
# TO THE CORRECT LOCATION (/kaggle/input) IN YOUR NOTEBOOK,
# THEN FEEL FREE TO DELETE THIS CELL.
# NOTE: THIS NOTEBOOK ENVIRONMENT DIFFERS FROM KAGGLE'S PYTHON
# ENVIRONMENT SO THERE MAY BE MISSING LIBRARIES USED BY YOUR
# NOTEBOOK.

import os
import sys
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from urllib.parse import unquote, urlparse
from urllib.error import HTTPError
from zipfile import ZipFile
import tarfile
import shutil

CHUNK_SIZE = 40960
DATA_SOURCE_MAPPING = 'pima-indians-diabetes-database:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F228%2F482%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240302%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240302T053210Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D907e1b7ae51f92d6bc1f30d0b54c1ae97392c5fa06503bd49e5f9a935e5edf3b11c106433bd26f461412de8be7b0c9bec4d3715fd810eacf826f31f8b35177b3b060f5af810855722ee1143cf804db51bfec87c30853b0d2790ae31721f8e0a6bfe4322342c41e556ab4323d7bd319e57dd021c3e5bcf71042f50b73764e35372909bfc18b7bef045904da17273159a1162fac2610156e2bf04a4eca3cc14174ecb1b1740fadf5b3bd23d6dee4ea0b2ad1acd7e8729a3e3a67a6fadb9655d8c69955e0306e94b837aec0abdd1e254a9d09afe632152892ca9f51fc3224f25ac2b83f659505c6d09d0a931bffdfa27520dd7bc9ace9c38ad94ad7d417704e1393'

KAGGLE_INPUT_PATH='/kaggle/input'
KAGGLE_WORKING_PATH='/kaggle/working'
KAGGLE_SYMLINK='kaggle'

!umount /kaggle/input/ 2> /dev/null
shutil.rmtree('/kaggle/input', ignore_errors=True)
os.makedirs(KAGGLE_INPUT_PATH, 0o777, exist_ok=True)
os.makedirs(KAGGLE_WORKING_PATH, 0o777, exist_ok=True)

try:
  os.symlink(KAGGLE_INPUT_PATH, os.path.join("..", 'input'), target_is_directory=True)
except FileExistsError:
  pass
try:
  os.symlink(KAGGLE_WORKING_PATH, os.path.join("..", 'working'), target_is_directory=True)
except FileExistsError:
  pass

for data_source_mapping in DATA_SOURCE_MAPPING.split(','):
    directory, download_url_encoded = data_source_mapping.split(':')
    download_url = unquote(download_url_encoded)
    filename = urlparse(download_url).path
    destination_path = os.path.join(KAGGLE_INPUT_PATH, directory)
    try:
        with urlopen(download_url) as fileres, NamedTemporaryFile() as tfile:
            total_length = fileres.headers['content-length']
            print(f'Downloading {directory}, {total_length} bytes compressed')
            dl = 0
            data = fileres.read(CHUNK_SIZE)
            while len(data) > 0:
                dl += len(data)
                tfile.write(data)
                done = int(50 * dl / int(total_length))
                sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {dl} bytes downloaded")
                sys.stdout.flush()
                data = fileres.read(CHUNK_SIZE)
            if filename.endswith('.zip'):
              with ZipFile(tfile) as zfile:
                zfile.extractall(destination_path)
            else:
              with tarfile.open(tfile.name) as tarfile:
                tarfile.extractall(destination_path)
            print(f'\nDownloaded and uncompressed: {directory}')
    except HTTPError as e:
        print(f'Failed to load (likely expired) {download_url} to path {destination_path}')
        continue
    except OSError as e:
        print(f'Failed to load {download_url} to path {destination_path}')
        continue

print('Data source import complete.')

!pip install xgboost

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from sklearn import preprocessing

# Importing Machine learning models library used for classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier as knn
from sklearn.naive_bayes import GaussianNB as GB
from sklearn.svm import SVC
import xgboost as xgb

from sklearn.metrics import confusion_matrix, accuracy_score, precision_score , recall_score
from sklearn.model_selection import GridSearchCV

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All"
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

df = pd.read_csv('/kaggle/input/pima-indians-diabetes-database/diabetes.csv')
df

df.describe().T

df.columns

df.info()

column_to_replace = ['Glucose', 'BloodPressure', 'SkinThickness', 'BMI']
df[column_to_replace] = df[column_to_replace].replace(0, np.nan)
df

df.describe().T

num_cols = 3

num_features = len(df.columns)
num_rows = (num_features + num_cols - 1) // num_cols

fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5*num_rows))
fig.subplots_adjust(hspace=0.5)

axes = axes.flatten()

for i, column in enumerate(df.columns):
    sns.histplot(df[column], kde=False, ax=axes[i])
    axes[i].set_title(f'Distribution of {column}')
    axes[i].set_xlabel(column)

for i in range(num_features, num_rows * num_cols):
    fig.delaxes(axes[i])

plt.show()

num_cols = 3

num_features = len(df.columns)
num_rows = (num_features + num_cols - 1) // num_cols

fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5*num_rows))
fig.subplots_adjust(hspace=0.5)

axes = axes.flatten()

for i, column in enumerate(df.columns):
    sns.boxplot(df[column], ax=axes[i])
    axes[i].set_title(f'Distribution of {column}')
    axes[i].set_xlabel(column)

for i in range(num_features, num_rows * num_cols):
    fig.delaxes(axes[i])

plt.show()

df.columns

def replace_outliers_zscore(df, column, n_std):
    mean = df[column].mean()
    std = df[column].std()
    lower_bound = mean - n_std * std
    upper_bound = mean + n_std * std

    df[column] = df[column].apply(lambda x: min(max(x, lower_bound), upper_bound))

def replace_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    df[column] = df[column].apply(lambda x: min(max(x, lower_bound), upper_bound))

NormalDistColumns = ['BloodPressure', 'BMI']
for col in NormalDistColumns:
    replace_outliers_zscore(df, col, 3)

NotNormalDistColumn = ['Pregnancies', 'SkinThickness', 'Insulin', 'DiabetesPedigreeFunction', 'Age']
for col in NotNormalDistColumn:
    replace_outliers_iqr(df, col)

num_cols = 3

num_features = len(df.columns)
num_rows = (num_features + num_cols - 1) // num_cols

fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5*num_rows))
fig.subplots_adjust(hspace=0.5)

axes = axes.flatten()

for i, column in enumerate(df.columns):
    sns.boxplot(df[column], ax=axes[i])
    axes[i].set_title(f'Distribution of {column}')
    axes[i].set_xlabel(column)

for i in range(num_features, num_rows * num_cols):
    fig.delaxes(axes[i])

plt.show()

df.isna().sum()

MissingNormalDistColumns = ['BloodPressure', 'BMI']
for col in MissingNormalDistColumns:
    mean = df[col].mean()
    std = df[col].std()

    nan_count = df[col].isnull().sum()

    random_values = np.random.normal(mean, std, nan_count)

    nan_index = df[col].index[df[col].isnull()]
    df.loc[nan_index, col] = random_values

MissingNotNormalDistColumns = ['Glucose', 'SkinThickness']
for col in MissingNotNormalDistColumns:
    lower_bound = df[col].min()
    upper_bound = df[col].max()

    nan_count = df[col].isnull().sum()

    random_values = np.random.uniform(lower_bound, upper_bound, nan_count)

    nan_index = df[col].index[df[col].isnull()]
    df.loc[nan_index, col] = random_values

df.isna().sum()

df

"""# Scaling"""

mm_scaler = preprocessing.MinMaxScaler()
data_scaled = pd.DataFrame(mm_scaler.fit_transform(df),columns = df.columns)

data_scaled

"""# Modeling"""

data = data_scaled.copy()

X = data.drop('Outcome' , axis = 1)
y = data['Outcome']

data['Outcome']

value_counts = y.value_counts()
print("Count of 0:", value_counts[0])
print("Count of 1:", value_counts[1])

sns.countplot(x=y)

plt.xlabel('Label')
plt.ylabel('Count')
plt.title('Countplot of Labels')

plt.show()

#Balancing target by over sampling
smote = SMOTE(k_neighbors = 10)
X, y = smote.fit_resample(X, y)

value_counts = y.value_counts()
print("Count of 0:", value_counts[0])
print("Count of 1:", value_counts[1])

sns.countplot(x=y)

plt.xlabel('Label')
plt.ylabel('Count')
plt.title('Countplot of Labels')

plt.show()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

#def func for multiple modleing

def Cls_model_GrdSrch_Tune(model, Data, X, y, params):

    clf = GridSearchCV(model, params, scoring ='accuracy', cv = 5)
    clf.fit(X, y)

    print("best score is :" , clf.best_score_)
    print("best estimator is :" , clf.best_estimator_)
    print("best Params is :" , clf.best_params_)

    return (clf.best_score_)

models_lables = ["RandomForestClassifier","Gaussian Naive Bays","KNN","Logistic_Regression","Support_Vector"]
models = [RandomForestClassifier(),GB(),knn(),LogisticRegression(),SVC()]
Model_Accuracy_default = []

for models_lable, model in zip(models_lables, models):
    print('*****************************************')
    print(models_lable)
    Accuracy = Cls_model_GrdSrch_Tune(model, data, X_train, y_train, {})
    Model_Accuracy_default.append(Accuracy)

AccuracyList_default = pd.DataFrame({
     "Classification Model" :models,
     "Accuracy":Model_Accuracy_default
    })
AccuracyList_default.sort_values( by = 'Accuracy' , ascending = False)

models_lables = ["RandomForestClassifier","Gaussian Naive Bays","KNN","Logistic_Regression","Support_Vector"]

models = [RandomForestClassifier(),GB(),knn(),LogisticRegression(),SVC()]

params_RFC = {
                'n_estimators': [5, 10, 15, 19, 20, 21, 25, 30, 35, 40],
                'min_samples_split': [2, 3, 4, 5, 6],
                'criterion' : ["gini", "entropy"]
            }
params_GB = {

            }
params_KNN = {
               'n_neighbors':[3, 4, 5, 10, 15, 20],
               'weights':('uniform','distance'),
               'p':[1,5]
             }
params_LR = {
             'C': [0.01,0.1,1,10],'penalty':('l1','l2'),
             'penalty': ('l1', 'l2', 'elasticnet')
            }
params_SVC = {

              'C': [0.1, 1, 10, 20, 100],
              'gamma': [1, 0.1, 0.01, 0.001, 0.0001,10],
              'kernel': ['rbf']
             }

params = [params_RFC, params_GB, params_KNN, params_LR, params_SVC]

Model_Accuracy_tunned = []

# lst = zip(models_lables, models, params)
# list(lst)

for models_lable, model, param in zip(models_lables, models, params):
    print('*****************************************')
    print(models_lable)

    Accuracy = Cls_model_GrdSrch_Tune(model, data, X_train, y_train, param)
    Model_Accuracy_tunned.append(Accuracy)

AccuracyList_tunned = pd.DataFrame({
     "Classification Model" :models,
     "Accuracy":Model_Accuracy_tunned
    })
AccuracyList_tunned.sort_values( by = 'Accuracy' , ascending = False)

AccuracyList_final = pd.DataFrame({
     "Classification Model" :models,
     "Accuracy_with_default_config":Model_Accuracy_default,
     "Accuracy_with_tunned_params": Model_Accuracy_tunned
    })
AccuracyList_final.sort_values(by = 'Accuracy_with_tunned_params' , ascending = False)

params = {'n_estimators' : [40],
          'min_samples_split' : [2],
          'criterion': ["gini"]
         }
BestModel = RandomForestClassifier(n_estimators= 40, min_samples_split= 2, criterion = 'gini')
BestModel.fit(X_train, y_train)
y_predicted = BestModel.predict(X_test)

conf_matrix = confusion_matrix(y_test, y_predicted)

acc_score = accuracy_score(y_test, y_predicted)
pre_score = precision_score(y_test, y_predicted)
re_score = recall_score(y_test, y_predicted)

print('accuracy_score : ', acc_score)
print('precision_score : ', pre_score)
print('recall_score : ', re_score, '\n')

print('Accuracy of RandomForestClassifier is: ', acc_score * 100)
print('Precision of RandomForestClassifier is: ', pre_score * 100)
print('Recall of KRandomForestClassifier is: ', re_score * 100, '\n')

print('Confusion_Matrix : ',"\n" , conf_matrix,  '\n')

