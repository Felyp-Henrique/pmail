# PMail

Simple e-mail backuper writed in Python 3

# Installation

To run, you need install Python 3.x and then, run the file install.sh if you are on Linux. If you are on Windows, create a environment variable to run.

# Usage

```shell
$ pmail --help
usage: PMail [-h] [--port PORT] [--ssl] [--password PASSWORD] host email

Simple e-mail backuper writed in Python 3

positional arguments:
  host                 Address of server POP3
  email                E-mail address of user

optional arguments:
  -h, --help           show this help message and exit
  --port PORT          Port of server
  --ssl
  --password PASSWORD  Password of user(less secure)
```

# Example

This example the user not pass the password as argument:

```shell
$ pmail my.domain user@my.domain
password: ******
# will print all e-mails relative this user
```

This other example, the user pass the password as argument:

```shell
$ pmail my.domain user@my.domain --pass my_pass_less_secure
# will print all e-mails relative this user
```