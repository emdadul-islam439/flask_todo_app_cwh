from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sl_no = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sl_no}- {self.title}"


@app.route("/", methods = ["GET", "POST"])
def hello_world():
    if request.method == "POST":
        todo = Todo(title = request.form['title'], desc = request.form['desc'])
        db.session.add(todo)
        db.session.commit()
        
    allTodo = Todo.query.all()
    print(allTodo)
    return render_template("index.html", allTodo = allTodo)


@app.route("/show")
def show():
    allTodo = Todo.query.all()
    print(allTodo)
    return "this is the second page"


if __name__ == "__main__":
    app.run(debug = True, port = 8000)
