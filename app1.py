from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys

#Creates an application that is the name of our file i.e. app
app = Flask(__name__)
#configuring our application to connect to our postgres database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:09091990@192.168.1.73:5432/todoapp'
#This creates an instance (called db) of our database that we can interact using SQLAlchemy
db = SQLAlchemy(app)

#Creating a class called "Todo" by inheriting from db.model. This allows us to map from our classes to database tables via SQLAlchemy ORM
class Todo(db.Model):
    __tablename__ = 'Todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)   
    #Use a repr method to return a customized string whenever we are debugging or printing an object in this script
    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

#This creates the table for the models that we have declared in the above lines
db.create_all()

#This controller retrieves data from the form when users click to submit/POST the data
@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        #As the description is coming to the server as dictionary, we use the following code
        description = request.get_json()['description']
        #Using the Todo class defined above
        todo = Todo(description=description)
        #This adds the data to the pending-to-add into database list
        db.session.add(todo)
        #This commits the pending list i.e. makes the changes in the database
        db.session.commit()
        body['description'] = todo.description
    except:
        db.session.rollback()
        error=True
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort (400)
    else:
        return jsonify(body)

 
@app.route('/')
#use render_template to specify the HTML file to render to the users whenever they visit this route.
#MVC: the index() method is the Controller, index.html is the View and the data is the Model
def index():
    #Flask uses Jinja, a templating engine that allows us to embed non-HTML inside HTML files
    return render_template('index.html', data=Todo.query.all())
