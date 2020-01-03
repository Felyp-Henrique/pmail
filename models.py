from pmail import database

class Email(db.Model):
    id = db.Field(int, 'id', 0, primary_key=True) # the class Model expect id field in class child
    sender = db.Field(str, 'sender', '')
    receiver = db.Field(str, 'receiver', '')
    body_email = db.Field(str, 'body_email', '')