import socket

from flask_cors import CORS
from flask import Flask, request

application = Flask(__name__)


allowed_domains = ['fs-dev.byu.edu',
                   'fs-cpy.byu.edu',
                   'fs-stg.byu.edu',
                   'fs.byu.edu',
                   '192.168.105.223']


chem_printer = "192.168.101.18"
nonchem_printer = '192.168.101.35'
port = 9100


def printer(ipaddress, port, print_test=None):
    origin = request.host
    cors = CORS(application, resources={r"/labels": {"origins": origin}})

    try:
        username = request.form['username']
        password = request.form['password']
        if print_test is not None:
            print_data = print_test
        else:
            print_data = request.form['printData']

        if username != 'lk$liC34' and password != 'M@KD(uS3oi':
            return "ERROR: Invalid Credentials"

        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
        clientsocket.connect((ipaddress, port))
        bytes_sent = clientsocket.sendall(print_data)
        return f"{len(print_data)} bytes were written successfully."
    except Exception as post_error:
        return f"ERROR:{post_error}"


@application.route("/labels/chemical", methods = ['POST'])
def chem_printer():
    printer(chem_printer, port)


@application.route("/labels/nonchemical", methods = ['POST'])
def nonchem_printer():
    printer(nonchem_printer, port)


@application.route("/labels/nonchemical/test", methods = ['POST'])
def test_print():
    test_data = ["\x02L\nD11\nH12\nPE\nSE\n1e9202000050010B",
                 "\n1921SA200000015B",
                 "\nE\n"]
    B36ID = ["BYUC123456", "BYUC654321"]
    data = f"{test_data[0]}{B36ID[0]}{test_data[1]}{B36ID[0]}{test_data[2]}"
    printer(nonchem_printer, port, print_test=data)


@application.route("/labels/chemical/test", methods = ['POST'])
def test_print2():
    test_data = ["\x02L\nD11\nH12\nPE\nSE\n1e9202000050010B",
                 "\n1921SA200000015B",
                 "\nE\n"]
    B36ID = ["BYUC123456", "BYUC654321"]
    data = f"{test_data[0]}{B36ID[1]}{test_data[1]}{B36ID[1]}{test_data[2]}"
    printer(chem_printer, port, print_test=data)


if __name__ == "__main__":
    application.run(debug=True)


