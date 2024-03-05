from flask import Flask, redirect, url_for, request , render_template

app = Flask(__name__)

@app.route("/home",)
def home():
    return render_template("addition.html")
@app.route("/", methods = ["POST","GET"])
def addition():
    # return "addition function"
    if request.method == "POST":
        var1 = request.form['input_text1']
        var2 = request.form['input_text2']
        return render_template("addition.html", add = int(var1) + int(var2))
    return render_template("addition.html")


if __name__ == "__main__":
    app.run(debug=True)
