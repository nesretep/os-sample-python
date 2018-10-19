import socket

from flask_cors import CORS
from flask import Flask, request

application = Flask(__name__)

origin = request.host
        allowed_domains = ['fs-dev.byu.edu',
                           'fs-cpy.byu.edu',
                           'fs-stg.byu.edu',
                           'fs.byu.edu'
                           '192.168.105.223']
cors = CORS(application, resources={r"/labels": {"origins": origin}})
chem_printer = "192.168.101.18"
nonchem_printer = '192.168.101.35'
port = 9100

def print(ipaddress, port):
    try:
        username = request.form['username']
        password = request.form['password']
        print_data = request.form['printData']

        if username != 'lk$liC34' and password != 'M@KD(uS3oi':
            return

        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.SOL_TCP)
        clientsocket.connect((ipaddress, port))
        bytes_sent = clientsocket.sendall(print_data)
        return f"{len(print_data)} were written successfully."
    except Exception as post_error:
        return f"ERROR:{post_error}"
    

@application.route("/labels/chemical", methods = ['POST'])
print(chem_printer)


@application.route("/labels/nonchemical", methods = ['POST'])
print(nonchem_printer)
if __name__ == "__main__":
    application.run(debug=True)
