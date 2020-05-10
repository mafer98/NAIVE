import logging
import azure.functions as func
import pyodbc #CONECTAR CON DB DE TIPO SQL
import pandas as pd
import json #INTERCAMBIO DE DATOS DENTRO LA MISMA RED
import uuid #CREAR VALOR ALFANUMERICO DE 12 DIGITOS
import os 
from sklearn import neighbors,datasets, preprocessing
from sklearn.model_selection import train_test_split 
from sklearn.metrics import accuracy_score 
from sklearn.metrics import classification_report 


def main(req: func.HttpRequest) -> func.HttpResponse:
    req_body = req.get_json()
    variable1 = req_body.get('variable1')#ALMACENAR EN VARIABLE 1 
    logging.info(variable1)

    conn=pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                'SERVER=svd1.database.windows.net;'
                'DATABASE=azurem;'
                'UID=azurem;'
                'PWD=sensores2020*;'
                'Trusted_Connection=no;')
    cursor=conn.cursor()
    
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
    #A=accuracy_score(y_test, y_pred)
    json_response =json.dumps(classification_report(y_test,y_pred),indent=2)
   
    if variable1 < 10:
        return func.HttpResponse(json_response)
    else:
        return func.HttpResponse("NUBE Puede que se ingresara in valor mal en el postman pero la funcion se ejecuto meleramente",status_code=200)