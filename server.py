import socket
from _thread import *
import sys

# server = "192.168.1.160"
server = "192.168.1.160"

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

pos = [(50,75), (50,100), (50,125), (25,125), (25,100), (1976 - 50,1464 - 100)]

def threaded_client(conn, player_num):
    copVsPrisoner = 0
    if player_num == 5:
        copVsPrisoner = 1
    print(player_num)
    conn.send(str.encode(make_pos(pos[player_num]) + "," + str(player_num)))
    print(pos[player_num])
    reply = ""
    while True:
        # try:
        data = conn.recv(2048).decode()
        pos[player_num] = read_pos(data)

        print(pos[player_num])
        if not data:
            print("Disconnected")
            break
        else:
            # reply = make_pos(pos[player_num-1])
            reply = ""
            for a in range(0,len(pos)):
                if reply == "":
                    reply = make_pos(pos[a])
                else:
                    reply = reply + "|" + make_pos(pos[a])

            # print("Received: " + data)
            # print("Sending : " + reply)

        conn.sendall(str.encode(reply))
        # except:
            # break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1