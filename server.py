import socket
import pygame
from _thread import *
from M5_Network import Network
from threading import Thread
import random
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = 'localhost'
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

currentId = "0"
pos = ["0:50,50", "1:100,100"]
keys = {}
def threaded_client(conn):
    global currentId, pos
    conn.send(str.encode(currentId))
    if currentId == '1':
        currentId = '2'
    currentId = "1"
    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                conn.send(str.encode("Goodbye"))
                print('ooooooooooooo\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\noooooooooooo')
                break
            else:
                #print('o')
                print("Recieved: " + reply)
                arr = reply.split(";;")
                reply_inf = arr[1].split(';')
                for i in reply_inf:
                    reply_inf_splited = i.split(':')
                    keys[reply_inf_splited[0]] = i
                print(keys)
                id = int(arr[0])
                pos[id] = reply

                #if id == 0:
                #    nid = 1
                #if id == 1:
                #    nid = 0

                #reply = pos[nid]
                reply = ';'.join(keys.values())
                print("Sending: " + reply)
                print()

            conn.sendall(str.encode(reply))
        except Exception as e:
            break

    print("Connection Closed")
    conn.close()

def server_processing():
    clock = pygame.time.Clock()
    net = Network()
    asteroid = ['001' + '.' + str(random.randint(9999999, 100000000)) + ':' + '10.10' + ':' + '1500',
                '001' + '.' + str(random.randint(9999999, 100000000)) + ':' + '120.120' + ':' + '1500']
    print(asteroid)
    while True:
        clock.tick(60)
        print(clock.get_fps())
        net.send(net.id + ';;' + ';'.join(asteroid))

th = Thread(target=server_processing, args=())
th.start()
#start_new_thread(server_processing, ())
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn,))