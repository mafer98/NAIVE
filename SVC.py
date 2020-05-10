# -*- coding: utf-8 -*-
"""
Created on Thu May  7 19:12:54 2020

@author: Usuario
"""
#SVM clasificación
#sciit-learn machine learning
import json
import pyodbc as p
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split# dividimos la BD en 70 - 30
from sklearn import preprocessing 
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report#CALCULA DIFERENTES MÉTRICAS, PRECISION, F1 SCORE ETC
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC# nos permite SVM

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

X_train, X_test, Y_train, Y_test = train_test_split(x,y,test_size=0.4,random_state=56)#DIVIDO EN 70-30 DE FORMA ALEATORIA,TAMAÑO DE TEST 30%
scaler = preprocessing.StandardScaler().fit(X_train)
X_train= scaler.transform(X_train)
X_test= scaler.transform(X_test)
#clasificacion
modelo = SVC(gamma=0.00034)#CREAMOS UN modelo de SVM CON GAMMA AUTO
modelo.fit(X_train, Y_train)# entrenamiento de modelo
predicciones = modelo.predict(X_test)# predicción o clasificación
#

Acc=accuracy_score(Y_test, predicciones)
Cf=confusion_matrix(Y_test, predicciones)
json_response = json.dumps(classification_report(Y_test, predicciones),indent=2)
