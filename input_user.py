""" ===================================
A simple user registration system.
Delete and Update user information

=> From     : hacker_tesla
=> Language : Flask [ Python microframework ] 
=> Email    : hacker_tesla@protonmail.com 
=> Github   : github.com/hacker-tesla
===================================== """



#  importing necessary modules
from flask import Flask
from flask import render_template
from flask import url_for
from flask import redirect 
from flask import request

#  importing sqlalchemy for manage database
from flask_sqlalchemy import SQLAlchemy

#  passing this webapp in flask
app = Flask(__name__)

#  configuring database
app.config["SQLALCHEMY_DATABASE_URI"]="postgres://postgres:123456789@127.0.0.1"
app.config["SQLALCHEMY_DATABASE_TRACK_MODIFICATION"]=False

#  passing webapp in database
db = SQLAlchemy(app)

#  make a database model for store user information
class User(db.Model): 
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   firstname = db.Column(db.String(80) )
   lastname = db.Column(db.String(80) )
   email = db.Column(db.String(180), unique=True)
   password = db.Column(db.String(100), unique=True)

#  default page of website
@app.route( "/", methods=['GET', 'POST'] )
def index():
   #  check the request method if request method is GET then execute this
   if request.method == "GET":
      users = User.query.all()
      user = User(
         firstname='',
         lastname='',
         email='',
         password=''
      )
      pagename='home'
      return render_template( 
         'input_user.html',
         pagename=pagename, 
         users=users, 
         user=user 
      )


   #  if request method is POST then execute this
   else:
      firstname = request.form['firstname']
      lastname = request.form['lastname']
      email = request.form['email']
      password = request.form['password']

      user = User(
         firstname=firstname,
         lastname=lastname,
         email=email,
         password=password
      )

      db.session.add(user)
      db.session.commit()
      return redirect(  url_for("index")   )


#  making user delete system 
@app.route( "/delete/<int:id>"   )
def delete(id):
   delete_user = User.query.get_or_404(id)
   db.session.delete(delete_user)
   db.session.commit()
   return redirect(  url_for("index")  )



#  making user update system
@app.route( "/update/<int:id>", methods=['POST', 'GET']   )
def update(id):
   user = User.query.get_or_404(id)
   #check if the request method is post then execute this
   if request.method == 'POST':
      user.firstname = request.form['firstname']
      user.lastname = request.form['lastname']
      user.email = request.form['email']
      user.password = request.form['password']
      db.session.commit()
      return redirect(  url_for("index")  )  

   else:
      pagename = 'updatehome'
      users = User.query.all()
      return render_template(
         'input_user.html',
         pagename=pagename,
         user=user,
         users=users
      )





if __name__ == "__main__":
   app.run(debug=True) 