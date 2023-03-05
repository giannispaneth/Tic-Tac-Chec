# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 20:09:26 2021

@author: John
"""
import random
import csv
import operator


from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression

import os
from sklearn.preprocessing import PolynomialFeatures


import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error, r2_score, roc_auc_score
import numpy as np

csv_reader = pd.read_csv('C:/Users/John/Desktop/testpiecevalues2.csv')
file=csv_reader.values.tolist()

values=[]
win=[]
i1=0
i2=0
for i in range(0,len(file),1):
    if file[i][13]!="overload":
        values.append(file[i][:13])
        
    if file[i][13]=="Win black":
        win.append(0)
        i1=i1+1
    elif file[i][13]=="Win white":
        win.append(1)
        i2=i2+2

randomForest=RandomForestClassifier(n_estimators=200,random_state=None,max_features=4)
randomForest.fit(values[:len(values)-500],win[:len(values)-500])
pred=randomForest.predict((values[(len(values)-500):len(values)]))
outcome=win[(len(values)-500):len(values)]
outcome=np.array(outcome)
pred=np.array(pred)
pred=pred.reshape(-1, 1)
a1=randomForest.score(values[(len(values)-500):len(values)],outcome)
outcome=outcome.reshape(-1,500)
outcome=outcome.transpose()
a2=roc_auc_score(outcome,randomForest.predict_proba(values[(len(values)-500):len(values)])[:,1])