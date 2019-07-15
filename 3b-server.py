from flask import redirect, request, Flask, render_template, url_for
import json, requests
import pandas as pd
import joblib

app=Flask(__name__)

# HOME ROUTE =====================================================================================================================

@app.route('/')
def home():
    return render_template('1ujian.html')


# HASIL ROUTE ==============================================================================================================================
@app.route('/hasil', methods=['POST','GET'])
def post():
    model=joblib.load('modeljoblib')

    poke1=request.form['namapokemon1']
    poke2=request.form['namapokemon2']
    poke1=poke1.lower() #nama
    poke2=poke2.lower() #nama

    datapokemon=pd.read_csv('pokemon.csv')
    idpoke1=(datapokemon[datapokemon['Name']==poke1.title()].index.values[0])+1
    idpoke2=(datapokemon[datapokemon['Name']==poke2.title()].index.values[0])+1

    url1='https://pokeapi.co/api/v2/pokemon/'+poke1
    url2='https://pokeapi.co/api/v2/pokemon/'+poke2
    data1=requests.get(url1)
    data2=requests.get(url2)

    if str(data1)=='<Response [404]>':
        return redirect(url_for('notfound'))
    if str(data2)=='<Response [404]>':
        return redirect(url_for('notfound'))

    gambar1=data1.json()['sprites']['front_default']
    gambar2=data2.json()['sprites']['front_default']

# =============================================== from pokemon.csv
    dfpoke=pd.read_csv('pokemon.csv',index_col=0)

    hp1=dfpoke.loc[idpoke1]['HP']
    hp2=dfpoke.loc[idpoke2]['HP']
    attack1=dfpoke.loc[idpoke1]['Attack']
    attack2=dfpoke.loc[idpoke2]['Attack']
    defense1=dfpoke.loc[idpoke1]['Defense']
    defense2=dfpoke.loc[idpoke2]['Defense']
    spatk1=dfpoke.loc[idpoke1]['Sp. Atk']
    spatk2=dfpoke.loc[idpoke2]['Sp. Atk']
    spdef1=dfpoke.loc[idpoke1]['Sp. Def']
    spdef2=dfpoke.loc[idpoke2]['Sp. Def']
    speed1=dfpoke.loc[idpoke1]['Speed']
    speed2=dfpoke.loc[idpoke2]['Speed']

    predict=model.predict([[hp1,hp2,attack1,attack2,defense1,defense2,spatk1,spatk2,spdef1,spdef2,speed1,speed2]])[0]
    if predict==0:
        winner=poke1.title()
    else:
        winner=poke2.title()

    proba=model.predict_proba([[hp1,hp2,attack1,attack2,defense1,defense2,spatk1,spatk2,spdef1,spdef2,speed1,speed2]])
    probamax=round(proba[0,predict]*100)

    return render_template('2ujian.html',nama1=poke1.title(),nama2=poke2.title(),gambar1=gambar1,gambar2=gambar2,winner=winner,proba=probamax)


# ERROR & NOT FOUND ROUTE ========================================================================================================================================

@app.route('/notFound')
def notfound():
    return render_template('errorujian.html')

@app.errorhandler(404)
def notFound404(error):
    return render_template('errorujian.html')

# ACTIVATE SERVER =================================================================================================================================================

if __name__=='__main__':
    app.run(debug=True)