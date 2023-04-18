from flask import Flask, render_template, request
app = Flask(__name__)

import pandas 
import matplotlib.pyplot as plt
import os
df = pandas.read_excel("https://github.com/wtitze/3E/blob/main/BikeStores.xls?raw=true", sheet_name="customers")

@app.route('/')
def home():
    li = list(set(df["city"]))
    li.sort()
    return render_template('home.html', lista = li)

@app.route('/nomeCognome', methods = ["GET"])
def nomeCognome():
    nome = request.args.get("nome")
    cognome = request.args.get("cognome")
    table = df[(df["first_name"] == nome.capitalize()) & (df["last_name"] == cognome.capitalize())].to_html()
    return render_template('risultato.html', tabella = table)

@app.route('/citta/<cittadina>', methods = ["GET"])
def citta(cittadina):
    table = df[df["city"] == cittadina].to_html()
    return render_template('risultato.html', tabella = table)

@app.route('/gruppo')
def gruppo():
    table = df.groupby("state").count()[["first_name"]].sort_values(by="first_name").reset_index().to_html()
    return render_template('risultato.html', tabella = table)

@app.route('/grande')
def grande():
    d = df.groupby("state").count()[["first_name"]].sort_values(by="first_name").reset_index()
    table = d[d["first_name"] == d["first_name"].max()][["state"]].to_html()
    return render_template('risultato.html', tabella = table)

@app.route('/grafici')
def grafici():
    d = df.groupby("state").count()[["first_name"]].sort_values(by="first_name").reset_index()
    stringhe = d["state"]
    dati = d["first_name"]

    fig, ax = plt.subplots(figsize=(10,7))
    ax.bar(stringhe, dati, label='numero di clienti')
    ax.set_title("numero di clienti per ogni stato")
    ax.set_xlabel("stati")
    ax.set_ylabel("numero clienti")
    plt.subplots_adjust(bottom=0.25)
    dir = "static/images"
    file_name = "graf.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)

    fig, axx = plt.subplots(figsize=(10,7))
    axx.barh(stringhe, dati, label='numero di clienti')
    axx.set_title("numero di clienti per ogni stato")
    axx.set_xlabel("numero clienti")
    axx.set_ylabel("sati")
    plt.subplots_adjust(bottom=0.25)
    dir = "static/images"
    file_name = "graf2.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)

    plt.figure(figsize=(16, 8))
    plt.pie(dati, labels=stringhe, autopct='%1.1f%%')
    dir = "static/images"
    file_name = "graf3.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template('grafici.html')

@app.route('/nulla')
def nulla():
    table = df[df['email'].isnull()][["first_name", "last_name", "phone"]].to_html()
    return render_template('risultato.html', tabella = table)

@app.route('/email')
def email():
    provider = request.args.get("provider")
    table = df[df["email"].str.contains(provider, na = False)][["first_name", "last_name"]].to_html()
    return render_template('risultato.html', tabella = table)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)