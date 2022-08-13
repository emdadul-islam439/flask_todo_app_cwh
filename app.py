from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "hello world"


@app.route("/second-route")
def second_route():
    return "this is the second page"


if __name__ == "__main__":
    app.run(debug = True, port = 8000)
