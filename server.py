import socket
import pygame
from _thread import *
from M5_Network import Network
from threading import Thread
import random
import sys
import S1_Server_Objekts
import S2_Server_Groups

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
line_bullet = S2_Server_Groups.Server_Line_Bullet_Group()
all_objekts = pygame.sprite.Group()


def threaded_client(conn):
    global currentId, pos, line_bullet
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
                ##print("Recieved: " + reply)
                arr = reply.split(";;")
                reply_inf = arr[1].split(';')
                bullet_inf = arr[2].split(';')
                for i in reply_inf:
                    reply_inf_splited = i.split(':')
                    #print(reply_inf_splited)
                    if reply_inf_splited[0] in keys.keys():
                        for j in all_objekts:
                            if j.id == reply_inf_splited[0]:
                                j.receiving(reply_inf_splited[1].split('.') + [64, 64], reply_inf_splited[2])
                                break
                        else:
                            all_objekts.add(S1_Server_Objekts.Server_colide_objekt(reply_inf_splited[0], reply_inf_splited[1].split('.') + [64, 64], reply_inf_splited[2]))
                    keys[reply_inf_splited[0]] = i
                for i in bullet_inf:
                    if i:
                        bullet_inf_splited = i.split(':')
                        line_bullet.add(S1_Server_Objekts.Server_line_bullet(*bullet_inf_splited))
                ##print(keys)
                ##print(arr[2])
                id = int(arr[0])
                pos[id] = reply

                #if id == 0:
                #    nid = 1
                #if id == 1:
                #    nid = 0

                #reply = pos[nid]
                reply = ';'.join(keys.values()) + ';;' + line_bullet.str_transformation()
                ##print("Sending: " + reply)
                ##print()

            conn.sendall(str.encode(reply))
        except Exception as e:
            break

    print("Connection Closed")
    conn.close()


def server_processing():
    global pos, all_objekts, line_bullet, keys
    clock = pygame.time.Clock()
    #net = Network()
    all_objekts.add(S1_Server_Objekts.Server_Objekt([10, 10, 64, 64], health=1500, angle_speed=random.randint(-200, 200) / 100))
    all_objekts.add(S1_Server_Objekts.Server_Objekt([120, 120, 64, 64], health=1500, angle_speed=random.randint(-200, 200) / 100))
    all_objekts.add(S1_Server_Objekts.Server_Objekt([520, 520, 64, 64], health=1500, angle_speed=random.randint(-200, 200) / 100))

    #asteroid = ['001' + '.' + str(random.randint(9999999, 100000000)) + ':' + '10.10' + ':' + '1500',
    #            '001' + '.' + str(random.randint(9999999, 100000000)) + ':' + '120.120' + ':' + '1500',
    #            '001' + '.' + str(random.randint(9999999, 100000000)) + ':' + '520.360' + ':' + '1500']
    #print(asteroid)
    while True:
        #print(line_bullet)
        for i in line_bullet:
            if i.time + 200 < pygame.time.get_ticks():
                i.kill()
        print(len(all_objekts), len(keys.keys()))
        line_bullet.collide_objekts(all_objekts)
        clock.tick(60)
        keys_now = {}
        for i in all_objekts:
            keys_now[i.id] = i.id + ':' + '.'.join([str(j) for j in i.cord]) + ':' + str(i.angle) + ':' + str(i.health)
        keys = keys_now
        all_objekts.update()
        #print()
        #clock.tick(60)
        #print(clock.get_fps())
        #net.send(net.id + ';;' + ';'.join(asteroid))

th = Thread(target=server_processing, args=())
th.start()
#start_new_thread(server_processing, ())
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn,))