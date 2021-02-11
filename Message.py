from Setting import Setting as S


def send_message(sock, message, reason_message_queue, address=-1):
    epty_mes = ''
    if len(str(len(message))) <= S.HEADER_SIZE:
        for i in range(S.HEADER_SIZE - len(str(len(message)))):
            epty_mes = epty_mes + ' '

    new_message = str(len(message)) + epty_mes + message
    #print(new_message)
    if address == -1:
        sock.send(bytes(new_message, 'utf-8'))
    else:
        sock.sendto(bytes(new_message, 'utf-8'), address)

    while True:
        if not reason_message_queue.empty():
            reason = reason_message_queue.get()

            if reason == 'sent':
                return True
            else:
                current_index_of_message = message
                if address == -1:
                    sock.send(bytes(new_message[int(current_index_of_message):], 'utf-8'))
                else:
                    sock.sendto(bytes(new_message[int(current_index_of_message):], 'utf-8'), address)


def get_message(sock, message_queue, reason_message_queue, server_address=-1):
    message, len_mes_part = '', 0
    is_first_step = True
    while True:
        mess_part, address = sock.recvfrom(S.PACKAGE_SIZE)
        mess_part = mess_part.decode('utf-8')

        mess_after = mess_part[:S.HEADER_SIZE]
        mess_before = mess_part[S.HEADER_SIZE:]

        if server_address != -1 and address != server_address:
            continue

        if mess_after == ' ' * S.HEADER_SIZE:
            reason_message_queue.put(mess_before)
            continue

        if is_first_step:
            len_mes_part = int(mess_after)
            is_first_step = False

        message += mess_part

        if len(message[S.HEADER_SIZE:]) == len_mes_part:
            if server_address == -1:
                sock.sendto(bytes(' ' * S.HEADER_SIZE + 'sent', 'utf-8'), address)
                message_queue.put((address, message[S.HEADER_SIZE:]))
            else:
                sock.send(bytes(' ' * S.HEADER_SIZE + 'sent', 'utf-8'))
                message_queue.put((message[S.HEADER_SIZE:]))

            message, is_first_step = '', True
        else:
            if server_address == -1:
                sock.sendto(bytes(' ' * S.HEADER_SIZE + str(len(message)), 'utf-8'), address)
            else:
                sock.send(bytes(' ' * S.HEADER_SIZE + str(len(message)), 'utf-8'))
