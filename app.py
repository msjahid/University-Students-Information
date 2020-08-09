from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
 
 
 
 
app = Flask(__name__)
app.secret_key = "Secret Key"
 
#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:5271@localhost/seustudents_info'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)
 
 
#Creating model table for our CRUD database
class Data(db.Model):
    id = db.Column(db.String(100), primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    batch = db.Column(db.Integer)
    gpa = db.Column(db.Float)
 
 
    def __init__(self, id, name, email, phone, batch, gpa):
 
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.batch = batch
        self.gpa = gpa
 
 
 
 
#This is the index route where we are going to
#query on all our employee data
@app.route('/')
def Index():
    all_data = Data.query.all()
 
    return render_template("index.html", students = all_data)
 
 
 
#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():
 
    if request.method == 'POST':
 
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        batch = request.form['batch']
        gpa = request.form['gpa']
 
 
        my_data = Data(id, name, email, phone, batch, gpa)
        db.session.add(my_data)
        db.session.commit()
 
        flash("Student Inserted Successfully")
 
        return redirect(url_for('Index'))
 
 
#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET', 'POST'])
def update():
 
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))
 
        my_data.id = request.form['id']
        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
        my_data.batch = request.form['batch']
        my_data.gpa = request.form['gpa']
 
        db.session.commit()
        flash("Student information Updated Successfully")
 
        return redirect(url_for('Index'))
 
 
 
 
#This route is for deleting our employee
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Student Information Deleted Successfully")
 
    return redirect(url_for('Index'))
 
 
 
 
 
 
if __name__ == "__main__":
    app.run(debug=True)