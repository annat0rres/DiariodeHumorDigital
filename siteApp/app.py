from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector as connection
from datetime import date, timedelta

app = Flask(__name__)
app.secret_key = "segredo123"

#função do connection para não repetir muitas vezes
def conectar():
    return connection.MySQLConnection(
        user="root",
        password="labinfo",
        host="127.0.0.1",
        database="setembroamarelo"
    )

@app.route("/")
def inicio():
    return render_template("inicio.html")

#parte do cadastro
@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/salvar", methods=["POST"])
def salvar():
    name = request.form.get("name")
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    data_nascimento = request.form.get("data_nascimento")
    apelido = request.form.get("apelido")

    cnx = conectar()
    cursor = cnx.cursor()

    sql = """
        INSERT INTO usuarios (name, username, email, password, data_nascimento, apelido)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    valores = (name, username, email, password, data_nascimento, apelido)
    cursor.execute(sql, valores)

    cnx.commit()
    cursor.close()
    cnx.close()

    flash("Cadastro realizado com sucesso!")
    return redirect(url_for("inicio"))

#parte de login
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/entrar", methods=["POST"])
def entrar():
    username = request.form.get("username")
    password = request.form.get("password")

    cnx = conectar()
    cursor = cnx.cursor(dictionary=True)

    sql = "SELECT * FROM usuarios WHERE username = %s AND password = %s"
    cursor.execute(sql, (username, password))
    resultado = cursor.fetchone()

    cursor.close()
    cnx.close()

    if resultado:
        session["username"] = resultado["username"]
        session["name"] = resultado["name"]
        flash("Login realizado com sucesso!")
        return redirect(url_for("principal"))
    else:
        flash("Usuário ou senha incorretos!")
        return redirect(url_for("login"))

#pagina principal
@app.route("/principal")
def principal():
    if "username" in session:
        name = session["name"]
        username = session["username"]
        return render_template("principal.html", name=name, username=username)
    else:
        flash("Faça login primeiro!")
        return redirect(url_for("login"))

#pagina do perfil com a função de alteração
@app.route("/perfil")
def perfil():
    if "username" not in session:
        flash("Faça login primeiro!")
        return redirect(url_for("login"))

    username = session["username"]

    cnx = conectar()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    cnx.close()

    return render_template(
        "perfil.html",
        name=user["name"],
        username=user["username"],
        email=user["email"],
        apelido=user["apelido"],
        data_nascimento=user["data_nascimento"]
    )

@app.route("/atualizar_perfil", methods=["POST"])
def atualizar_perfil():
    if "username" not in session:
        flash("Faça login para alterar o perfil.")
        return redirect(url_for("login"))

    username_atual = session["username"]

    name = request.form.get("name")
    username_novo = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    data_nascimento = request.form.get("data_nascimento")
    apelido = request.form.get("apelido")

    cnx = conectar()
    cursor = cnx.cursor()

    sql = """
        UPDATE usuarios
        SET name=%s, username=%s, email=%s, password=%s, data_nascimento=%s, apelido=%s
        WHERE username=%s
    """
    valores = (name, username_novo, email, password, data_nascimento, apelido, username_atual)
    cursor.execute(sql, valores)
    cnx.commit()
    cursor.close()
    cnx.close()

    session["name"] = name
    session["username"] = username_novo

    flash("Perfil atualizado!")
    return redirect(url_for("perfil"))

#parte dos registros
@app.route("/escrever")
def escrever():
    return render_template("escrever.html")

@app.route("/registro_escrever", methods=["POST"])
def registro_escrever():
    if "username" not in session:
        flash("Faça login antes de registrar seu humor!")
        return redirect(url_for("login"))

    username = session["username"]
    emocao = request.form.get("emocao")
    texto = request.form.get("texto")
    emoji = request.form.get("emoji")  # caso use um campo hidden com o nome do arquivo

    cnx = conectar()
    cursor = cnx.cursor()

    sql = """
        INSERT INTO registros (usernameUsuarios, emocao, emoji, texto)
        VALUES (%s, %s, %s, %s)
    """
    valores = (username, emocao, emoji, texto)
    cursor.execute(sql, valores)
    cnx.commit()
    cursor.close()
    cnx.close()

    flash("Registro salvo com sucesso!")
    return redirect(url_for("principal"))

#pagina do historico
@app.route("/historico")
def historico():
    if "username" not in session:
        flash("Faça login primeiro!")
        return redirect(url_for("login"))

    username = session["username"]

    cnx = conectar()
    cursor = cnx.cursor(dictionary=True)

    sql = """
        SELECT emocao, emoji, texto, data_registro
        FROM registros
        WHERE usernameUsuarios = %s
        ORDER BY data_registro DESC
    """
    cursor.execute(sql, (username,))
    registros = cursor.fetchall()
    cursor.close()
    cnx.close()

    current_date = date.today()
    week_start = current_date - timedelta (days = current_date.weekday ())


    return render_template("historico.html", registros=registros)

#parte da evolução
@app.route("/evolucao_humor")
def evolucao_humor():
    if "username" not in session:
        flash ("Faça login primeiro.")
        return redirect (url_for("login"))
    
    username = session["username"]

    cnx = conectar()
    cursor = cnx.cursor(dictionary=True)

    sql = """
        SELECT emocao, emoji, texto, data_registro
        FROM registros
        WHERE usernameUsuarios = %s
        ORDER BY data_registro DESC
        LIMIT 7
    """
    cursor.execute(sql, (username,))
    registros = cursor.fetchall()

    cursor.close()
    cnx.close()

    return render_template("evolucao_humor.html", registros=registros)

@app.route("/ver_mais/<int:idregistro>")
def ver_mais(idregistro):
    if "username" not in session:
        flash("Faça login primeiro!")
        return redirect(url_for("login"))

    username = session["username"]

    cnx = conectar()
    cursor = cnx.cursor(dictionary=True)

    sql = """
        SELECT emocao, emoji, texto, data_registro
        FROM registros
        WHERE idregistros = %s AND usernameUsuarios = %s
    """
    cursor.execute(sql, (idregistro, username))
    registro = cursor.fetchone()
    cursor.close()
    cnx.close()

    #se não houver registro, redireciona para a página "sem registro"
    if not registro:
        flash("Nenhum registro encontrado para este dia.")
        return redirect(url_for("semregistro"))

    return render_template("ver_mais.html", registro=registro)

@app.route ("/semregistro")
def semregistro ():
    return render_template ("semregistro.html")

if __name__ == "__main__":
    app.run(debug=True)