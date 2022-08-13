from crypt import methods
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    sl_no = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sl_no}- {self.title}"


@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST" and request.form['title'] and request.form['desc']:
        todo = Todo(title=request.form['title'], desc=request.form['desc'])
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    print(allTodo)
    return render_template("index.html", allTodo=allTodo)


@app.route("/show")
def show():
    allTodo = Todo.query.all()
    print(allTodo)
    return "this is the second page"


@app.route("/update/<int:sl_no>", methods=["GET", "POST"])
def update(sl_no):
    if request.method == "POST" and request.form['title'] and request.form['desc']:
        title = request.form['title'] 
        desc = request.form['desc']

        todo = Todo.query.filter_by(sl_no=sl_no).first()

        todo.title = title
        todo.desc = desc

        db.session.add(todo)
        db.session.commit()
        
        return redirect("/")

    todo = Todo.query.filter_by(sl_no=sl_no).first()
    return render_template("update.html", todo = todo)


@app.route("/delete/<int:sl_no>")
def delete(sl_no):
    todo = Todo.query.filter_by(sl_no=sl_no).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
