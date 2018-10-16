from flask import Flask, request
application = Flask(__name__)

@application.route("/")
def hello():
    param = request.args['test']
    return f"Hello {param}!"

if __name__ == "__main__":
    application.run(debug=True)
