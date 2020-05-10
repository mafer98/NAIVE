# -*- coding: utf-8 -*-
"""
Created on Thu May  7 23:22:36 2020

@author: Usuario
"""

#NAIVE BAYES
import json
import pyodbc as p
import pandas as pd
from sklearn.model_selection import train_test_split# dividimos la BD en 70 - 30
from sklearn import preprocessing 
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report#CALCULA DIFERENTES MÉTRICAS, PRECISION, F1 SCORE ETC
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB

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
x=B[:,0:257]
y=B[:,-1]
m,n=x.shape
y=y.reshape((m,1))
#entrenamiento y validación
X_train, X_test, Y_train, Y_test = train_test_split(x,y,test_size=33,random_state=34)#DIVIDO EN 70-30 DE FORMA ALEATORIA,TAMAÑO DE TEST 30%
scaler = preprocessing.StandardScaler().fit(X_train)
X_train= scaler.transform(X_train)
X_test= scaler.transform(X_test)
#clasificacion N
NVB = GaussianNB()
NVB.fit(X_train, Y_train)
y_pred = NVB.predict(X_test)
#metricas
Acc=accuracy_score(Y_test, y_pred)
Cf=confusion_matrix(Y_test, y_pred)
json_response =json.dumps(classification_report(Y_test,y_pred),indent=2)