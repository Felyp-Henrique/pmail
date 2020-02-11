#!/usr/bin/env python3

import argparse
import poplib
import re
import getpass
import zipfile
import datetime
import tempfile

input_args = argparse.ArgumentParser(
    'PMail', description='Simple tool writed in Python 3 to backup emails.'
)

input_args.add_argument('host', help='Address of server POP3')
input_args.add_argument('--port', type=int, help='Port of server')
input_args.add_argument('--ssl', action='store_true')
input_args.add_argument('email', help='E-mail address of user')
input_args.add_argument('--password', help='Password of user(less secure)')
input_args.add_argument('--outzip', action='store_true', help='Save the backup in Zip file')

options = input_args.parse_args()

# Create connection with server POP3
if not options.ssl:
    pop_server = poplib.POP3(
        options.host,
        options.port or poplib.POP3_PORT,
    )
else:
    pop_server = poplib.POP3_SSL(
        options.host,
        options.port or poplib.POP3_SSL_PORT,
    )

# Validate if e-mail is valid
if re.match(r'^.+@.+$', options.email) is None:
    print('E-mail is invalid! Try again with correct e-mail')
    exit(1)

# Try do connection with user and password
pop_server.user(options.email)
pop_server.pass_(options.password or getpass.getpass())

# Get number of messages
number_messages = len(pop_server.list()[1])

# save backup in zip file
if options.outzip is not None:
    file_name = f"./{ datetime.datetime.now() } - { options.email }"
    file_zip = zipfile.ZipFile(file_name, 'w')
    for i in range(number_messages):
        msg = b"\n".join(pop_server.retr(i+1)[1])
        with tempfile.NamedTemporaryFile() as file_email:
            file_email.write(msg)
            file_zip.write(file_email.name)
    file_zip.close()
    exit(0)

# if not make zip, only print the emails in standard out
for i in range(number_messages):
    msg = b"\n".join(pop_server.retr(i+1)[1])
    print(msg.decode('utf-8'))