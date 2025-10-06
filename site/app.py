from flask import Flask 
from flask import render_template, request, redirect, url_for, session, flash
import mysql.connector as connection 

app = Flask (__name__)
app.secret_key = "segredo123"
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
        user = "root",
        password = "gilovers@25",
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

@app.route ("/principal")
def principal ():
    if "usuario" in session:
        name = session ["name"]
        username = session ["username"]
        return render_template("principal.html", name=name, username=username)
    
    else:
        flash ("Faça login primeiro!")
        return redirect (url_for("login"))

@app.route ("/perfil")
def perfil ():
    if "username" not in session:
        flash ("Faça login primeiro!")
        return redirect (url_for ("login"))
    
    username = session ["username"]

    cnx = connection.MySQLConnection (
        user = "root",
        password = "gilovers@25",
        host = "127.0.0.1",
        database = "DiarioDeHumor"
    )

    cursor = cnx.cursor (dictionary=True)
    cursor.execute ("SELECT * FROM usuarios WHERE username = %s", (username,))
    user = cursor.fetchone ()
    cursor.close ()
    cnx.close ()

    return render_template (
        "perfil.html", 
        name = user ["name"],
        username = user ["username"],
        email = user ["email"]
    )

@app.route ("/atualizar_perfil", methods= ["POST"])
def atualizar_perfil ():
    if "username" not in session:
        flash ("Faça login para alterar o perfil.")
        return redirect (url_for("login"))
    
    username_atual = session ["username"]

    name = request.form.get ("name")
    username_novo = request.form.get ("username")
    email = request.form.get ("email")
    password = request.form.get ("password")

    cnx = connection.MySQLConnection (
        user = "root",
        password = "gilovers@25",
        host = "127.0.0.1",
        database = "DiarioDeHumor"
    )
    cursor = cnx.cursor ()

    sql ="""UPDATE usuarios
            SET name = %s, username = %s, email = %s, password = %s
            WHERE username = %s"""
    
    valores = (name, username_novo, email, password, username_atual)
    cursor.execute (sql, valores)
    cnx.commit ()
    cursor.close ()
    cnx.close ()

    session ["name"] = name
    session ["username"] = username_novo

    flash ("Perfil atualizado!")
    return redirect (url_for ("perfil"))

@app.route ("/humor")
def humor ():
    return render_template("registro_humor.html")

@app.route ("/semregistro")
def semregistro ():
    return render_template("semregistro.html")

@app.route ("/escrever")
def escrever ():
    return render_template("escrever.html")

@app.route ("/login")
def login ():
    return render_template ("login.html")

@app.route("/entrar", methods=["POST"])
def entrar():
    username = request.form.get("username")
    password = request.form.get("password")

    cnx = connection.MySQLConnection(
        user="root",
        password="gilovers@25",
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
        session ["name"] = resultado ["name"]
        session["username"] = resultado["username"] 

        flash("Login realizado com sucesso!")
        return redirect(url_for("principal"))

    else:
        flash("Usuário ou senha incorretos!")
        return redirect(url_for("login"))

if __name__ == "__main__":
    app.run (debug = True)
