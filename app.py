from flask import Flask , render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


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



@app.route("/",methods=['GET','POST'])
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

@app.route("/user" ,methods = ['POST'])
def user_post():
    data = request.json
    try:
        temperature = data['temperature']
        humidity = data['humidity']
        light = data['light']
        moistureLevel = data["moistureLevel"]
        #post = open(f'./data/{user}.json','w')
        
        obj = {
            'temperature': temperature,
            'humidity':humidity,
            'light':light,
            'moistureLevel':moistureLevel  
        }
        print(obj)
        # post.write(json.dumps(obj))
        # post.close()
        
        return {'status_code':200,'message':'Post created successful'}
        
    except Exception as e:
        return {'status_code':300 , 'message':f'Generic error:{str(e)}'}


@app.route("/login" or "/signup")
def login():
    return render_template('login.html')
   
@app.route("/show")
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return redirect("https://www.hotelmanagement.net/")

@app.route("/aboutus")
def aboutus():
    return render_template('aboutus.html') 

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno =sno).first()
    db.session.delete(todo)
    db.session.commit()
    #print(allTodo)
    #return "<p>This page for products page </p>"
    return redirect("/")

@app.route("/update/<int:sno>",methods=['GET','POST'])
def update(sno):
    if request.method == 'POST':
        title =  request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno =sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    
        
        
    todo = Todo.query.filter_by(sno =sno).first()
    #print(allTodo)
    return render_template('update.html' , todo = todo)

if __name__ == "__main__":
    app.run(debug = True,port = 8000) 
    