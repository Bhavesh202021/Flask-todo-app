from flask import Flask , render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from ddtrace import tracer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(200) , nullable = False)
    desc = db.Column(db.String(500) , nullable = False)
    date_created = db.Column(db.DateTime , default = datetime.utcnow)
    
    def __repr__(self) -> str:
        return f'{self.sno} - {self.title}'


@tracer.wrap("flask.request",service='flask-todo',resource='GET/POST',span_type='web')
@app.route("/login/myto-do/feedback",methods=['GET','POST'])
def feed_back():
    return render_template('feedback.html')

@tracer.wrap("flask.request",service='flask-home',resource='GET/POST',span_type='web')
@app.route("/login/myto-do",methods=['GET','POST'])
def hello_world():
    if request.method == 'POST':
        title =  request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title, desc = desc)
        db.session.add(todo)
        db.session.commit()
        #print('post')
        #print(request.form['title'])   
    allTodo = Todo.query.all()
    return render_template('index.html' , allTodo = allTodo)
    #print(allTodo)
    #return "<p>Hello, World!</p>"

@tracer.wrap("flask.request",service='flask-login',resource='GET',span_type='web')
@app.route("/login")
def login():
    return render_template('login.html')

@tracer.wrap("flask.request",service='flask-home',resource='GET',span_type='web')
@app.route("/")
def login1():
    return render_template('login.html')

@tracer.wrap("flask.request",service='flask-show',resource='GET',span_type='web')
@app.route("/login/myto-do/show")
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return redirect("https://www.hotelmanagement.net/")


@tracer.wrap("flask.request",service='flask-aboutus',resource='GET',span_type='web')
@app.route("/login/myto-do/aboutus")
def aboutus():
    return render_template('aboutus.html') 

@tracer.wrap("flask.request",service='flask-todoupdate',resource='GET',span_type='web')
@app.route("/login/myto-do/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno =sno).first()
    db.session.delete(todo)
    db.session.commit()
    #print(allTodo)
    #return "<p>This page for products page </p>"
    return redirect("/login/myto-do")


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
        return redirect("/login/myto-do")
    
        
        
    todo = Todo.query.filter_by(sno =sno).first()
    #print(allTodo)
    return render_template('update.html' , todo = todo)

if __name__ == "__main__":
    app.run(debug = True,port = 8000) 
    