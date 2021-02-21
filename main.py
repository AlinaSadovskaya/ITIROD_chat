from Client import Client


if __name__ == "__main__":
    print("Enter the login under which you will be displayed in the user chat: ")
    login = input()
    print("Enter the port for creating the client: ")
    clientPort = int(input())
    while True:
        try:
            client = Client(login, clientPort)
            break
        except Exception:
            print("The user cannot be created!")
            print("Enter the new port for creating the client: ")
            clientPort = int(input())
    client.work()
