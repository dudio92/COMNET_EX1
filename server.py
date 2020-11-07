import socket
import errno
import struct
import sys
import binascii

def start_game(n_a,n_b,n_c,port = 6444):

    heaps_list = [n_a,n_b,n_c]
    heaps_tuple = tuple(heaps_list)
    ListeningSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ListeningSocket.bind(('',port))
    ListeningSocket.listen(1)
    try:
        (clientConnected, clientAddress) = ListeningSocket.accept()
        print("Accepted a connection request from %s:%s" % (clientAddress[0], clientAddress[1]))
        packer = struct.Struct('>iii')
        packed_data = packer.pack(*heaps_tuple)
        print(sys.stderr, 'sending "%s"' % binascii.hexlify(packed_data), heaps_tuple)
        print("to client",clientAddress)
        clientConnected.sendall(packed_data)
        clientConnected.sendall(b'4')
        #while heaps_list[0] != 0 and heaps_list[1] != 0 and heaps_list[2] != 0:
        while True:
            recv_move = clientConnected.recv(5)
            recv_move_unpacked = struct.unpack(">1ci",recv_move)
            print("recv_move_unpacked",recv_move_unpacked)
            if recv_move_unpacked[0].decode() == 'A':
                if recv_move_unpacked[1] <= heaps_list[0]:
                    clientConnected.sendall(b'1')
                    heaps_list[0] = heaps_list[0] - recv_move_unpacked[1]
                    x = server_move(heaps_list)
                    send_updated_heaps(clientConnected, heaps_list,packer)
                    send_server_message(clientConnected,heaps_list,x)
                    #server_game_over(clientConnected,heaps_list)
                else:
                    clientConnected.sendall(b'0')
                    x = server_move(heaps_list)
                    send_updated_heaps(clientConnected, heaps_list, packer)
                    send_server_message(clientConnected,heaps_list,x)

            elif recv_move_unpacked[0].decode() == 'B':
                if recv_move_unpacked[1] <= heaps_list[1]:
                    clientConnected.sendall(b'1')
                    heaps_list[1] = heaps_list[1] - recv_move_unpacked[1]
                    x = server_move(heaps_list)
                    send_updated_heaps(clientConnected, heaps_list, packer)
                    send_server_message(clientConnected,heaps_list,x)
                    #server_game_over(clientConnected,heaps_list)
                else:
                    clientConnected.sendall(b'0')
                    x = server_move(heaps_list)
                    send_updated_heaps(clientConnected, heaps_list, packer)
                    send_server_message(clientConnected,heaps_list,x)

            elif recv_move_unpacked[0].decode() == 'C':
                if recv_move_unpacked[1] <= heaps_list[2]:
                    clientConnected.sendall(b'1')
                    print("sent 1 ")
                    heaps_list[2] = heaps_list[2] - recv_move_unpacked[1]
                    x = server_move(heaps_list)
                    send_updated_heaps(clientConnected, heaps_list, packer)
                    send_server_message(clientConnected,heaps_list,x)
                    #server_game_over(clientConnected,heaps_list)

                else:
                    clientConnected.sendall(b'0')
                    x = server_move(heaps_list)
                    send_updated_heaps(clientConnected, heaps_list, packer)
                    send_server_message(clientConnected,heaps_list,x)

            elif recv_move_unpacked[0].decode() == 'Q':
                print("Quit")
                clientConnected.close()






    except OSError as error:
        if  error.errno == errno.ECONNREFUSED:
            print("connection refused by server")
        else:
            print(error.strerror)
    ListeningSocket.close()


def server_move(heaps_list):
    if heaps_list[0] == heaps_list[1] == heaps_list[2] == 0:
        return 0
    else:
        heaps_list[heaps_list.index(max(heaps_list))] -= 1 #Make the server move
        return 1



def send_server_message(clientConnected,heaps_list,x):
    if x == 0 :
        clientConnected.sendall(b'5')  # "You win!"
        return

    elif heaps_list[0] == heaps_list[1] == heaps_list[2] == 0 and x==1:
        clientConnected.sendall(b'6') #"Server win!"
    else:
        clientConnected.sendall(b'4')  # "Your turn"

# def server_game_over(clientConnected,heaps_list):
#     if heaps_list[0] == heaps_list[1] == heaps_list[2] == 0 :
#         clientConnected.sendall(b'6')  #Server win!"



def send_updated_heaps(clientConnected, heaps_list, packer):
    values = tuple(heaps_list)
    print("values",values)
    packed_data = packer.pack(*values)
    clientConnected.sendall(packed_data)


# def process_user_move(recv_move_unpacked,heaps_list,clientConnected):
#     if recv_move_unpacked[1] <= heaps_list[0]:
#         heaps_list[0] = heaps_list[0] - recv_move_unpacked[1]
#         clientConnected.sendall(b'1')
#         if heaps_list[0] == 0 and heaps_list[1] == 0 and heaps_list[2] == 0:
#             clientConnected.sendall(b'2')
#         else:
#             server_move(heaps_list,clientConnected)
#     else:
#         clientConnected.sendall(b'0')



start_game(10,20,30)


