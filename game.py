import socket

# from signal import signal, SIGPIPE, SIG_DFL

# signal(SIGPIPE,SIG_DFL)

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "72.73.24.66"
        # self.server = "127.0.1.1"
        # self.server = "192.168.1.160"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.startArgs = self.connect()
        print(self.startArgs)

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except: 
            print ('Cannot connect to server')
            exit()
            pass

    def send(self, data):
        try:
            self.client.sendall(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

    def recieve(self):
        try:
            return self.client.recv(2048).decode()
        except:
            print ('Cannot connect to server')
            exit()

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])



import pygame

width = 500
height = 500


clientNumber = 0

cameraShiftx = -200
cameraShifty = -150


class Background():
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load('maze.png'), (1926, 1464))
    def draw(self, win):
        global cameraShiftx
        global cameraShifty
        # win.blit(self.image, (-cameraShiftx, -cameraShifty))
        win.blit(self.image, (-cameraShiftx, -cameraShifty))

caught = False

class Player():
    def __init__(self, x, y, IsCopOrPrisoner): # False = prisoner true = cop
        global cameraShiftx
        global cameraShifty
        self.x = x
        self.y = y
        cameraShiftx = -self.x
        cameraShifty = -self.y
        self.rect = (x,y,width,height)
        self.color = (0,255,255)
        self.currentImageIndex = 0;
        self.is_cop = IsCopOrPrisoner
        self.images = [ pygame.transform.scale(pygame.image.load('costume1.png'), (20,40)),
                        pygame.transform.scale(pygame.image.load('costume2.png'), (20,40)),
                        pygame.transform.scale(pygame.image.load('costume3.png'), (20,40))]
        if self.is_cop:
            self.images = [ pygame.transform.scale(pygame.image.load('copCostume1.png'), (20,40)),
                            pygame.transform.scale(pygame.image.load('copCostume2.png'), (20,40)),
                            pygame.transform.scale(pygame.image.load('copCostume3.png'), (20,40))]
            
        
        self.vel = 5
        self.tick = 0

    def draw(self, win):
        global cameraShiftx
        global cameraShifty
        win.blit(self.images[self.currentImageIndex], (self.x - cameraShiftx, self.y - cameraShifty))

    def move(self, win):
        keys = pygame.key.get_pressed()

        diffx = 0;
        diffy = 0;
        if keys[pygame.K_LEFT]:
            diffx -= self.vel
        if keys[pygame.K_RIGHT]:
            diffx += self.vel
        if keys[pygame.K_UP]:
            diffy -= self.vel
        if keys[pygame.K_DOWN]:
            diffy += self.vel
        if keys[pygame.K_a]:
            diffx -= self.vel
        if keys[pygame.K_d]:
            diffx += self.vel
        if keys[pygame.K_w]:
            diffy -= self.vel
        if keys[pygame.K_s]:
            diffy += self.vel


        global cameraShiftx
        global cameraShifty
        #check value at corners
        if win.get_at(((self.x - cameraShiftx) + diffx,(self.y - cameraShifty))).hsva[2] > 2: # 2/255
            diffx = 0
        if win.get_at(((self.x - cameraShiftx)+20 + diffx,(self.y - cameraShifty))).hsva[2] > 2:
            diffx = 0
        if win.get_at(((self.x - cameraShiftx) + diffx,(self.y - cameraShifty)+40)).hsva[2] > 2:
            diffx = 0
        if win.get_at(((self.x - cameraShiftx)+20 + diffx,(self.y - cameraShifty)+40)).hsva[2] > 2:
            diffx = 0
        if win.get_at(((self.x - cameraShiftx),(self.y - cameraShifty) + diffy)).hsva[2] > 2:
            diffy = 0
        if win.get_at(((self.x - cameraShiftx)+20,(self.y - cameraShifty) + diffy)).hsva[2] > 2:
            diffy = 0
        if win.get_at(((self.x - cameraShiftx),(self.y - cameraShifty)+40 + diffy)).hsva[2] > 2:
            diffy = 0
        if win.get_at(((self.x - cameraShiftx)+20,(self.y - cameraShifty)+40 + diffy)).hsva[2] > 2:
            diffy = 0
        self.x += diffx
        cameraShiftx += diffx
        self.y += diffy
        cameraShifty += diffy

        if diffy == 0 and diffx == 0:
            self.currentImageIndex = 0
        else:
            self.currentImageIndex = 1 + ((self.tick // 3) % 2)

        self.tick += 1

    def check_cop_collision(self, CopPositions):
        global caught
        for a in range (0, 2):
            if CopPositions[a][0] - self.x > -10 and CopPositions[a][0] - self.x < 30:
                caught = True
            if CopPositions[a][1] - self.y > -20 and CopPositions[a][1] - self.y < 60:
                caught = True


class Prisoner():
    def __init__(self, x, y, IsCopOrPrisoner):
        self.x = x
        self.y = y
        self.rect = (x,y,width,height)
        self.color = (0,255,255)
        self.currentImageIndex = 0;
        self.is_cop = IsCopOrPrisoner
        self.images = [ pygame.transform.scale(pygame.image.load('costume1.png'), (20,40)),
                        pygame.transform.scale(pygame.image.load('costume2.png'), (20,40)),
                        pygame.transform.scale(pygame.image.load('costume3.png'), (20,40))]
        if self.is_cop:
            self.images = [ pygame.transform.scale(pygame.image.load('copCostume1.png'), (20,40)),
                            pygame.transform.scale(pygame.image.load('copCostume2.png'), (20,40)),
                            pygame.transform.scale(pygame.image.load('copCostume3.png'), (20,40))]
            
        self.tick = 0
        self.prevX = x
        self.prevY = y

    def draw(self, win):
        global cameraShiftx
        global cameraShifty
        if self.prevX-self.x != 0 or self.prevY-self.y != 0:
            self.currentImageIndex =  1 + ((self.tick // 3) % 2)
        else:
            self.currentImageIndex = 0
        win.blit(self.images[self.currentImageIndex], (self.x - cameraShiftx, self.y - cameraShifty))
        self.tick += 1
        self.prevX = self.x
        self.prevY = self.y


class GotCaughtScreen():
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load('endGameScreen.png'), (245, 147))
        self.x = 250 - 245//2
        self.y = 250 - 147//2
    def draw(self, win):
        win.blit(self.image, self.x, self.y)


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])
def parse_args(str):
    str = str.split(",")
    return int(str[0]), int(str[1]), int(str[2])

def main():
    pygame.init()
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Prison Maze")
    playerPositions = [(0,0), (0,0),(0,0), (0,0), (0,0), (0,0),]
    clock = pygame.time.Clock()
    global net
    player = Player(parse_args(net.startArgs)[0], parse_args(net.startArgs)[1], bool(parse_args(net.startArgs)[2] == 5 or parse_args(net.startArgs)[2] == 2))
    global cameraShiftx
    global cameraShifty
    cameraShiftx = -250 + player.x
    cameraShifty = -250 + player.y
    playerIndex = parse_args(net.startArgs)[2]
    otherPlayers = [Prisoner(0,0,0), Prisoner(0,0,0), Prisoner(0,0,1), Prisoner(0,0,0), Prisoner(0,0,0), Prisoner(0,0,1),]
    del otherPlayers [playerIndex]
    running = True
    bg = Background()
    caughtScreen = GotCaughtScreen()
    while running:
        clock.tick(30)
        # n.send("hi")
        idk1 = cameraShiftx
        idk2 = cameraShifty
        cameraShifty = 0
        cameraShiftx = 0
        bg.draw(win)
        cameraShiftx = idk1
        cameraShifty = idk2
        playerPositionsString = net.send(make_pos((player.x, player.y)))
        playerPositionsStringsSeparated = playerPositionsString.split('|')
        for a in range(0, len(playerPositions) - 1):
            if a < playerIndex:
                playerPositions[a] = read_pos(playerPositionsStringsSeparated[a])
                otherPlayers[a].x = playerPositions[a][0]
                otherPlayers[a].y = playerPositions[a][1]
            else:
                playerPositions[a+1] = read_pos(playerPositionsStringsSeparated[a+1])
                otherPlayers[a].x = playerPositions[a+1][0]
                otherPlayers[a].y = playerPositions[a+1][1]


        if not player.is_cop:
            player.check_cop_collision([playerPositions[2], playerPositions[5]])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        win.fill((0, 0, 0))
        bg.draw(win)

        player.move(win)
        bg.draw(win)
        for a in otherPlayers:
            a.draw(win)
        player.draw(win)

        if caught:
            caughtScreen.draw(win)

        pygame.display.update()

net = Network()
print("Waiting for at least 3 players...")
print("Hint: you can join multiple times from the same computer")

import time
while True:
    if net.recieve() != "":
        break
    time.sleep(0.5)

main()

pygame.quit()
quit()