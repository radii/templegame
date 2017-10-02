#!/usr/bin/env python

import pygame
import time

pygame.init()

# surf = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
surf = pygame.display.set_mode((800, 600))
surf.fill((255,255,255))

allkeys = []

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

def keydown(s):
    '''called by mainloop when a key is pressed.  Takes a string representing
    the key that was pressed.'''
    global allkeys
    print "keydown got %r" % s
    if s == '\r':
        tag = ''.join(allkeys)
        print(tag)
        update_img(tag)
        allkeys = []
    else:
        allkeys.append(s.encode('UTF8'))

update_img("default")
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
