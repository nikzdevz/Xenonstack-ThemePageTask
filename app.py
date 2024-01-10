
import mysql.connector
from flask import Flask, render_template, session, request, redirect, url_for


app = Flask(__name__)
app.secret_key = 'jdbjiobd'
config = {
    'user': 'nikz',
    'password': 'Devznikz#09',
    'host': 'localhost',
    'port': '3306',
    'database': 'xenonstackdb'
}
# config = {
#     'user': 'root',
#     'password': '',
#     'host': 'localhost',
#     'port': '3306',
#     'database': 'xenonstackdb'
# }
connection = mysql.connector.connect(**config)
cursor = connection.cursor()


@app.route('/login', methods=['POST'])
def login():
    username = request.form['email']
    password = request.form['password']
    # Check if the user exists and if the password matches
    query = "SELECT * FROM userbase WHERE email = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    if user:
        session['loggedInEmail'] = username
        return redirect(url_for('dashboard'))
    else:
        return "Invalid email or password"


@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    password = request.form['password']
    confirmPass = request.form['confirmpass']
    if password != confirmPass:
        return "Password not matched"
    # Check if the username already exists
    query = "SELECT * FROM userbase WHERE email = %s"
    cursor.execute(query, (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        return "Username already exists"
    else:
        # Insert the new user into the database
        insert_query = "INSERT INTO userbase (email,password) VALUES (%s, %s)"
        cursor.execute(insert_query, (email, password))
        connection.commit()
        session['loggedInEmail'] = email
        return redirect(url_for('dashboard'))


@app.route('/contactSubmit', methods=['POST'])
def contactSubmit():
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['contactEmail']
    phone = request.form['contactPhone']
    message = request.form['comment']
    # Check if the username already exists
    insert_query = "INSERT INTO contactus (Fname, Lname,Email, Phone, Message) VALUES (%s, %s, %s,%s,%s)"
    cursor.execute(insert_query, (fname, lname, email, phone, message))
    connection.commit()
    return f'Your message has been saved. We Will contact you soon.'


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contactus.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if session.get('loggedInEmail') is None:
        return f'You are not logged in. Please Login to continue.'
    return render_template('dashboard.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('loggedInEmail', None)
    return redirect(url_for('index'))


@app.route('/loginRegister', methods=['GET'])
def loginRegister():
    if session.get('loggedInEmail') is not None:
        return redirect(url_for('dashboard'))
    return render_template('loginRegister.html')


if __name__ == "__main__":
    # app.config["SESSION_PERMANENT"] = False
    # app.config["SESSION_TYPE"] = "filesystem"
    app.run()
