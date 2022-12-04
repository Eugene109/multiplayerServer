import socket
from _thread import *
import sys

server = "192.168.1.160"
# server = "192.168.1.160"

# server = "127.0.1.1"

port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(3)
print("Waiting for a connection, Server Started")

def read_pos(str):
    str = str.split(',')
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

pos = []


currentPlayer = 0
import time

def threaded_client(conn, player_num, game_num):
    global currentPlayer
    copVsPrisoner = 0
    if player_num == 2 or player_num == 5:
        copVsPrisoner = 1
    print(player_num)
    conn.send(str.encode(make_pos(pos[game_num][player_num]) + "," + str(player_num)))
    print(pos[game_num][player_num])
    while currentPlayer%6 < 3:
        time.sleep(0.5)
    conn.send(str.encode("Game Start"))

    reply = ""
    while True:
        try:
            data = conn.recv(2048).decode()
            if not data:
                print("Disconnected")
                break
            else:
                pos[game_num][player_num] = read_pos(data)

                # print(pos[game_num][player_num])
                reply = ""
                for a in range(0,len(pos[game_num])):
                    if reply == "":
                        reply = make_pos(pos[game_num][a])
                    else:
                        reply = reply + "|" + make_pos(pos[game_num][a])

                # print("Received: " + data)
                # print("Sending : " + reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("Lost connection")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    if currentPlayer % 6 == 0:
        pos.append([(50,75), (50,100), (1976 - 50, 1464 - 150), (25,125), (25,100), (1976 - 50, 1464-100)])
    start_new_thread(threaded_client, (conn, currentPlayer%6, currentPlayer//6))
    currentPlayer += 1