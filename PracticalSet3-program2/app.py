from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

#create the object of Flask
app  = Flask(__name__)
app.config['SECRET_KEY'] = 'hardsecretkey'

#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/mydatabase_python'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#our model
class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username =  db.Column(db.String(100), unique=True, nullable=False)
    password =  db.Column(db.String(256), nullable=False)
    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if UserInfo.query.filter_by(username=username).first():
            flash('Username already taken. Please choose another.', 'error')
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = UserInfo(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = UserInfo.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['username'] = username
            # flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
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
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))
#creating our routes
@app.route('/')
def index():
    return render_template('index.html')

#obj1 = UserInfo("neha","root")

with app.app_context():
    db.create_all()

#run flask app
if __name__ == "__main__":
    app.run(debug=True)