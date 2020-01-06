class EmailTable(dict):
    SQL_CREATE_TABLE = """
        \rCREATE TABLE IF NOT EXISTS emails (
        \r  sender TEXT DEFAULT '',
        \r  receiver TEXT DEFAULT '',
        \r  subject TEXT DEFAULT '',
        \r  date TEXT DEFAULT '',
        \r  body_protocol TEXT DEFAULT ''
        \r)
    """

    SQL_INSERT_TABLE = """
        \rINSERT INTO emails (sender, receiver, subject, date, body_protocol)
        \rVALUES (?, ?, ?, ?, ?)
    """

    connection = None

    def create_table(self):
        self.connection.run(self.SQL_CREATE_TABLE)
    
    def save(self):
        self.connection.run(
            self.SQL_INSERT_TABLE,
            self.get('sender'),
            self.get('receiver'),
            self.get('subject'),
            self.get('date'),
            self.get('body_protocol'),
        )