#!/usr/bin/env python

import optparse
import pygame
import time

from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, ServerFactory
from twisted.protocols.basic import LineReceiver

allkeys = []
surf = None

def update_img(img_id):
    filename = "img/" + img_id
    img=pygame.image.load(filename)
    img=pygame.transform.scale(img, (800,600))
##    surf.blit(img,(0,0))
##    pygame.display.flip() # update the display

    for alpha in range(0,255,5):
        img.set_alpha(alpha)
        surf.blit(img,(0,0))
        pygame.display.flip() # update the display
        pygame.display.update()
mainloop = True

def keydown(s):
    '''called by mainloop when a key is pressed.  Takes a string representing
    the key that was pressed.'''
    global allkeys
    global mainloop
    print "keydown got %r" % s
    if s == '\r':
        tag = ''.join(allkeys)
        print(tag)
        update_img(tag)
        allkeys = []
    elif s == 'q' or s == 'Q':
        mainloop = False
    else:
        allkeys.append(s.encode('UTF8'))

def run_game(opts):
    global surf
    global mainloop
    pygame.init()

    if opts.full:
        surf = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
    else:
        surf = pygame.display.set_mode((800, 600))
    surf.fill((255,255,255))

    update_img("default")
    while mainloop:
        for event in pygame.event.get():
            print "got event %r" % ((event,event.type, pygame.QUIT),)
            if event.type == pygame.QUIT:
                mainloop = False
            if event.type == pygame.KEYDOWN:
                keydown(event.unicode)
        pygame.display.update()

    pygame.quit()


class ChatProtocol(LineReceiver):

    def __init__(self, recv):
        self.recv = recv

    def lineReceived(self,line):
        print "lineReceived %r" % line
        self.recv(line, self)

    def connectionMade(self):
        print "connection made"
    def connectionLost(self, reason):
        print "connection lost: %r" % reason

class ChatClient(ClientFactory):
    def __init__(self, recv):
        self.protocol = ChatProtocol
        self.recv = recv

    def buildProtocol(self, addr):
        global chatprotocol
        c = ChatProtocol(self.recv)
        chatprotocol.append(c)
        return c

chatprotocol = []

def sendline(s):
    for c in chatprotocol:
        print "%r <- %r" % (c, s)
        c.sendLine(s)

class Client(object):

    def __init__(self):
        self.line = 'no message'
        self.n = 0
        self.allkeys = []
        pygame.init()
        self.screen = pygame.display.set_mode((200, 200))
        reactor.callLater(0.1, self.tick)

    def new_line(self, line, responder):
        self.line = line

    def keydown(self, s):
        print "keydown %r" % s
        if s == '\r':
            a = ''.join(self.allkeys)
            self.allkeys = []
            sendline(a)
        else:
            self.allkeys.append(s.encode('UTF8'))

    def tick(self):
        self.n += 1
        self.screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                reactor.stop() # just stop somehow
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    reactor.stop() # just stop somehow
                else:
                    self.keydown(event.unicode)

        self.screen.blit(pygame.font.SysFont('mono', 12, bold=True).render(self.line, True, (0, 255, 0)), (20,20))
        pygame.display.flip()
        reactor.callLater(0.1, self.tick)

class ChatServer(ServerFactory):
    def __init__(self, recv):
        print "new ChatServer object"
        self.protocol = ChatProtocol
        self.recv = recv

    def buildProtocol(self, addr):
        print "buildProtocol"
        global chatprotocol
        c = ChatProtocol(self.recv)
        chatprotocol.append(c)
        return c

class Server(object):
    def __init__(self):
        print "created Server object"
        reactor.callLater(0.1, self.tick)
        self.n = 0
    def new_line(self, line, responder):
        print "Server new_line %r sending to %r" % (line, responder)
        responder.sendLine("fromserver %r" % line)
    def tick(self):
        self.n += 1
        # print "Server tick %d" % self.n
        reactor.callLater(0.1, self.tick)

def twistedclient(serveraddr):
    c = Client()
    reactor.connectTCP(serveraddr, 12345, ChatClient(c.new_line))
    reactor.run()

def twistedserver():
    s = Server()
    reactor.listenTCP(12345, ChatServer(s.new_line))
    reactor.run()

def main():
    parser = optparse.OptionParser()
    parser.add_option('-f', '--full', action='store_true')
    parser.add_option('-s', '--server', action='store_true')

    (opts, args) = parser.parse_args()

    if opts.server:
        twistedserver()
    else:
        twistedclient(args[0])

if __name__ == '__main__':
    main()
