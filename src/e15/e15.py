import json
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify,
)
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = "your-secret-key-here"  


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="x",
        password="x",
        database="albergo",
    )


@app.route("/raw")
def list_entries_raw():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM CAMERA")
    entries = cursor.fetchall()
    cursor.close()
    conn.close()
    return entries

@app.route("/")
def list_entries():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM CAMERA")
    entries = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("list.html", entries=entries)

@app.route("/available")
def list_available_entries():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM CAMERA WHERE disponibile = TRUE")
    entries = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("list.html", entries=entries)

@app.route("/add", methods=("GET", "POST"))
def add_entries():
    if request.method == "POST":
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
    
        numero = request.form["numero"]
        tipo = request.form["tipo"]
        disponibile = bool(request.form["disponibile"])
        prezzo = request.form["prezzo"]
        numero_posti = request.form["numero_posti"]

       
        cursor.execute(
            "INSERT INTO CAMERA (numero, tipo, disponibile, prezzo, numero_posti) VALUES (%s, %s, %s, %s, %s)",
            (numero, tipo, disponibile, prezzo, numero_posti),
        )
        conn.commit()    
        cursor.close()
        conn.close()
        return redirect(url_for("list_entries"))
    return render_template("add.html")

@app.route("/bookings")
def list_bookings():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM PRENOTAZIONE")
    bookings = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("list.html", bookings=bookings)

@app.route("/bookings_raw")
def list_bookings_raw():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM PRENOTAZIONE")
    bookings = cursor.fetchall()
    cursor.close()
    conn.close()
    return  bookings

@app.route("/book", methods=("GET", "POST"))
def book_room():
    if request.method == "POST":
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        numero = request.form["numero"]
        cliente = request.form["cliente"]
        data_inizio = request.form["data_inizio"]
        data_fine = request.form["data_fine"]

        
        cursor.execute(
            "SELECT * FROM CAMERA WHERE numero = %s AND disponibile = TRUE", (numero,)
        )
        room = cursor.fetchone()
        if room:
         
            cursor.execute(
                "INSERT INTO PRENOTAZIONE (numero_camera, cliente, data_inizio, data_fine) VALUES (%s, %s, %s, %s)",
                (numero, cliente, data_inizio, data_fine),
            )
            cursor.execute(
                "UPDATE CAMERA SET disponibile = FALSE WHERE numero = %s", (numero)
            )
            conn.commit()
            flash("Camera prenotata con successo!")
        else:
            flash("Camera non disponibile!")
        
        cursor.close()
        conn.close()
        return redirect(url_for("list_bookings"))
    return render_template("add.html")

if __name__ == "__main__":
    app.run(debug=True)
