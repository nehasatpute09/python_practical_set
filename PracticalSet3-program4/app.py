from flask import Flask, redirect, url_for, request , render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# @app.route('/')
# def home():
#     return render_template('home.html')
# @app.route('/login')
# def login():
#     pass
# @app.route('/register')
# def register():
#     pass
@app.route("/home")
def fun():
    return render_template("home.html")

@app.route("/", methods=["GET", "POST"])
def processing_input():
    result = None
    if request.method == "POST":
        user_input = request.form['input_text']
        result = f"You have entered {user_input}"
    return render_template("home.html",result = result)

if __name__ == "__main__":
    app.run(debug=True)
