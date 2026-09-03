import csv
import os

import psycopg
from psycopg.rows import dict_row
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Voor lokaal werken gebruikt Flask localhost.
# Later, in Docker Compose, wordt DB_HOST ingesteld op "db".
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "portfolio")
DB_USER = os.getenv("DB_USER", "portfolio_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "portfolio_password")


def get_db_connection():
    return psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/interests")
def interests():
    with get_db_connection() as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""
                SELECT id, name, category, description
                FROM interests
                ORDER BY name
            """)
            interests = cursor.fetchall()

    return render_template("interests.html", interests=interests)


@app.route("/<string:page_name>.html")
def html_page(page_name):
    return render_template(f"{page_name}.html")


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