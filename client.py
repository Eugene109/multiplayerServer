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
        self.pos = self.connect()
        print(self.pos)

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except: 
            print ('Something Went Wrong')
            pass

    def send(self, data):
        try:
            self.client.sendall(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])



import pygame

width = 500
height = 500

pygame.init()
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Prison Maze")

clientNumber = 0

cameraShiftx = -200
cameraShifty = -150


class Background():
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load('maze.png'), (247*8, 183*8))
    def draw(self, win):
        global cameraShiftx
        global cameraShifty
        win.blit(self.image, (-cameraShiftx, -cameraShifty))

class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = (x,y,width,height)
        self.color = (0,255,255)
        self.currentImageIndex = 0;
        self.images = [ pygame.transform.scale(pygame.image.load('costume1.png'), (20,40)),
                        pygame.transform.scale(pygame.image.load('costume2.png'), (20,40)),
                        pygame.transform.scale(pygame.image.load('costume3.png'), (20,40))]
        
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
        if win.get_at(((self.x - cameraShiftx) + diffx,(self.y - cameraShifty))).hsva[2] > 2:
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


class OtherPlayer():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = (x,y,width,height)
        self.color = (0,255,255)
        self.currentImageIndex = 0;
        self.images = [ pygame.transform.scale(pygame.image.load('costume1.png'), (20,40)),
                        pygame.transform.scale(pygame.image.load('costume2.png'), (20,40)),
                        pygame.transform.scale(pygame.image.load('costume3.png'), (20,40))]
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





def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def main():
    clock = pygame.time.Clock()
    n = Network()
    player = Player(read_pos(n.pos)[0], read_pos(n.pos)[1])
    running = True
    bg = Background()
    while running:
        clock.tick(30)
        # n.send("hi")
        playerPositionsString = n.send(make_pos((player.x, player.y)))
        # print(n.connect())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        win.fill((0, 0, 0))
        bg.draw(win)

        player.move(win)
        player.draw(win)
        pygame.display.update()


main()

pygame.quit()
quit()