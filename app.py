from datetime import datetime
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = "myapplication123"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///data.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "demo@gmail.com"
app.config["MAIL_PASSWORD"] = "123"
db = SQLAlchemy(app)

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.String(80))
    occupation = db.Column(db.String(80))



@app.route("/",methods=["GET","POST"])
def index():
    print(request.method)
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_obj = datetime.strptime(date,"%Y-%m-%d")
        occupation = request.form["occupation"]

        form = Form(first_name=first_name,last_name=last_name,email=email,date=date,occupation=occupation)
        db.session.add(form)
        db.session.commit()

        message_body = f"Thank you for your submission, {first_name}."\
                    f"Here are your Data:{first_name}\n{last_name}\n{date}\n"\
                    f"Thank You!"
        message = Message(subject="New form submission",
                          sender=app.config["MAIL_USERNAME"],)

        flash(f"{first_name}, Your Form was submitted successfully!","success")

    return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True,port=5001)