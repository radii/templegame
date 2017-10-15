#!/usr/bin/env python

import sys
import pygame
import optparse

from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, ServerFactory
from twisted.protocols.basic import LineReceiver

class ChatProtocol(LineReceiver):

    def __init__(self, recv):
        self.recv = recv

    def lineReceived(self,line):
        print "lineReceived %r" % line
        self.recv(line)

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
        chatprotocol = ChatProtocol(self.recv)
        return chatprotocol

chatprotocol = None

def sendline(s):
    chatprotocol.sendLine(s)

class Client(object):

    def __init__(self):
        self.line = 'no message'
        self.n = 0
        self.allkeys = []
        pygame.init()
        self.screen = pygame.display.set_mode((200, 200))
        reactor.callLater(0.1, self.tick)

    def new_line(self, line):
        print "new_line %r" % line
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
        # print "tick %d" % self.n
        for event in pygame.event.get():
            print "event %r" % event
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
        chatprotocol = ChatProtocol(self.recv)
        return chatprotocol

class Server(object):
    def __init__(self):
        print "created Server object"
        reactor.callLater(0.1, self.tick)
        self.n = 0
    def new_line(self, line):
        print "Server new_line %r" % line
        sendline("fromserver %r I WAS FROM ELSEWHERE" % line)
    def tick(self):
        self.n += 1
        # print "Server tick %d" % self.n
        reactor.callLater(0.1, self.tick)

def twistedclient(serverhost):
    global chatClient
    c = Client()
    chatClient = ChatClient(c.new_line)
    print "connecting to %r "% serverhost
    reactor.connectTCP(serverhost,1234, chatClient)
    reactor.run()

def twistedserver():
    s = Server()
    reactor.listenTCP(1234, ChatServer(s.new_line))
    reactor.run()

def twistedmain():
    if sys.argv[-1] == "-s":
        twistedserver()
    else:
        twistedclient(sys.argv[-1])

if __name__ == '__main__':
    twistedmain()
