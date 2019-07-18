import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

dataPokemon=pd.read_csv('pokemon.csv')
dataCombat=pd.read_csv('combats.csv')
print(dataPokemon)
print(dataCombat.values[0])
print(len(dataCombat.values))

dataMatch=pd.DataFrame(columns=['HP1','Attack1','Defense1','Special Attack1','Special Defense1','Speed1','HP2','Attack2','Defense2','Special Attack2','Special Defense2','Speed2'])
j=0
for i in dataCombat.values:
    dataMatch.loc[j]=(dataPokemon[dataPokemon['#']==i[0]]['HP'].values[0],dataPokemon[dataPokemon['#']==i[0]]['Attack'].values[0],dataPokemon[dataPokemon['#']==i[0]]['Defense'].values[0],dataPokemon[dataPokemon['#']==i[0]]['Sp. Atk'].values[0],dataPokemon[dataPokemon['#']==i[0]]['Sp. Def'].values[0],dataPokemon[dataPokemon['#']==i[0]]['Speed'].values[0],dataPokemon[dataPokemon['#']==i[1]]['HP'].values[0],dataPokemon[dataPokemon['#']==i[1]]['Attack'].values[0],dataPokemon[dataPokemon['#']==i[1]]['Defense'].values[0],dataPokemon[dataPokemon['#']==i[1]]['Sp. Atk'].values[0],dataPokemon[dataPokemon['#']==i[1]]['Sp. Def'].values[0],dataPokemon[dataPokemon['#']==i[1]]['Speed'].values[0])
    j+=1
    if j==1000:
        break
    # print(dataMatch.iloc[0])
    # break

j=0
for i in dataCombat['Winner']:
    if i==dataCombat.iloc[j]['First_pokemon']:
        dataCombat.iloc[j]['Winner']=1
        j+=1
    else:
        dataCombat.iloc[j]['Winner']=0
        j+=1
target=dataCombat['Winner'].iloc[0:1000]

print(target)
print(dataMatch)
# print(np.matrix(dataMatch))

# from sklearn.linear_model import LinearRegression
# model=LinearRegression()
# model.fit(np.matrix(dataMatch),target)
# random forest

from sklearn.ensemble import RandomForestClassifier
modelRandom=RandomForestClassifier()
modelRandom.fit(np.matrix(dataMatch),target)

poke1='Pikachu'
poke2='Charizard'
indexpoke1=dataPokemon[dataPokemon['Name']==poke1]['#'].values[0]
indexpoke2=dataPokemon[dataPokemon['Name']==poke2]['#'].values[0]
statpoke=[]
statpoke.append([dataPokemon[dataPokemon['#']==indexpoke1]['HP'].values[0],dataPokemon[dataPokemon['#']==indexpoke1]['Attack'].values[0],dataPokemon[dataPokemon['#']==indexpoke1]['Defense'].values[0],dataPokemon[dataPokemon['#']==indexpoke1]['Sp. Atk'].values[0],dataPokemon[dataPokemon['#']==indexpoke1]['Sp. Def'].values[0],dataPokemon[dataPokemon['#']==indexpoke1]['Speed'].values[0],dataPokemon[dataPokemon['#']==indexpoke2]['HP'].values[0],dataPokemon[dataPokemon['#']==indexpoke2]['Attack'].values[0],dataPokemon[dataPokemon['#']==indexpoke2]['Defense'].values[0],dataPokemon[dataPokemon['#']==indexpoke2]['Sp. Atk'].values[0],dataPokemon[dataPokemon['#']==indexpoke2]['Sp. Def'].values[0],dataPokemon[dataPokemon['#']==indexpoke2]['Speed'].values[0]])
print(statpoke)

print(modelRandom.predict_proba(statpoke))
print(modelRandom.predict(statpoke))
proba=modelRandom.predict_proba(statpoke)
if proba[0][0]>=proba[0][1]:
    print(str(proba[0][0]*100)+'%',str(poke2),'Wins!')
else:
    print(str(proba[0][1]*100)+'%',str(poke2),'Wins!')

import joblib as jb
jb.dump(modelRandom,'modelPoke')