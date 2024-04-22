from flask import Flask, render_template

from routes import main

app = Flask(__name__)


@main.get("/")
def home():
    return render_template("home.html")