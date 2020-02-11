# PMail

Simple tool writed in Python 3 to backup emails.

# Installation

To run, you need install Python 3.x and then, run the file install.sh if you are on Linux. If you are on Windows, create a environment variable to run.

# Usage

```shell
$ pmail --help
usage: PMail [-h] [--port PORT] [--ssl] [--password PASSWORD] [--outzip]
             host email

Simple tool writed in Python 3 to backup emails.

positional arguments:
  host                 Address of server POP3
  email                E-mail address of user

optional arguments:
  -h, --help           show this help message and exit
  --port PORT          Port of server
  --ssl
  --password PASSWORD  Password of user(less secure)
  --outzip             Save the backup in Zip file
```

# Example

This example the user not pass the password as argument and save all emails in binary files and save the files in zip file:

```shell
$ pmail my.domain user@my.domain --outzip
password: ******
```

This other example, the user pass the password as argument:

```shell
$ pmail my.domain user@my.domain --pass my_pass_less_secure --outzip
```