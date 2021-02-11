import socket
import threading
import queue
from Message import send_message, get_message


def server_working(address, port):
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	server_socket.bind((address, port))
	user_addresses = {}
	user_logins = {}
	chats = {}
	user_chat = {}

	mess_queue = queue.Queue()
	reason_mess_queue = queue.Queue()
	threading.Thread(target=get_message, args=(server_socket, mess_queue, reason_mess_queue)).start()

	print('Server ia active!')
	while True:
		while not mess_queue.empty():
			message_from_queue = mess_queue.get()
			address, message = message_from_queue[0], message_from_queue[1]
			address_str = str(address[0]) + ':' + str(address[1])

			if address not in user_addresses.values():
				if message not in user_addresses.keys():
					user_addresses.update({message: address})
					user_logins.update({address_str: message})
					send_message(server_socket, 'set_name', reason_mess_queue, address)
					print('\nUser is logged!')
					print('New user name:', message)
				else:
					send_message(server_socket, 'sign_in_error', reason_mess_queue, address)

			elif user_logins[address_str] not in user_chat.keys():

				try:
					chat_name = message
					if chat_name not in chats.keys():
						chats[chat_name] = []

					chats[chat_name].append(address)
					user_chat[user_logins[address_str]] = chat_name
					send_message(server_socket, 'You are in the chat ' + chat_name + '!', reason_mess_queue, address)

					print('\nThe composition of the chat:')
					print('chats:', chats)

				except Exception as e:
					send_message(server_socket, 'sign_in_error', reason_mess_queue, address)

			elif user_logins[address_str] in user_chat.keys():
				send_message(server_socket, 'sent\n', reason_mess_queue, address)
				if message == 'leave_chat' or message == 'logout':
					name_of_chat = user_chat[user_logins[address_str]]
					chats[name_of_chat].remove(address)
					del user_chat[user_logins[address_str]]
					print('\nThe composition of the chat:')
					print('chats: ', chats)

					if message == 'leave_chat':
						send_message(server_socket, 'leaved', reason_mess_queue, address)
					if message == 'logout':
						name = user_logins[address_str]
						del user_logins[address_str]
						del user_addresses[name]
						send_message(server_socket, 'logout', reason_mess_queue, address)
						print('\nUser ' + name + ' deleted!')
				else:
					name_of_chat = user_chat[user_logins[address_str]]
					receiver_addresses = [receiver_address for receiver_address in chats[name_of_chat] if receiver_address != address]
					for receiver_address in receiver_addresses:
						send_message(server_socket, user_logins[address_str] + ' >> ' + message, reason_mess_queue, receiver_address)
						send_message(server_socket, 'delivered\n', reason_mess_queue, receiver_address)


if __name__ == '__main__':
	UDP_SERVER_IP_ADDRESS = '127.0.0.1'
	UDP_SERVER_PORT = 5001
	server_working(UDP_SERVER_IP_ADDRESS, UDP_SERVER_PORT)