import socket
import threading
import queue
from Setting import Setting as S
from Message import send_message, get_message


def send_mess_chat(client_socket, name, reason_mess_queue, mess_queue):
    get_mess_chat_task = threading.Thread(target=get_chat_mess, args=(mess_queue,))
    get_mess_chat_task.start()

    print('\n')
    while True:
        message = input()

        global is_active
        if is_active == S.MESSAGE:
            send_message(client_socket, message, reason_mess_queue)
        else:
            get_mess_chat_task._stop()
            break


def get_chat_mess(received_message_queue):
    global is_active

    while True:
        if not received_message_queue.empty():
            message = received_message_queue.get()

            if message != 'chat was closed' and message != 'client was logout':
                print(message)
            elif message == 'chat was closed':
                print('You or someone left the chat so it was closed. Type something to choose another chat.')
                is_active = S.SET_CHAT_NAME

                return True
            else:
                print('You were logout. Type something to login again.')
                is_active = S.SET_NAME

                return True


def select_name(client_socket, mess_queue, reason_mess_queue):
    print('\nEnter your name: ')
    name = input()
    send_message(client_socket, name, reason_mess_queue)

    while True:
        if not mess_queue.empty():
            message = mess_queue.get()

            if message == 'sign_in_error':
                print('\nLogin error! Perhaps this name already exists. Try again with a different name:')
                name = input()
                send_message(client_socket, name, reason_mess_queue)
            if message == 'set_name':
                print('\nYou are registered!')
                global is_active
                is_active = S.SET_CHAT_NAME
                break

    return name


def choose_chat(client_socket, mess_queue, reason_mess_queue):
    print('\nPlease enter the name of the group chat:')
    chat = input()
    send_message(client_socket, chat, reason_mess_queue)

    while True:
        if not mess_queue.empty():
            message = mess_queue.get()

            if message == 'sign_in_error':
                print('\nSomething went wrong. Please try again.')
                chat = input('Please type chat you like to join: ')
                send_message(client_socket, chat, reason_mess_queue)
            else:
                print('\n' + message)
                print('\nIf you want to leave the chat, write : leave_chat')
                print('If you want to logout the chat, write : logout')

                global is_active
                is_active = S.MESSAGE

                break


def client_working(server_address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.connect(server_address)

    mess_queue = queue.Queue()
    reason_mess_queue = queue.Queue()
    threading.Thread(target=get_message, args=(
        client_socket, mess_queue, reason_mess_queue, server_address)).start()

    while True:
        global is_active
        if is_active == S.SET_CHAT_NAME:
            choose_chat(client_socket, mess_queue, reason_mess_queue)
        elif is_active == S.SET_NAME:
            name = select_name(client_socket, mess_queue, reason_mess_queue)
        elif is_active == S.MESSAGE:
            send_mess_chat(client_socket, name, reason_mess_queue, mess_queue)


if __name__ == '__main__':
    UDP_SERVER_IP_ADDRESS = '127.0.0.1'
    UDP_SERVER_PORT = 5001
    SERVER_ADDRESS = (UDP_SERVER_IP_ADDRESS, UDP_SERVER_PORT)
    UDP_CLIENT_IP_ADDRESS = '127.0.0.1'
    is_active = S.SET_NAME
    client_working(SERVER_ADDRESS)
