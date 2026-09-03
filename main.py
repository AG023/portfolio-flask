import csv
import os
import sqlite3

from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Het pad naar portfolio.db, naast dit main.py-bestand
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "portfolio.db")


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/interests")
def interests():
    connection = get_db_connection()

    interests = connection.execute("""
        SELECT id, name, category, description
        FROM interests
        ORDER BY name
    """).fetchall()

    connection.close()

    return render_template("interests.html", interests=interests)


@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)


def write_to_csv(data):
    with open("database.csv", "a", newline="") as csvfile:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        writer = csv.writer(csvfile)
        writer.writerow([email, subject, message])


@app.route("/submit_form", methods=["GET", "POST"])
def submit_form():
    if request.method == "POST":
        data = request.form.to_dict()
        write_to_csv(data)
        return redirect("/thankyou.html")

    return "Something went wrong!"