from flask import Flask , render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from ddtrace import tracer

import logging, os , sys, time

          
filepath = "C:/Study/SEM-8/Flask2022/test.log"
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
FORMAT = logging.Formatter('%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s')
#logging.basicConfig(format=FORMAT, filename = filepath,filemode= 'a+' )
file_handler = logging.FileHandler(filepath)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(FORMAT)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(FORMAT)

log.addHandler(file_handler)
log.addHandler(stream_handler)
########################################
# create a flask app

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# class Todo():
#     def get_db_connection():
#         conn = sqlite3.connect('database.db')
#         conn.row_factory = sqlite3.Row
#         return conn

#-----------------------------------------
#  Table Name : Todo
#  Col: sno , title, desc, date_created, status
#-----------------------------------------
class Todo(db.Model):
    #log.info('Program started - ', datetime.now())
    sno = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(200) , nullable = False)
    desc = db.Column(db.String(500) , nullable = False)
    date_created = db.Column(db.DateTime , default = datetime.utcnow)
    
    def __repr__(self) -> str:
       return f'{self.sno} - {self.title}'

### Feedback page 
@tracer.wrap("flask.request",service='flask-todo',resource='GET/POST',span_type='web')
@app.route("/login/myto-do/feedback",methods=['GET','POST'])
def feed_back():
    log.info('currently working on feeback page! ')
    return render_template('feedback.html')

#-----------------------------------------
#               Home Page
#-----------------------------------------
@tracer.wrap("flask.request",service='flask-home',resource='GET/POST',span_type='web')
@app.route("/login/myto-do",methods=['GET','POST'])
def hello_world():
    if request.method == 'POST':
        title =  request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title, desc = desc)
        db.session.add(todo)
        db.session.commit()
        #log.info('post')
        log.info("Added new todo title", request.form['title'])
        log.info("Added new todo ",request.form['desc'])
        
        
        #print(request.form['title'])   
    allTodo = Todo.query.all()
    #log.info(allTodo)
    return render_template('index.html' , allTodo = allTodo)
    
    #return "<p>Hello, World!</p>"

@tracer.wrap("flask.request",service='flask-login',resource='GET',span_type='web')
@app.route("/login")
def login():
    log.info("successfully login ")
    return render_template('login.html')

@tracer.wrap("flask.request",service='flask-home',resource='GET',span_type='web')
@app.route("/")
def login1():
    log.info("home Page")
    return render_template('login.html')

# @tracer.wrap("flask.request",service='flask-show',resource='GET',span_type='web')
# @app.route("/login/myto-do/show")
# def products():
#     allTodo = Todo.query.all()
#     print(allTodo)
#     return redirect("https://www.hotelmanagement.net/")





#-----------------------------------------
#               Delete List
#-----------------------------------------
@tracer.wrap("flask.request",service='flask-tododelete',resource='GET',span_type='web')
@app.route("/login/myto-do/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno =sno).first()
    db.session.delete(todo)
    db.session.commit()
    log.info("Delete a list of ",todo)
    #print(allTodo)
    #return "<p>This page for products page </p>"
    return redirect("/login/myto-do")

#-----------------------------------------
#               Update List
#-----------------------------------------
@tracer.wrap("flask.request",service='flak_update',resource='GET/POST',span_type='web')
@app.route("/login/myto-do/update/<int:sno>", methods=['GET','POST'])
def update(sno):
    if request.method == 'POST':
        title =  request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno =sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        log.info('update a todo list ',todo)
        return redirect("/login/myto-do")
       
    todo = Todo.query.filter_by(sno =sno).first()
    #print(allTodo)
    return render_template('update.html' , todo = todo)

# @app.route("/login/myto-do/completed")
# def completed(sno):
#     todo = Todo.query.filter_by(status ='Done').first()
#     db.session.add(todo)
#     db.session.commit()
#     #print(allTodo)
#     #return "<p>This page for products page </p>"
#     return redirect("completd.html",todo=todo)

# @app.route("/login/myto-do/uncompletd")
# def uncompleted(sno):
#     todo = Todo.query.filter_by(sno=sno).all()
#     db.session.add(todo)
#     db.session.commit()
#     #print(allTodo)
#     #return "<p>This page for products page </p>"
#     return redirect("uncompletd.html",todo=todo)


if __name__ == "__main__": 
    app.run(host = '0.0.0.0',debug = True,port = 7000) 