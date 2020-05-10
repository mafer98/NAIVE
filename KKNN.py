# -*- coding: utf-8 -*-
"""
Created on Fri May  8 19:26:19 2020

@author: Acer
"""

from sklearn import neighbors,datasets, preprocessing
from sklearn.model_selection import train_test_split 
from sklearn.metrics import accuracy_score 
import pandas as pd 
import pyodbc as p
import json
from sklearn.metrics import classification_report 

#Base=pd.read_excel('features.xlsx')
#B=Base.to_numpy()

#X=B[:,0:511]
#y=B[:,512]
conn=p.connect('Driver={ODBC Driver 17 for SQL Server};'
                'SERVER=svd1.database.windows.net;'
                'DATABASE=azurem;'
                'UID=azurem;'
                'PWD=sensores2020*;'
                'Trusted_Connection=no;')
cursor=conn.cursor()

#cursor.execute("select *from azurem.dbo.matrizD")
g=pd.read_sql_query("select *from azurem.dbo.matrizD",con=conn)
conn.commit()
B=g.to_numpy()
X=B[:,0:257]
y=B[:,-1]
m,n=X.shape
y=y.reshape((m,1))
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=55) 
scaler = preprocessing.StandardScaler().fit(X_train) 
X_train = scaler.transform(X_train) 
X_test = scaler.transform(X_test)  
knn = neighbors.KNeighborsClassifier(n_neighbors=5) 
knn.fit(X_train, y_train) 
y_pred = knn.predict(X_test) 
A=accuracy_score(y_test, y_pred)
json_response =json.dumps(classification_report(y_test,y_pred),indent=2)

