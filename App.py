from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api, Resource
from werkzeug.utils import cached_property
from sqlalchemy import text


app = Flask(__name__)
app.secret_key = "Secret Key"

#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://phpmyadmin:welcome123$@localhost/flask_crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


#Creating model table for our CRUD database
class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))


    def __init__(self, name, email, phone):

        self.name = name
        self.email = email
        self.phone = phone


class Company(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    company_name = db.Column(db.String(100))
    company_email = db.Column(db.String(100))
    company_phone = db.Column(db.String(100))


    def __init__(self, company_name, company_email, company_phone):

        self.company_name = company_name
        self.company_email = company_email
        self.company_phone = company_phone


api = Api()
api.init_app(app)
name_space = api.namespace('my_api', description='API Project')


#This is the index route where we are going to
#query on all our employee data
@app.route('/employees')
def Index():
    all_data = Data.query.all()
    return render_template("index.html", employees = all_data)



#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']


        my_data = Data(name, email, phone)
        db.session.add(my_data)
        db.session.commit()

        flash("Employee Inserted Successfully")

        return redirect(url_for('Index'))


#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']

        db.session.commit()
        flash("Employee Updated Successfully")

        return redirect(url_for('Index'))




#This route is for deleting our employee
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")
    return redirect(url_for('Index'))






@name_space.route("/")
class LogList(Resource):
    def get(self):  # will be used to fetch all record from log later
        sql = text('select company_name from company')
        result = db.engine.execute(sql)
        data = [row[0] for row in result]
        response = jsonify(data)
        response.status_code = 200 # or 400 or whatever
        return response

    def post(self):  # will be used to create a new log record
        return {
            "status": "Create new log"
        }


@name_space.route("/<int:id>")
class LogDetail(Resource):
    def get(self, id):  # will be used to see one particular log detail
        sql = text('SELECT company_name FROM company WHERE id = \'{}\''.format(id))
        result = db.engine.execute(sql)
        data = [row[0] for row in result]
        response = jsonify(data)
        response.status_code = 200 # or 400 or whatever
        return response

    def put(self, id):  # will be used to update particular log
        return {
            "status": "Updated log with id " + str(id)
        }

    def delete(self, id):  # will be used to delete particular log
        return {
            "status": "Deleted log with id " + str(id)
        }

if __name__ == "__main__":
    app.run(debug=True)