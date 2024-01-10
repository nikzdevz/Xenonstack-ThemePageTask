import mysql
import mysql.connector
from flask import Flask, render_template, session

from flask_session import Session

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    loggedinEmail = ""
    if session.get('loggedInEmail') is not None:
        print(session['loggedInEmail'])
        loggedinEmail = session['loggedInEmail']
    return render_template('index.html', email=loggedinEmail)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contactus.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('loginRegister.html')


if __name__ == "__main__":
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
    app.run()
