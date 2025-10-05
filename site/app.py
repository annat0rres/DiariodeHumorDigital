from flask import Flask 
from flask import render_template, request, redirect, url_for, session, flash
import mysql.connector as connection 

app = Flask (__name__)
app.secret_key = ""
#Colocar a secret key aqui

@app.route ("/")
def inicio ():
    return render_template ("inicio.html")

@app.route ("/cadastro")
def cadastro ():
    return render_template ("cadastro.html")

@app.route ("/salvar", methods = ["POST"])
def salvar ():
    name = request.form.get ("name")
    username = request.form.get ("username")
    email = request.form.get ("email")
    password = request.form.get ("password")

    cnx = connection.MySQLConnection (
        user = "",
        password = "",
        host = "127.0.0.1",
        database = "DiarioDeHumor"
    )
    cursor = cnx.cursor ()
    #Colocar o user e password do banco de dados aqui, criar o usuário caso não exista e baixar e importar o banco de dados no mysql


    sql = "INSERT INTO usuarios (name, username, email, password) VALUES (%s, %s, %s, %s)"
    valores = (name, username, email, password)
    cursor.execute (sql, valores)

    cnx.commit ()
    cursor.close ()
    cnx.close ()

    return redirect (url_for ("inicio"))

@app.route ("/login")
def login ():
    return render_template ("login.html")

@app.route("/entrar", methods=["POST"])
def entrar():
    username = request.form.get("username")
    password = request.form.get("password")

    cnx = connection.MySQLConnection(
        user="",
        password="",
        host="127.0.0.1",
        database="DiarioDeHumor"
    )
    cursor = cnx.cursor(dictionary=True)
    #Colocar o user e password do banco de dados aqui também

    sql = "SELECT * FROM usuarios WHERE username = %s AND password = %s"
    valores = (username, password)
    cursor.execute(sql, valores)
    resultado = cursor.fetchone()

    cursor.close()
    cnx.close()

    if resultado:  
        session["usuario"] = resultado["username"]  
        flash("Login realizado com sucesso!")
        return redirect(url_for("inicio"))
    else:
        flash("Usuário ou senha incorretos!")
        return redirect(url_for("login"))

if __name__ == "__main__":
    app.run (debug = True)
