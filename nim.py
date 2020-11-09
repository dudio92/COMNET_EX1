#!/usr/bin/python3
import socket
import errno
import struct
import sys
from urllib.request import localhost

def start_game(hostname='127.0.0.1',port = 6444):
    unpacker = struct.Struct('>iii')
    try:
        clientSoc =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        clientSoc.connect(('127.0.0.1', port))
        recv_bytes = clientSoc.recv(unpacker.size)
        rec_unpacked = unpacker.unpack(recv_bytes)
        print_status(rec_unpacked)
        read_server_msg(clientSoc)
        while True:
            user_move = read_move()
            if user_move[0] == 0:
                send_move(user_move,clientSoc)
                clientSoc.close()
                return 0
            elif user_move[0] == 1:
                send_move(user_move,clientSoc)
                resposne = print_move_response(clientSoc,unpacker)
                get_print_heaps(unpacker,clientSoc)
                read_server_msg(clientSoc)
            else:
                send_move(user_move,clientSoc)
                resposne = print_move_response(clientSoc,unpacker)
                get_print_heaps(unpacker,clientSoc)
                read_server_msg(clientSoc)
    except OSError as error:
        if error.errno == errno.ECONNREFUSED:
            print("connection refused by server")
        else:
            print(error.strerror)
    finally:
        clientSoc.close()





def print_status(rec_unpacked):
    print("Heap A:",rec_unpacked[0])
    print("Heap B:", rec_unpacked[1])
    print("Heap C:",rec_unpacked[2])


def read_move():
    input_text = input()
    input_splitted = input_text.split()
    if len(input_splitted) == 1 :
        if input_splitted[0] == 'q' or input_splitted[0] == 'Q':
            return 0, input_splitted[0], None
        else:
            return 'X', 0, 0
    elif len(input_splitted) == 2:
        if input_splitted[0] == 'A' or input_splitted[0] == 'B' or input_splitted[0] == 'C':
            return 1, input_splitted[0], input_splitted[1]
        else:
            return 'X', 0, 0
    else:
            return 'X',0,0

def print_move_response(clientSoc,unpacker):
    response = int(clientSoc.recv(4).decode())
    print("response",response)
    if response == 1:
        print("Move accepted")
        return 1
    elif response == 0:
        print("Illegal move")
        return 0
    else:
        print("no valid return code")

def read_server_msg(clientSoc):
    recv = clientSoc.recv(4).decode()
    print("recv",recv)
    response = int(recv)
    print("response is",response)
    if response == 4 :
        print("Your turn:")
    elif response == 5:
        print("You win!")
    elif response == 6:
        print("Server win!")

def send_move(user_move,clientSoc):
    if user_move[0] == 1:
        heap_name_bytes = bytes(user_move[1], 'utf-8')
        move_struct = struct.pack(">1ci", heap_name_bytes, int(user_move[2]))
        clientSoc.sendall(move_struct)
    elif user_move[0] == 0 : #User pressed Q
        heap_name_bytes = bytes(user_move[1], 'utf-8')
        move_struct = struct.pack(">1ci", heap_name_bytes,0)
        clientSoc.sendall(move_struct)
    else: #Any illegal move
        heap_name_bytes = bytes('X', 'utf-8')
        move_struct = struct.pack(">1ci", heap_name_bytes,0)
        clientSoc.sendall(move_struct)



def get_print_heaps(unpacker,clientSoc):
    recv_bytes = clientSoc.recv(unpacker.size)
    rec_unpacked = unpacker.unpack(recv_bytes)
    print_status(rec_unpacked)





start_game()