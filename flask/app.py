from flask import Flask 
from flask import render_template, request, redirect, url_for, session, flash
import mysql.connector as connection 

app = Flask (__name__)
app.secret_key = "segredo123"

@app.route ("/")
def conexao ():
    cnx = connection.MySQLConnection (
        user = "root",
        password = "gilovers@25",
        host = "127.0.0.1",
        database = "DiarioDeHumor"
    )

    cursor = cnx.cursor (dictionary = True)
    cursor.execute ("SELECT nome, user, email FROM usuarios")
    resultado = cursor.fetchall ()

    return render_template ("cadastro.html", banco = resultado)

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

    return redirect (url_for ("conexao"))

@app.route ("/login")
def login ():
    return render_template ("login.html")

@app.route("/entrar", methods=["POST"])
def entrar():
    user = request.form.get("user")
    senha = request.form.get("senha")

    cnx = connection.MySQLConnection(
        user="root",
        password="gilovers@25",
        host="127.0.0.1",
        database="DiarioDeHumor"
    )
    cursor = cnx.cursor(dictionary=True)

    sql = "SELECT * FROM usuarios WHERE user = %s AND senha = %s"
    valores = (user, senha)
    cursor.execute(sql, valores)
    resultado = cursor.fetchone()

    cursor.close()
    cnx.close()

    if resultado:  
        session["usuario"] = resultado["user"]  
        flash("Login realizado com sucesso!")
        return redirect(url_for("conexao"))
    else:
        flash("Usuário ou senha incorretos!")
        return redirect(url_for("login"))

if __name__ == "__main__":
    app.run (debug = True)
