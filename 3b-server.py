import numpy as np
import pandas as pd
from flask import redirect, request, Flask, render_template, send_from_directory
import json, requests
import joblib as jb
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['upload_folder']='album'

# HOME ROUTE =====================================================================================================================
@app.route('/')
def home():
    return render_template('1ujian.html')

# HASIL & UPLOAD ROUTE ==============================================================================================================================

@app.route('/hasil', methods=['POST'])
def post():
    poke1=request.form['namapokemon1'].lower()
    poke2=request.form['namapokemon2'].lower()
    
    url1='https://pokeapi.co/api/v2/pokemon/'+poke1
    url2='https://pokeapi.co/api/v2/pokemon/'+poke2
    
    pokemon1 = requests.get(url1)
    pokemon2 = requests.get(url2)
    
    if str(pokemon1)=='<Response [404]>' or str(pokemon2)=='<Response [404]>':
        return redirect('/NotFound')

    name1 = pokemon1.json()['name']
    upper1 = name1[0].upper()
    nama1 = upper1 + name1[1:]
    
    name2 = pokemon2.json()['name']
    upper2 = name2[0].upper()
    nama2 = upper2 + name2[1:]
    
    dfPokemon = pd.read_csv('pokemon.csv')
    # dfCombat = pd.read_csv('combats.csv')
    indexpoke1 = dfPokemon[dfPokemon['Name']==nama1]['#'].values[0]
    indexpoke2 = dfPokemon[dfPokemon['Name']==nama2]['#'].values[0]
    
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
    
    model = jb.load('modelPokemon')
    proba=model.predict_proba(statpoke)
    if proba[0][0]>=proba[0][1]:
        win = str(proba[0][0]*100)+'%'+' '+str(nama2)+' '+'Wins!'
    else:
        win = str(proba[0][1]*100)+'%'+' '+str(nama1)+' '+'Wins!'
        
    poke=[nama1,nama2]
    pokehp=[dfPokemon[dfPokemon['#']==indexpoke1]['HP'].values[0],dfPokemon[dfPokemon['#']==indexpoke2]['HP'].values[0]]
    pokeatk=[dfPokemon[dfPokemon['#']==indexpoke1]['Attack'].values[0],dfPokemon[dfPokemon['#']==indexpoke2]['Attack'].values[0]]
    pokedef=[dfPokemon[dfPokemon['#']==indexpoke1]['Defense'].values[0],dfPokemon[dfPokemon['#']==indexpoke2]['Defense'].values[0]]
    pokespatk=[dfPokemon[dfPokemon['#']==indexpoke1]['Sp. Atk'].values[0],dfPokemon[dfPokemon['#']==indexpoke2]['Sp. Atk'].values[0]]
    pokespdef=[dfPokemon[dfPokemon['#']==indexpoke1]['Sp. Def'].values[0],dfPokemon[dfPokemon['#']==indexpoke2]['Sp. Def'].values[0]]
    pokespd=[dfPokemon[dfPokemon['#']==indexpoke1]['Speed'].values[0],dfPokemon[dfPokemon['#']==indexpoke2]['Speed'].values[0]]

    # plotting to figures
    # fig = plt.figure(figsize=(13,9))
    plt.subplot(161)
    plt.bar(poke,pokehp,color=['lightblue','lightgreen'])
    plt.title('HP')
    i=0

    while i<len(poke):
        plt.text(poke[i],pokehp[i]-4,f'''{pokehp[i]}''',fontsize=17)
        i+=1

    plt.subplot(162)
    plt.bar(poke,pokeatk,color=['lightblue','lightgreen'])
    plt.title('Attack')
    i=0
    while i<len(poke):
        plt.text(poke[i],pokeatk[i]-4,f'''{pokeatk[i]}''',fontsize=17)
        i+=1

    plt.subplot(163)
    plt.bar(poke,pokedef,color=['lightblue','lightgreen'])
    plt.title('Defense')
    i=0
    while i<len(poke):
        plt.text(poke[i],pokedef[i]-4,f'''{pokedef[i]}''',fontsize=17)
        i+=1

    plt.subplot(164)
    plt.bar(poke,pokespatk,color=['lightblue','lightgreen'])
    plt.title('Special Attack')
    i=0
    while i<len(poke):
        plt.text(poke[i],pokespatk[i]-4,f'''{pokespatk[i]}''',fontsize=17)
        i+=1

    plt.subplot(165)
    plt.bar(poke,pokespdef,color=['lightblue','lightgreen'])
    plt.title('Special Defense')
    i=0
    while i<len(poke):
        plt.text(poke[i],pokespdef[i]-4,f'''{pokespdef[i]}''',fontsize=17)
        i+=1

    plt.subplot(166)
    plt.bar(poke,pokespd,color=['lightblue','lightgreen'])
    plt.title('Speed')
    i=0
    while i<len(poke):
        plt.text(poke[i],pokespd[i]-4,f'''{pokespd[i]}''',fontsize=17)
        i+=1

    addressgrafik='./album/'+nama1+'vs'+nama2+'.png'
    urlgrafik='http://localhost:5000/fileupload/'+nama1+'vs'+nama2+'.png'
    plt.savefig(addressgrafik)
    grafik=urlgrafik
    
    filegmb1 = pokemon1.json()['sprites']
    gmb1 = filegmb1['front_default']

    filegmb2 = pokemon2.json()['sprites']
    gmb2 = filegmb2['front_default']

    files = [nama1, nama2, gmb1, gmb2, win, grafik]
    return render_template('2ujian.html',x=files)

@app.route('/fileupload/<path:x>')
def hasilUpload(x):
    return send_from_directory('storage',x)

# ERROR & NOT FOUND ROUTE ========================================================================================================================================

@app.route('/NotFound')
def notFound():
    return render_template('errorujian.html')

@app.errorhandler(404)
def notFound404(error):
    return render_template('errorujian.html')

# ACTIVATE SERVER =================================================================================================================================================

if __name__=='__main__':
    app.run(debug=True)