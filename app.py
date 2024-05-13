import os
from flask import Flask, render_template, request, jsonify
from main import main

app = Flask(__name__, template_folder="templates")
app.config["TESTING"] = True

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/run_main", methods=["POST"])
def run_main():
    main()
    return "Completed run"



if __name__ == "__main__":
    app.run(debug=True)