import socket
import pygame
from _thread import *
from M5_Network import Network
from threading import Thread
import random
import sys
import S1_Server_Objekts
import S2_Server_Groups
import S3_Server_Functions

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = '192.168.0.17'
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
all_objekts = S2_Server_Groups.Server_Object_Group()


def threaded_client(conn):
    global currentId, pos, line_bullet
    conn.send(str.encode(currentId))
    if currentId == '1':
        currentId = '2'
    currentId = "1"

    player = False
    player_life = True
    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                conn.send(str.encode("Goodbye"))
                print('ooooooooooooo\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\noooooooooooo')
                if player:
                    player.kill()
                break
            else:

                if player:
                    if player.health <= 0:
                        player.kill()
                        player_life = False

                arr = reply.split(";;")
                reply_inf = arr[1].split(':')
                bullet_inf = arr[2].split(';')
                #print(reply_inf)

                player_life_in_list = S3_Server_Functions.check_id_in_group(all_objekts, reply_inf[0])

                if player_life_in_list:
                    player_life_in_list.receiving(reply_inf[1].split('.'), reply_inf[2])
                else:
                    if not player and player_life:
                        if len(reply_inf) == 3:
                            player = S1_Server_Objekts.Player(reply_inf[0], reply_inf[1].split('.'), reply_inf[2])
                            all_objekts.add(player)
                    else:
                        if reply_inf[0] == 'True':
                            player_life = True
                            player = False
                        else:
                            player_life = False
                            player = False

                for i in bullet_inf:
                    if i:
                        bullet_inf_splited = i.split(':')
                        line_bullet.add(S1_Server_Objekts.Server_line_bullet(*bullet_inf_splited))

            reply = str(bool(player_life)) + ';;' + ';'.join(keys.values()) + ';;' + line_bullet.str_transformation()
            #print(reply)
            conn.sendall(str.encode(reply))

        except Exception as a:
            print(a)
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
        line_bullet.collide_objekts(all_objekts)
        clock.tick(60)
        keys_now = {}
        for i in all_objekts:
            keys_now[i.id] = i.id + ':' + '.'.join([str(j) for j in i.cord]) + ':' + str(i.angle) + ':' + str(i.health)
        all_objekts.collide()
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