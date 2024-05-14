import os
from flask import Flask, render_template, request, jsonify, session
from main import main

app = Flask(__name__, template_folder="templates")
app.config["TESTING"] = True
app.config["SESSION_COOKIE_SECURE"] = True
app.secret_key = os.urandom(24)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/run_main", methods=["POST", "GET"])
def run_main():
    api_key = session.get('api_key')
    if not api_key:
        print("api key not set....")
        return jsonify(error="API Key not set"), 401
    response = main(api_key)
    print(f"response: {response}")
    return jsonify(response)

@app.route('/set_api_key', methods=['POST'])
def set_api_key():
    data = request.get_json()
    session['api_key'] = data['apiKey']
    return jsonify({"message": "API Key stored successfully"})

if __name__ == "__main__":
    app.run(debug=True)