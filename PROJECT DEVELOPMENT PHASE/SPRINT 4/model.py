 file=(r'C:\Users\HP\OneDrive\Documents\ML MODEL DEPLOYMENT\ML MODEL DEPLOYMENT\FLIGHTDELAYDATA.CSV')
import sys
import pandas as pd
import numpy as np
import seaborn as sns
import pickle
%matplotlib inline
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import sklearn.metrics as metrics
dataset=pd.read_csv(file)
dataset.info()
dataset.describe()
dataset.isnull().sum()
dataset['DEST'].unique()
sns.heatmap(dataset.corr())
dataset=dataset[["FL_NUM","MONTH","DAY_OF_MONTH","DAY_OF_WEEK","ORIGIN","DEST","CRS_ARR_TIME","DEP_DEL15","ARR_DEL15"]]
dataset.isnull().sum()
dataset = dataset.fillna({'ARR_DEL15':1})
dataset =dataset.fillna({'DEP_DEL15':0})
dataset.iloc[177:185]
import math
for index,row in dataset.iterrows():
  dataset.loc[index,'CRS_ARR_TIME'] = math.floor(row['CRS_ARR_TIME'])
dataset.head()
from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
dataset['DEST']=le.fit_transform(dataset['DEST'])
dataset['ORIGIN']=le.fit_transform(dataset['ORIGIN'])
dataset.head(5)
dataset =pd.get_dummies(dataset,columns=['ORIGIN','DEST'])
dataset.head()
x=dataset.iloc[:,0:8].values
y=dataset.iloc[:,8:9].values
from sklearn.preprocessing import OneHotEncoder
oh=OneHotEncoder()
z=oh.fit_transform(x[:,4:5]).toarray()
t=oh.fit_transform(x[:,5:6]).toarray()
z
t
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=0)
x_test.shape
x_train.shape
y_test.shape
y_train.shape
from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier(max_depth = 4, min_samples_split = 4, random_state = 0)
clf.fit(x_train, y_train)
pred = clf.predict(x_test)
decisiontree = clf.predict(x_test)
decisiontree
from sklearn.metrics import accuracy_score
print(accuracy_score(y_test, decisiontree))
pickle.dump(clf, open('flightclf.pkl','wb'))




