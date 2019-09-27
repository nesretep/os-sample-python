#! /usr/bin/env python3

import socket

from flask_cors import CORS
from flask import Flask, request

application = Flask(__name__)

allowed_domains = ['fs-dev.byu.edu',
                   'fs-cpy.byu.edu',
                   'fs-stg.byu.edu',
                   'fs.byu.edu',
                   '192.168.105.220']

chem_printer = "192.168.101.18"
nonchem_printer = '192.168.101.35'
port = 9100


def printer(ipaddress, port, test=None):
    print("test")
    origin = request.host_url
    cors = CORS(application, resources={r"/labels": {"origins": origin}})
    application.config['CORS_HEADERS'] = 'Content-Type'

    test_data = ["\x02L\nD11\nH12\nPE\nSE\n1e9202000050010B",
                 "\n1921SA200000015B",
                 "\nE\n"]
    B36ID = ["BYUC123456", "BYUC654321"]
    my_data = f"{test_data[0]}{B36ID[0]}{test_data[1]}{B36ID[0]}{test_data[2]}"

    try:
        username = request.form.get("username")
        password = request.form.get("password")
        if username != 'lk$liC34' and password != 'M@KD(uS3oi':
            return f"ERROR: Invalid Credentials - {username}:{password} - {request.get_data()}\n"

        if test is not None:
            print_data = my_data
        else:
            print_data = request.form("printData", False)
            print("print_data built")

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
        client_socket.connect((ipaddress, port))
        bytes_sent = client_socket.sendall(print_data)
        return f"{bytes_sent} bytes were written successfully."
    except Exception as post_error:
        return f"ERROR: {post_error} {request.get_data()}"


@application.route("/labels/", methods = ['POST'])
def nonchem_printer():
    response = printer(nonchem_printer, port)
    return response


@application.route("/labels/test", methods = ['POST'])
def test_print():
    response = printer(nonchem_printer, port, test="test")
    return f"Test print sent to non-chemical printer: {response}"


if __name__ == "__main__":
    application.run(debug=True)


