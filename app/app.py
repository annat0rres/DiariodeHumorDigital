from flask import Flask 
from flask import render_template, request, redirect, url_for
import mysql.connector as connection 

app = Flask (__name__)

@app.route ("/")
def conexão ():
    cnx = connection.MySQLConnection (
        user = "root",
        password = "gilovers@25",
        host = "127.0.0.1",
        database = "DiarioDeHumor"
    )

    cursor = cnx.cursor (dictionary = True)
    cursor.execute ("SELECT nome, user, email FROM usuarios")
    resultado = cursor.fetchall ()

    return render_template (banco = resultado)

@app.route ("/cadastro")
def cadastro ():
    return render_template ("cadastro.html")

@app.route ("/salvar", methods = ["POST"])
def salvar ():
    nome = request.form.get ("nome")
    user = request.form.get ("user")
    email = request.form.get ("email")
    senha = request.form.get ("senha")

    cnx = connection.MySQLConnection (
        user = "root",
        password = "gilovers@25",
        host = "127.0.0.1",
        database = "DiarioDeHumor"
    )
    cursor = cnx.cursor ()

    sql = "INSERT INTO usuarios (nome, user, email, senha) VALUES (%s, %s, %s, %s)"
    valores = (nome, user, email, senha)
    cursor.execute (sql, valores)

    cnx.commit ()
    cursor.close ()
    cnx.close ()

    return redirect (url_for ("conexão"))

if __name__ == "__main__":
    app.run (debug = True)
