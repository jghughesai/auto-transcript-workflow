import os
import logging
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from main import main
from datetime import timedelta

app = Flask(__name__, template_folder="templates")
app.config["TESTING"] = True
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = 'Lax'
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', os.urandom(24))

csrf = CSRFProtect(app)

logging.basicConfig(level=logging.INFO)

class APIKeyForm(FlaskForm):
    api_key = StringField('OpenAI API Key', validators=[DataRequired(), Length(min=20, max=60)])
    submit = SubmitField('Submit')

class SignInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=60)])
    password = StringField('Password', validators=[DataRequired(), Length(min=5, max=60)])
    submit = SubmitField('Submit')

@app.route("/home", methods=["GET"])
def home():
    form = APIKeyForm()
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template("home.html", form=form)

@app.route("/", methods=["GET"])
def index():
    form = SignInForm()
    return render_template("index.html", form=form)

@app.route("/run_main", methods=["POST", "GET"])
def run_main():
    api_key = session.get('api_key')
    if 'username' not in session:
        return jsonify("Username not found or session has expired. Please login again.")
    if not api_key:
        logging.error("API key not set.")
        return jsonify(error="API Key not set"), 401
    
    try:
        response = main(api_key)
        logging.info(f"response: {response}")
        if response == "success":
            logging.info("Execution Success!")
            return jsonify(response)
        elif response == "failed":
            return jsonify(response), 200
        elif response == "get_summary_error":
            return jsonify(error="There was a problem getting the ai generated summary.")
        elif response == "drive_api_error":
            return jsonify(error="There was a problem connecting to the Google Drive API.")
        elif response == "authorization_error":
            return jsonify(error="There was a problem authorizing your Google Drive credentials.")
        else:
            return jsonify(error="There was a problem on our end, we apologize.")
    except Exception as e:
        logging.error(f"Error in run_main: {e}")
        return jsonify(error="An error occured"), 500
    
@app.route('/set_api_key', methods=['POST'])
def set_api_key():
    data = request.get_json()
    form = APIKeyForm(data=data)

    if form.validate():
        api_key = form.api_key.data
        session['api_key'] = api_key
        session.modified = True

        logging.info("API Key stored successfully")
        return jsonify({"message": "API Key stored successfully"}), 200
    else:
        logging.warning("Form validation failed: %s", form.errors)
        return jsonify({"error": "Failed to validate form"}), 400
    
@app.route('/sign-in', methods=['POST'])
def sign_in():
    if request.method == "POST":
        form = SignInForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            
            username_env = os.environ.get("USERNAME")
            password_env = os.environ.get("PASSWORD")

            if username and password and username == username_env and password == password_env:
                session['username'] = username
                session.permanent = True
                session.modified = True
                logging.info(f"User signed in successfully")
                return redirect(url_for("home"))
            else:
                logging.warning("Invalid login attempt")
                return redirect(url_for('index'))

        else:
            logging.warning("Form validation failed: %s", form.errors)
            return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=os.environ.get('FLASK_ENV') != 'production')
