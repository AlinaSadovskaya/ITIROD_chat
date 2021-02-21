class PersonalInfo:
    def __init__(self, login, port, ip):
        self.login = login
        self.port = port
        self.ip = ip
        self.message_with_person = list()

    def insert_mess(self, mess):
        self.message_with_person.append(mess)
