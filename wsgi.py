# import requests as url
import logging
from flask import Flask, request
application = Flask(__name__)

@application.route("/labels", methods = ['POST'])
def print():
    try:
        username = request.form['username']
        password = request.form['password']
        print_data = request.form['printData']
    except Exception as post_error:
        return f"ERROR:{post_error}"

    return f"username: {username}; password: {password}; printData: {print_data}"

if __name__ == "__main__":
    application.run(debug=True)
