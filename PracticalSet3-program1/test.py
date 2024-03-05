from flask import Flask,render_template
app=Flask(__name__)
@app.route("/welcome")
def mylogic():
  return render_template("index.html",name="Python")
if __name__=="__main__":
  app.run()