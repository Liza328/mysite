from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)

with app.app_context():
     db.create_all()

@app.route("/")
def index():
     return render_template("index.html")

@app.route('/submit', methods=["POST"])
def submit_from():
     #Проверка формата имейла + пробелы
     email = request.form["textInput"]
     valid = re.match(r"^[a-zA-Z0-9._%+-]=@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",email)
     if valid:
     #доп.проверка на пробелы
          if " " in email:
               email.replace(" ","")
     #проверка на регистр    
          if email!=email.lower():
               email=email.lower()
     #проверка на дубли в имейле
          existing_user = User.query.filter_by(email=email).first()
          if existing_user is not None:
               return redirect(url_for("index")) 
          else:
               new_user = User(email=email)

               db.session.add(new_user)
               db.session.commit()
          return redirect(url_for("index"))   

     else:      
          return redirect(url_for("index")) 

if __name__ == '__main__':
       app.run(debug=True)
   