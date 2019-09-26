import socket

from flask_cors import CORS
from flask import Flask, request
import requests

application = Flask(__name__)


allowed_domains = ['fs-dev.byu.edu',
                   'fs-cpy.byu.edu',
                   'fs-stg.byu.edu',
                   'fs.byu.edu',
                   '192.168.105.220']


chem_printer = "192.168.101.18"
nonchem_printer = '192.168.101.35'
port = 9100


def printer(ipaddress, port, data):
    origin = request.host
    cors = CORS(application, resources={r"/labels": {"origins": origin}})

    try:
        username = request.form['username']
        password = request.form['password']
        if data is not None:
            print_data = data
        else:
            print_data = request.form['printData']
            print("print_data built")

        if username != 'lk$liC34' and password != 'M@KD(uS3oi':
            return "ERROR: Invalid Credentials"

        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
        clientsocket.connect((ipaddress, port))
        bytes_sent = clientsocket.sendall(print_data)
        return f"{bytes_sent} bytes were written successfully."
    except Exception as post_error:
        return f"ERROR:{post_error}"


@application.route("/labels/", methods = ['POST'])
def nonchem_printer():
    printer(nonchem_printer, port)


@application.route("/labels/test", methods = ['GET', 'POST'])
def test_print():
    test_data = ["\x02L\nD11\nH12\nPE\nSE\n1e9202000050010B",
                 "\n1921SA200000015B",
                 "\nE\n"]
    B36ID = ["BYUC123456", "BYUC654321"]
    data = f"{test_data[0]}{B36ID[0]}{test_data[1]}{B36ID[0]}{test_data[2]}"
    printer(nonchem_printer, port, data=data)
    return f"Test print sent to non-chemical printer: {data}"


if __name__ == "__main__":
    application.run(debug=True)


