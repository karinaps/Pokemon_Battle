import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

dfPokemon=pd.read_csv('pokemon.csv')
dfCombat=pd.read_csv('combats.csv')
# print(dfPokemon)
# print(dfCombat.values[0])
# print(len(dfCombat.values))

data_match=pd.DataFrame(columns=[
    'HP1','Attack1','Defense1','Special Attack1',
    'Special Defense1','Speed1','HP2','Attack2',
    'Defense2','Special Attack2','Special Defense2','Speed2']
)
j=0
for i in dfCombat.values:
    data_match.loc[j]=(
        dfPokemon[dfPokemon['#']==i[0]]['HP'].values[0],
        dfPokemon[dfPokemon['#']==i[0]]['Attack'].values[0],
        dfPokemon[dfPokemon['#']==i[0]]['Defense'].values[0],
        dfPokemon[dfPokemon['#']==i[0]]['Sp. Atk'].values[0],
        dfPokemon[dfPokemon['#']==i[0]]['Sp. Def'].values[0],
        dfPokemon[dfPokemon['#']==i[0]]['Speed'].values[0],
        dfPokemon[dfPokemon['#']==i[1]]['HP'].values[0],
        dfPokemon[dfPokemon['#']==i[1]]['Attack'].values[0],
        dfPokemon[dfPokemon['#']==i[1]]['Defense'].values[0],
        dfPokemon[dfPokemon['#']==i[1]]['Sp. Atk'].values[0],
        dfPokemon[dfPokemon['#']==i[1]]['Sp. Def'].values[0],
        dfPokemon[dfPokemon['#']==i[1]]['Speed'].values[0])
    j+=1
    if j==1000:
        break
    # print(data_match.iloc[0])
    # break

j=0
for i in dfCombat['Winner']:
    if i==dfCombat.iloc[j]['First_pokemon']:
        dfCombat.iloc[j]['Winner']=1
        j+=1
    else:
        dfCombat.iloc[j]['Winner']=0
        j+=1
target=dfCombat['Winner'].iloc[0:1000]

# print(target)
# print(data_match)
# print(np.matrix(data_match))

dfx = np.matrix(data_match)
dfy = target

#=============================================================== MODEL MACHINE LEARNING ========================================================================================================================================

from sklearn.ensemble import RandomForestClassifier
modelRandom=RandomForestClassifier()
modelRandom.fit(dfx,dfy)

poke1='Pikachu'
poke2='Charizard'
indexpoke1=dfPokemon[dfPokemon['Name']==poke1]['#'].values[0]
indexpoke2=dfPokemon[dfPokemon['Name']==poke2]['#'].values[0]

statpoke=[]
statpoke.append([
    dfPokemon[dfPokemon['#']==indexpoke1]['HP'].values[0],
    dfPokemon[dfPokemon['#']==indexpoke1]['Attack'].values[0],
    dfPokemon[dfPokemon['#']==indexpoke1]['Defense'].values[0],
    dfPokemon[dfPokemon['#']==indexpoke1]['Sp. Atk'].values[0],
    dfPokemon[dfPokemon['#']==indexpoke1]['Sp. Def'].values[0],
    dfPokemon[dfPokemon['#']==indexpoke1]['Speed'].values[0],
    dfPokemon[dfPokemon['#']==indexpoke2]['HP'].values[0],
    dfPokemon[dfPokemon['#']==indexpoke2]['Attack'].values[0],
    dfPokemon[dfPokemon['#']==indexpoke2]['Defense'].values[0],
    dfPokemon[dfPokemon['#']==indexpoke2]['Sp. Atk'].values[0],
    dfPokemon[dfPokemon['#']==indexpoke2]['Sp. Def'].values[0],
    dfPokemon[dfPokemon['#']==indexpoke2]['Speed'].values[0]])
# print(statpoke)

print(modelRandom.predict_proba(statpoke))
print(modelRandom.predict(statpoke))
proba=modelRandom.predict_proba(statpoke)

if proba[0][0]>=proba[0][1]:
    print(str(proba[0][0]*100)+'%',str(poke2),'Wins!')
else:
    print(str(proba[0][1]*100)+'%',str(poke2),'Wins!')

import joblib as jb
jb.dump(modelRandom,'modelPokemon')