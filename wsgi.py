import socket

from flask_cors import CORS
from flask import Flask, request

app = Flask(__name__)


allowed_domains = ['fs-dev.byu.edu',
                   'fs-cpy.byu.edu',
                   'fs-stg.byu.edu',
                   'fs.byu.edu',
                   '192.168.105.220']


chem_printer = "192.168.101.18"
nonchem_printer = '192.168.101.35'
port = 9100


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


def printer(ipaddress, port, test=None):
    origin = request.host_url
    cors = CORS(app, resources={r"/labels": {"origins": origin}})
    app.config['CORS_HEADERS'] = 'Content-Type'

    try:
        username = request.form['username']
        password = request.form['password']
        if test is not None:
            print_data = test
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


@app.route("/labels/", methods = ['POST'])
def nonchem_printer():
    printer(nonchem_printer, port)


@app.route("/labels/test", methods = ['POST'])
@cross_origin(origin=request.host, supports_credentials=True, headers=['Content- Type','Authorization'])
def test_print():
    test_data = ["\x02L\nD11\nH12\nPE\nSE\n1e9202000050010B",
                 "\n1921SA200000015B",
                 "\nE\n"]
    B36ID = ["BYUC123456", "BYUC654321"]
    data = f"{test_data[0]}{B36ID[0]}{test_data[1]}{B36ID[0]}{test_data[2]}"
    printer(nonchem_printer, port, test=data)
    return f"Test print sent to non-chemical printer: {data}"


if __name__ == "__main__":
    app.run(debug=True)


