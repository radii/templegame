#!/usr/bin/env python

import pygame

pygame.init()

# surf = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
surf = pygame.display.set_mode((800, 600))

allkeys = []

def keydown(s):
    '''called by mainloop when a key is pressed.  Takes a string representing
    the key that was pressed.'''
    global allkeys
    print "keydown got %r" % s
    if s == '\r':
       print 'got %r' % allkeys
       allkeys = []
    else:
       allkeys.append(s)

mainloop = True
while mainloop:
    for event in pygame.event.get():
        print "got event %r" % ((event,event.type, pygame.QUIT),)
        if event.type == pygame.QUIT:
            mainloop = False
        if event.type == pygame.KEYDOWN:
            keydown(event.unicode)
    pygame.display.update()

pygame.quit()
