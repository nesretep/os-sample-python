# import requests as url
import logging
from flask import Flask, request
application = Flask(__name__)

@application.route("/labels")
def print():
    try:
        username = request.args['username']
        password = request.args['password']
        print_data = request.args['printData']
    except Exception as post_error:
        return "ERROR"

    return f"username: {username}; password: {password}; printData: {print_data}"

if __name__ == "__main__":
    application.run(debug=True)
