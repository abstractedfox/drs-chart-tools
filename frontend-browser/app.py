from flask import Flask
from flask import render_template

app = Flask(__name__, static_folder = "static")

@app.route("/")
def index():
    return render_template("/superstepper.html")
