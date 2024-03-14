#flask: This is the name of the module being imported.
#Flask: This is the class within the Flask module that represents a Flask application. You create an instance of this class to create a Flask application.
#render_template : this function  takes a template(HTML file from template folder) filename and optional context data as arguments and returns the rendered template
#request: This is an object provided by Flask that represents the current HTTP request.
#redirect: This is a function provided by Flask for performing HTTP redirects. It takes a URL as an argument and redirects the client to that URL.
#url_for: This is a function provided by Flask for generating URLs for Flask routes. It takes the name of a view function as an argument and returns the URL for that view function.
#session: This is an object provided by Flask for storing user-specific data across requests. It uses cookies to store a session ID on the client side and stores the session data on the server side.
#flash: This is a function provided by Flask for displaying temporary messages to the user. It is typically used to display feedback messages after certain actions such as form submissions.
#werkzeug.security: This is a module provided by the Werkzeug library, which is a utility library for WSGI (Web Server Gateway Interface) applications in Python. It provides various utilities for working with HTTP, including password hashing and authentication.
#generate_password_hash: This is a function provided by Werkzeug for generating a secure hash of a password. It takes a password as input and returns a hash string.
#check_password_hash: This is a function provided by Werkzeug for checking if a password matches a given hash. It takes a password and a hash as inputs and returns True if the password matches the hash, otherwise False.
from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'hardsecretkey'

# MySQL database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'mydatabase_python'
}


# Function to create MySQL connection
def create_connection():
    return mysql.connector.connect(**db_config)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = create_connection()
        cursor = conn.cursor()

        # Check if username already exists
        cursor.execute("SELECT * FROM user_info WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('register'))
        else:
            # Insert new user into the database
            hashed_password = generate_password_hash(password)
            cursor.execute("INSERT INTO user_info (username, password) VALUES (%s, %s)", (username, hashed_password))
            conn.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = create_connection()
        cursor = conn.cursor()

        # Retrieve user from database
        cursor.execute("SELECT * FROM user_info WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[2], password):
            # Store user data in session
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Login successful.', 'success')
            return redirect(url_for('dashboard'))
            # return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template("logout.html",session_username = session["username"] )

    else:
        # return "Login Unsuccessful"
        flash('Please log in to access the dashboard.', 'info')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # Clear session data
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
