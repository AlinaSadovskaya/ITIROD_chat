from Setting import Status as S
import threading
from PersonalInfo import PersonalInfo
from Message import UDP, Message


class Client:
    def __init__(self, login, Port, IP="127.0.0.1"):
        self.login = login
        self.UDP = UDP(IP, Port)
        self.list_client = list()
        self.actual_person_id = -1
        self.is_chatting = False

    def connect(self, Port, IP="127.0.0.1"):
        self.actual_person_id = len(self.list_client)
        self.sendMessage(self.login, S.REQUEST, None, Port, IP)
        self.check_chat(Port, IP)

    def sendMessage(self, login, status, mess, Port, IP="127.0.0.1"):
        message = Message(login, mess, status)
        if status == S.MESSAGE:
            self.list_client[self.actual_person_id].insert_mess(message)
        self.UDP.send(message, IP, Port)

    def work(self):
        work = threading.Thread(target=self.listen_client)
        work.start()
        while True:
            print('What do you want to do:')
            print('1)Connect to a user')
            print('2)View your chats')
            try:
                action = int(input())
            except:
                print("Invalid input! Try again")
                continue
            if action == 1:
                port = int(input("Enter the port to connect: "))
                self.connect(port)
            elif action == 2:
                if len(self.list_client) == 0:
                    print("You don't have any chats available!")
                else:
                    for num, client in enumerate(self.list_client):
                        print("{0}) @{1}".format(num + 1, client.login))
                    print("Enter the user number: ", end="")
                    client_id = int(input())
                    self.actual_person_id = client_id - 1
                    self.check_chat(self.list_client[self.actual_person_id].port, self.list_client[self.actual_person_id].ip)

    def show_chat(self, Port, IP="127.0.0.1"):
        for mes in self.list_client:
            if mes.port == Port and mes.ip == IP:
                for letter in mes.message_with_person:
                    print("{0}: {1}".format(letter.login, letter.mess))

    def check_chat(self, Port, IP="127.0.0.1"):
        self.show_chat(Port, IP)
        while True:
            message = input("Enter your message: ")
            if message == "exit":
                self.actual_person_id = -1
                break
            self.sendMessage(self.login, S.MESSAGE, message, Port, IP)

    def listen_client(self):
        while True:
            mess, address = self.UDP.receive()
            #print(mess)
            #print(self.actual_person_id)
            if mess['status'] == S.MESSAGE:
                if self.list_client[self.actual_person_id].login == mess['login'] \
                        and self.list_client[self.actual_person_id].port == address[1] \
                        and self.list_client[self.actual_person_id].ip == address[0] \
                        and self.actual_person_id != -1:
                    mes = Message(mess['login'], mess['mess'], S.MESSAGE)
                    self.list_client[self.actual_person_id].insert_mess(mes)
                    print('\n-----------------------------')
                    print("{0}: {1}".format(mess['login'], mess['mess']))
                    print('-----------------------------')
                    print("Enter your message:")
            else:
                if (mess['login'], address[1]) not in list(
                        zip((x.login for x in self.list_client), (x.port for x in self.list_client))):
                    client = PersonalInfo(mess['login'], address[1], address[0])
                    self.list_client.append(client)
                if mess['status'] == S.REQUEST:
                    self.is_chatting = True
                    self.sendMessage(self.login, S.RESPONSE, None, address[1], address[0])
