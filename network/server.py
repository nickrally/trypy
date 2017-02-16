import socket
import sys
from threading import Thread
import traceback


def process_input(input_str):
    return input_str[::-1]


def client_thread(conn, port, ip, MAX_BUFFER=4096):
    client_msg = conn.recv(MAX_BUFFER)
    msg_size = sys.getsizeof(client_msg)
    if msg_size >= MAX_BUFFER:
        print('the message is too long: {}'.format(msg_size))

    client_msg = client_msg.decode('utf-8').rstrip()
    result = process_input(client_msg)
    print('Result of processing {} is {}'.format(client_msg, result))
    result = result.encode('utf-8')
    conn.sendall(result)
    conn.close()
    print('Connection ' + ip + ':' + port + ' closed')


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server = '127.0.0.1'
    port = 5004
    try:
        server_socket.bind((server, port))
    except:
        print('Bind failed. Error: ' + str(sys.exc_info()))
        sys.exit()

    server_socket.listen(4)
    print('Listening...')

    while True:
        '''
        At accept(), a new socket is created that is distinct from the server_socket.
        This new socket is used only for communication with a particular client.
        For TCP servers, the socket object used to receive connections is not the same socket used
        to perform subsequent communication with the client.
        accept() returns a new socket obj that's actually used for the connection.
        It allows a server to have connections with many clients simultaneously.
        '''
        client_socket, addr = server_socket.accept()
        ip, port = str(addr[0]), str(addr[1])
        print('Accepting connection from ' + ip + ':' + port)
        try:
            Thread(target=client_thread, args=(client_socket, ip, port)).start()
        except:
            print('Oh,noes!')
            traceback.print_exc()
    server_socket.close()


start_server()
