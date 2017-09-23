#!/usr/bin/env python

import pygame

pygame.init()

# surf = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
surf = pygame.display.set_mode((800, 600))

mainloop = True
while mainloop:
    for event in pygame.event.get():
        print "got event %r" % ((event,event.type, pygame.QUIT),)
        if event.type == pygame.QUIT:
            mainloop = False
    pygame.display.update()

pygame.quit()
